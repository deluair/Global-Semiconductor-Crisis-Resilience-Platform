import multiprocessing
import subprocess
import sys
import time
from pathlib import Path

import uvicorn


def run_backend():
    """Run the FastAPI backend server."""
    uvicorn.run(
        "semiconductor_resilience.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )


def run_frontend():
    """Run the Dash frontend server."""
    subprocess.run(
        [sys.executable, str(Path("semiconductor_resilience/web/app.py"))],
        check=True,
    )


if __name__ == "__main__":
    # Create processes for backend and frontend
    backend_process = multiprocessing.Process(target=run_backend)
    frontend_process = multiprocessing.Process(target=run_frontend)
    
    try:
        # Start the backend server
        print("Starting backend server...")
        backend_process.start()
        
        # Wait for backend to start
        time.sleep(2)
        
        # Start the frontend server
        print("Starting frontend server...")
        frontend_process.start()
        
        # Wait for both processes to complete
        backend_process.join()
        frontend_process.join()
        
    except KeyboardInterrupt:
        print("\nShutting down servers...")
        backend_process.terminate()
        frontend_process.terminate()
        backend_process.join()
        frontend_process.join()
        print("Servers shut down successfully.") 