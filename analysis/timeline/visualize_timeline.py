import os
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html
from datetime import datetime, timedelta

# ================= Configuration =================
# 1. Path to your Bitcoin Data CSV
# Assuming it's in the sibling 'ibit/data' folder based on your previous structure.
# Please update this if your file is named differently or located elsewhere.
BTC_CSV_PATH = "BTCUSD_PERP-1m-2025-10-10.zip"

# 2. Target Date to Visualize (UTC)
TARGET_DATE_STR = "2025-10-10"

# 3. Events to Annotate
# Format: "HH:MM" in UTC
TIMELINE_EVENTS = [
    {"time": "20:50", "text": "Trump Post about Tariff", "color": "green"},
    {"time": "21:12", "text": "Binance Crypto Withdrawals Halted", "color": "blue"},
    {"time": "22:06", "text": "SPY Intraday Low", "color": "purple"},
    # You can add more events here
]

# 4. Time Ranges to Highlight (Background Color)
TIMELINE_REGIONS = [
    {
        "start": "21:00", 
        "end": "21:40", 
        "text": "Binance Widespread System Overload Error<br>(exact time requires Binance disclosure)", 
        "color": "orange"
    }
]

# 5. Depth Data Path
DEPTH_CSV_PATH = "BTCUSDT-bookDepth-2025-10-10.csv"

# 6. IBIT Data Path
IBIT_CSV_PATH = "BATS_IBIT, 2.csv"
# =================================================

def load_btc_data(file_path):
    """Loads Bitcoin CSV/ZIP data."""
    if not os.path.exists(file_path):
        # Try absolute path if relative fails, or just return None
        if os.path.exists(os.path.abspath(file_path)):
            file_path = os.path.abspath(file_path)
        else:
            print(f"File not found: {file_path}")
            return None

    try:
        # Determine compression based on extension
        compression = 'zip' if file_path.lower().endswith('.zip') else None
        # Read CSV (pandas handles zip compression automatically if specified)
        df = pd.read_csv(file_path, compression=compression)
        
        # Normalize column names to lower case and strip spaces
        df.columns = [c.strip().lower() for c in df.columns]
        
        # Handle 'open_time' from Binance format
        if 'open_time' in df.columns:
            df.rename(columns={'open_time': 'time'}, inplace=True)

        # Convert timestamp
        # Assuming unix timestamp in seconds or milliseconds
        if pd.api.types.is_numeric_dtype(df['time']):
            first_ts = float(df['time'].iloc[0])
            unit = 'ms' if first_ts > 10000000000 else 's'
            df['time'] = pd.to_datetime(df['time'], unit=unit, utc=True)
        else:
            df['time'] = pd.to_datetime(df['time'], utc=True)
            
        df.set_index('time', inplace=True)
        df.sort_index(inplace=True)
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def load_ibit_data(file_path):
    """Loads IBIT CSV data."""
    if not os.path.exists(file_path):
        print(f"IBIT file not found: {file_path}")
        return None

    try:
        # Read CSV
        df = pd.read_csv(file_path)
        
        # Normalize column names
        df.columns = [c.strip().lower() for c in df.columns]
        
        # Convert timestamp (assuming unix seconds based on snippet)
        if 'time' in df.columns:
            df['time'] = pd.to_datetime(df['time'], unit='s', utc=True)
            
        df.set_index('time', inplace=True)
        df.sort_index(inplace=True)
        return df
    except Exception as e:
        print(f"Error loading IBIT data: {e}")
        return None

