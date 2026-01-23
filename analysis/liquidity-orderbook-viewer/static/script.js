async function fetchData() {
    const exchange = document.getElementById('exchange').value;
    const fromDate = document.getElementById('fromDate').value.replace('T', ' ');
    const toDate = document.getElementById('toDate').value.replace('T', ' ');
    const symbolsInput = document.getElementById('symbols').value;
    const symbols = symbolsInput.split(',').map(s => s.trim());
    const limit = parseInt(document.getElementById('limit').value);
    
    console.log('🚀 Fetching data with params:', { exchange, fromDate, toDate, symbols, limit });
    
    const statusDiv = document.getElementById('status');
    const resultsDiv = document.getElementById('results');
    const fetchBtn = document.getElementById('fetchBtn');
    
    // Show loading state
    statusDiv.className = 'status loading';
    statusDiv.textContent = 'Fetching data...';
    resultsDiv.innerHTML = '';
    fetchBtn.disabled = true;
    
    try {
        console.log('📡 Sending request to /api/replay...');
        const response = await fetch('/api/replay', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                exchange,
                from_date: fromDate,
                to_date: toDate,
                symbols,
                limit
            })
        });
        
        console.log('📥 Response status:', response.status);
        const data = await response.json();
        console.log('📦 Response data:', data);
        
        if (data.success) {
            console.log('✅ Success! Retrieved', data.count, 'messages');
            statusDiv.className = 'status success';
            statusDiv.textContent = `✓ Successfully retrieved ${data.count} messages`;
            
            if (data.count === 0) {
                console.warn('⚠️ No data returned');
                resultsDiv.innerHTML = `
                    <div class="empty-state">
                        <p>No data found for the selected parameters.</p>
                        <p style="margin-top: 10px; font-size: 14px;">
                            Note: Free tier only has access to the first day of each month.
                        </p>
                    </div>
                `;
            } else {
                console.log('📊 Rendering', data.count, 'messages');
                resultsDiv.innerHTML = data.data.map((item, index) => `
                    <div class="message">
                        <div class="message-header">
                            Message #${index + 1} - ${item.timestamp}
                        </div>
                        <div class="message-data">${JSON.stringify(item.data, null, 2)}</div>
                    </div>
                `).join('');
            }
        } else {
            console.error('❌ API returned error:', data.error);
            statusDiv.className = 'status error';
            statusDiv.textContent = `✗ Error: ${data.error}`;
        }
    } catch (error) {
        console.error('❌ Fetch error:', error);
        statusDiv.className = 'status error';
        statusDiv.textContent = `✗ Error: ${error.message}`;
    } finally {
        fetchBtn.disabled = false;
    }
}

// Auto-fetch on page load
window.addEventListener('load', () => {
    fetchData();
});
