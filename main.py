from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from datetime import datetime
import pytz  # Import pytz for timezone handling

app = FastAPI()

# Mount the static files directory to serve favicon.ico
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return "<h1>Welcome to the Timeserver API</h1><p>Use <a href='/time'>/time</a> to view the current time in UTC+1.</p>"

@app.get("/time", response_class=JSONResponse)
async def get_current_time():
    # Get current time in UTC+1 (West Africa Time)
    tz = pytz.timezone('Africa/Lagos')  # Updated to use WAT as per your preference
    current_time = datetime.now(tz)
    # Format the time as ISO 8601 string
    formatted_time = current_time.isoformat()

    # Return JSON response with the current time
    return JSONResponse(content={"current_time": formatted_time})

# Optionally, retain the HTML response if needed
@app.get("/time/html", response_class=HTMLResponse)
async def get_current_time_html():
    # Get current time in UTC+1
    tz = pytz.timezone('Africa/Lagos')  # Updated to use WAT as per your preference
    current_time = datetime.now(tz)
    # Format the time as ISO 8601 string
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S %Z")

    # HTML content with bold stylized font and JavaScript clock
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Current Time</title>
        <link rel="icon" href="/static/favicon.ico" type="image/x-icon">
        <style>
            body {{
                font-family: 'Arial', sans-serif;
                text-align: center;
                background-color: #f0f0f0;
                padding: 50px;
            }}
            .time-display {{
                font-size: 48px;
                font-weight: bold;
                color: #333;
                margin-top: 20px;
            }}
            .clock {{
                font-size: 36px;
                font-weight: bold;
                color: #007BFF;
                margin-top: 20px;
            }}
        </style>
    </head>
    <body>
        <h1>Current Time in WAT (UTC+1)</h1>
        <div class="time-display">{formatted_time}</div>

        <h2>Live Clock</h2>
        <div class="clock" id="clock"></div>

        <script>
            function updateClock() {{
                const now = new Date();
                const hours = String(now.getUTCHours() + 1).padStart(2, '0'); // Adjust for UTC+1
                const minutes = String(now.getUTCMinutes()).padStart(2, '0');
                const seconds = String(now.getUTCSeconds()).padStart(2, '0');
                const timeString = hours + ':' + minutes + ':' + seconds + ' UTC+1';
                document.getElementById('clock').textContent = timeString;
            }}
            setInterval(updateClock, 1000);
            updateClock();  // Initial call to display clock immediately
        </script>
    </body>
    </html>
    """
    
    return HTMLResponse(content=html_content)