def load_depth_cross_events(file_path):
    """Loads depth data and identifies crossed order book events."""
    if not os.path.exists(file_path):
        print(f"Depth data file not found: {file_path}")
        return None
    
    try:
        df = pd.read_csv(file_path)
        df.columns = [c.strip() for c in df.columns]
        
        # Parse timestamp
        time_col = 'timestamp' if 'timestamp' in df.columns else 'wtimestamp'
        
        # Clean timestamp strings (remove potential leading spaces)
        if df[time_col].dtype == 'object':
            df[time_col] = df[time_col].astype(str).str.strip()

        df[time_col] = pd.to_datetime(df[time_col], format='mixed')
        if df[time_col].dt.tz is None:
             df[time_col] = df[time_col].dt.tz_localize('UTC')
        else:
             df[time_col] = df[time_col].dt.tz_convert('UTC')

        # Filter for relevant percentages: -3, -2, -1 (Bids) and 1 (Ask)
        relevant = df[df['percentage'].isin([-3, -2, -1, 1])].copy()
        
        # Pivot to get prices in columns
        pivoted = relevant.pivot(index=time_col, columns='percentage', values='weighted_avg_price')
        
        events = []
        for ts, row in pivoted.iterrows():
            if 1 not in row: continue
            
            ask1 = row[1]
            
            # Check levels of crossing (Bid > Ask)
            if -1 in row and row[-1] > ask1:
                events.append({'time': ts, 'y_value': 2, 'text': 'Level 1 Cross'})
                
                if -2 in row and row[-2] > ask1:
                    events.append({'time': ts, 'y_value': 1, 'text': 'Level 2 Cross'})
                    
                    if -3 in row and row[-3] > ask1:
                        events.append({'time': ts, 'y_value': 0, 'text': 'Level 3 Cross'})
                
        return pd.DataFrame(events) if events else None
    except Exception as e:
        print(f"Error processing depth data: {e}")
        return None

