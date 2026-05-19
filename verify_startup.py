import requests
import time

def verify_services():
    print("Waiting for services to start up...")
    
    backend_url = "http://localhost:8000/health"
    frontend_url = "http://localhost:3000"
    
    backend_up = False
    frontend_up = False
    
    for _ in range(60): # wait up to 120 seconds
        if not backend_up:
            try:
                res = requests.get(backend_url)
                if res.status_code == 200:
                    print("Backend is UP and accessible at http://localhost:8000/docs")
                    backend_up = True
            except:
                pass
                
        if not frontend_up:
            try:
                res = requests.get(frontend_url)
                if res.status_code == 200:
                    print("Frontend is UP and accessible at http://localhost:3000")
                    frontend_up = True
            except:
                pass
                
        if backend_up and frontend_up:
            print("All services are running successfully!")
            return True
            
        time.sleep(2)
        
    print("Error: Services did not start within the expected time.")
    print(f"Backend status: {'UP' if backend_up else 'DOWN'}")
    print(f"Frontend status: {'UP' if frontend_up else 'DOWN'}")
    return False

if __name__ == "__main__":
    verify_services()
