# Running Flask-MVC PDF API in Google Colab

This notebook runs the Flask-MVC PDF Embed/Extract API directly in Colab and exposes it through ngrok.

## 1. Install Dependencies

```python
!pip install flask PyPDF2 flasgger pytest gunicorn pyngrok
```

## 2. Clone the Repository

```python
!git clone https://github.com/yahiaAlg/flask_mvc_api.git
%cd flask_mvc_api
```

## 3. Create or Update requirements.txt

```python
%%writefile requirements.txt
flask>=2.0.0
PyPDF2>=3.0.0
flasgger>=0.9.5
pytest>=7.0.0
gunicorn>=20.1.0
pyngrok>=5.1.0
```

## 4. Run the Flask App Using ngrok

```python
# Import necessary libraries
from pyngrok import ngrok
import subprocess
import time
import threading
import requests

# Start Flask application in a separate thread
def run_flask():
    subprocess.Popen(["python", "run.py"])

# Create and start the thread
flask_thread = threading.Thread(target=run_flask)
flask_thread.daemon = True
flask_thread.start()

# Wait for Flask to start
print("Starting Flask app...")
time.sleep(5)

# Test if Flask is running
try:
    requests.get("http://localhost:5000")
    print("Flask app is running!")
except:
    print("Flask app may not be running correctly. Continuing anyway...")

# Start ngrok tunnel
public_url = ngrok.connect(5000)
print(f"Public URL: {public_url}")

# Display access information
print("\n=== Flask-MVC PDF API Access Information ===")
print(f"Web Interface: {public_url}")
print(f"API Documentation: {public_url}/apidocs/")
print(f"Embed PDFs Endpoint: {public_url}/api/pdf/create_embedded_pdf")
print(f"Extract PDFs Endpoint: {public_url}/api/pdf/extract_embedded_pdf")
```

## 5. Keep the Notebook Running

```python
# This will keep the notebook running
# To stop, interrupt the kernel
import IPython
from IPython.display import display, HTML

display(HTML('<h3>Service is running. Click "Interrupt kernel" to stop.</h3>'))

# Keep the kernel busy but allow interruption
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopping the service...")
    ngrok.kill()
```

## 6. Stop the Service (Run separately)

```python
# Kill ngrok tunnels
ngrok.kill()
print("Service stopped")
```