def create_figure(df, target_date_str, events, regions, depth_crosses=None, df_ibit=None):
    """Creates the Plotly figure with annotations."""
    # Filter data for the target date (UTC)
    target_date = pd.to_datetime(target_date_str).date()
    # Get data for the whole day plus maybe a bit of next day for context
    start_ts = pd.Timestamp(target_date).tz_localize('UTC')
    end_ts = start_ts + timedelta(hours=24)
    
    mask = (df.index >= start_ts) & (df.index <= end_ts)
    df_day = df.loc[mask]

    if df_day.empty:
        return go.Figure().add_annotation(text="No data found for this date", showarrow=False)

    # Calculate scaling ratio based on early data (before 20:00 UTC)
    # Ratio = BTC Price / IBIT Price
    price_ratio = None
    if df_ibit is not None:
        cutoff_ts = pd.Timestamp(f"{target_date_str} 20:00:00").tz_localize('UTC')
        
        # Filter for early data to calculate the "correct" ratio
        btc_early = df_day[df_day.index < cutoff_ts]
        # Filter IBIT similarly (need to align with day first)
        ibit_day_subset = df_ibit[(df_ibit.index >= start_ts) & (df_ibit.index <= end_ts)]
        ibit_early = ibit_day_subset[ibit_day_subset.index < cutoff_ts]

        if not btc_early.empty and not ibit_early.empty:
            # Use mean of Low for BTC (since we plot Low) and Close for IBIT
            avg_btc = btc_early['low'].mean()
            avg_ibit = ibit_early['close'].mean()
            if avg_ibit > 0:
                price_ratio = avg_btc / avg_ibit

    # Create Main Price Line
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_day.index, 
        y=df_day['low'], 
        mode='lines', 
        name='BTC Price',
        line=dict(color='#1f77b4', width=2)
    ))

    # Add IBIT Price Trace
    if df_ibit is not None:
        # Filter IBIT data for the same range
        mask_ibit = (df_ibit.index >= start_ts) & (df_ibit.index <= end_ts)
        df_ibit_day = df_ibit.loc[mask_ibit]
        
        if not df_ibit_day.empty:
            fig.add_trace(go.Scatter(
                x=df_ibit_day.index,
                y=df_ibit_day['close'],
                mode='lines',
                name='IBIT Price',
                line=dict(color='#8c564b', width=2, dash='dot'), # Brown dashed line
                yaxis='y3'
            ))

    # Add Regions (Highlight specific time ranges)
    for region in regions:
        start_ts = pd.to_datetime(f"{target_date_str} {region['start']}:00").tz_localize('UTC')
        end_ts = pd.to_datetime(f"{target_date_str} {region['end']}:00").tz_localize('UTC')
        
        fig.add_vrect(
            x0=start_ts, 
            x1=end_ts,
            fillcolor=region['color'],
            opacity=0.1,
            layer="below",
            line_width=0
        )

    # Add Depth Cross Annotations
    if depth_crosses is not None and not depth_crosses.empty:
        fig.add_trace(go.Scatter(
            x=depth_crosses['time'],
            y=depth_crosses['y_value'],
            mode='markers',
            name='Binance Book Depth Anomaly (Bid > Ask)',
            marker=dict(size=4, color='red', symbol='circle'),
            hovertemplate='<b>Book Data Anomaly</b><br>Time: %{x}<br>Level: %{y}<extra></extra>',
            yaxis='y2'
        ))

    # Add Region Legend Entries (to appear below anomalies in legend)
    for region in regions:
        fig.add_trace(go.Scatter(
            x=[None], y=[None],
            mode='markers',
            name=region['text'],
            marker=dict(size=10, color=region['color'], symbol='square')
        ))

    # Add Event Annotations
    for i, event in enumerate(events):
        event_time_str = f"{target_date_str} {event['time']}:00"
        event_ts = pd.to_datetime(event_time_str).tz_localize('UTC')
        
        # Calculate staggered y position for text (on yaxis2)
        # yaxis2 range is [-25, 5]. Bottom is -25.
        # We place text below -25 to appear under the chart.
        y_pos = -27 - (i % 4) * 2

        fig.add_trace(go.Scatter(
            x=[event_ts, event_ts],
            y=[y_pos, 5], # Line from text to top of chart
            mode='lines+text',
            name=event['text'],
            text=[event['text'], None],
            textposition="bottom center",
            textfont=dict(color=event['color']),
            line=dict(color=event['color'], width=1, dash="dash"),
            yaxis='y2',
            cliponaxis=False, # Allow text to appear outside plot area
            showlegend=True
        ))

    # Determine Y-Axis Ranges
    # Get min/max for BTC to set a nice view
    btc_min = df_day['low'].min()
    btc_max = df_day['low'].max()
    # Add some padding (e.g. 5%)
    padding = (btc_max - btc_min) * 0.05
    btc_range = [btc_min - padding, btc_max + padding]
    
    # Calculate corresponding IBIT range to keep percentage fluctuation identical
    # Range_IBIT = Range_BTC / Ratio
    ibit_range = None
    if price_ratio:
        ibit_range = [btc_range[0] / price_ratio, btc_range[1] / price_ratio]

    fig.update_layout(
        title=f"Bitcoin Price Timeline - {target_date_str}",
        xaxis_title="Time (UTC)",
        yaxis_title="Price (USD)",
        hovermode="x unified",
        template="plotly_white",
        height=700,
        margin=dict(t=50, b=160), # Increase bottom margin to accommodate staggered labels
        yaxis=dict(
            range=btc_range,
            title="BTC Price"
        ),
        yaxis2=dict(
            overlaying='y',
            side='right',
            range=[-25, 5], # Keep dots at the top of the chart
            visible=False,  # Hide axis labels
            fixedrange=True
        ),
        yaxis3=dict(
            title="IBIT Price",
            overlaying='y',
            side='right',
            showgrid=False,
            range=ibit_range
        )
    )
    return fig

# ================= Main Execution =================
if __name__ == '__main__':
    print(f"Loading data from: {BTC_CSV_PATH}")
    df = load_btc_data(BTC_CSV_PATH)
    
    if df is not None:
        print("Data loaded. Starting server...")
        
        # Load depth cross events
        depth_crosses = load_depth_cross_events(DEPTH_CSV_PATH)
        df_ibit = load_ibit_data(IBIT_CSV_PATH)
        
        app = Dash(__name__)
        fig = create_figure(df, TARGET_DATE_STR, TIMELINE_EVENTS, TIMELINE_REGIONS, depth_crosses, df_ibit)
        
        app.layout = html.Div([
            dcc.Graph(figure=fig, style={'height': '90vh'})
        ])
        
        app.run(debug=True, port=8050)
    else:
        print("Failed to load data. Please check the BTC_CSV_PATH.")