import asyncio
import logging
from flask import Flask, render_template, jsonify, request
from tardis_client import TardisClient, Channel
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Your API key
API_KEY = "TD.SfYCQOzqT-jrf-Ad.hKDNp399hs7YdbK.kQBlFtDulneF1VV.VClWHQAmLEEqNRm.TNnNEkg8P39U9Lx.G-AQ"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/replay', methods=['POST'])
def replay_data():
    data = request.json
    exchange = data.get('exchange', 'bitmex')
    from_date = data.get('from_date', '2024-12-01')
    to_date = data.get('to_date', '2024-12-01 00:10:00')
    symbols = data.get('symbols', ['XBTUSD'])
    limit = data.get('limit', 50)
    
    logger.info(f"Replay request: exchange={exchange}, from={from_date}, to={to_date}, symbols={symbols}, limit={limit}")
    
    async def fetch_data():
        logger.debug("Initializing Tardis client...")
        tardis_client = TardisClient(api_key=API_KEY)
        
        logger.debug(f"Starting replay for {exchange}...")
        messages = tardis_client.replay(
            exchange=exchange,
            from_date=from_date,
            to_date=to_date,
            filters=[Channel(name="trade", symbols=symbols)],
        )
        
        results = []
        count = 0
        logger.debug("Iterating through messages...")
        async for local_timestamp, message in messages:
            results.append({
                'timestamp': local_timestamp.isoformat(),
                'data': message
            })
            count += 1
            if count % 10 == 0:
                logger.debug(f"Fetched {count} messages so far...")
            if count >= limit:
                break
        
        logger.info(f"Completed fetch: {len(results)} messages retrieved")
        return results
    
    try:
        results = asyncio.run(fetch_data())
        return jsonify({
            'success': True,
            'count': len(results),
            'data': results
        })
    except Exception as e:
        logger.error(f"Error during replay: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
