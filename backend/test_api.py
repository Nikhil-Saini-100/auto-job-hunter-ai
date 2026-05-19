import asyncio
import httpx
import os

API_URL = "http://localhost:8000/api/v1"
EMAIL = "test@example.com"
PASSWORD = "password123"

async def test_all_endpoints():
    print("--- Starting API Integration Tests ---")
    
    async with httpx.AsyncClient() as client:
        # 1. Login
        print("\n1. Testing Login...")
        response = await client.post(f"{API_URL}/auth/login", data={"username": EMAIL, "password": PASSWORD})
        if response.status_code != 200:
            print(f"Login failed: {response.text}")
            return
        
        token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        print("Login successful. Token acquired.")

        # 2. Get Profile
        print("\n2. Fetching Profile...")
        response = await client.get(f"{API_URL}/profile/me", headers=headers)
        print(f"Profile status: {response.status_code}")

        # 3. Upload Resume (Trigger AI Parser)
        print("\n3. Testing Resume Upload and AI Parsing...")
        resume_path = "uploads/resumes/sample_resume.docx"
        if not os.path.exists(resume_path):
            print("Sample resume not found. Run seed.py first.")
            return

        with open(resume_path, "rb") as f:
            files = {"file": ("sample_resume.docx", f, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
            response = await client.post(f"{API_URL}/profile/upload-resume", headers=headers, files=files, timeout=60.0)
            
        print(f"Upload status: {response.status_code}")
        if response.status_code == 200:
            profile = response.json()
            print("AI Parsed Resume Data successfully.")
        else:
            print(f"Upload failed: {response.text}")
            # If OPENAI_API_KEY is dummy, this will fail.

        # 4. Trigger Job Analysis
        # Assuming job_id=1 exists from seed.py
        print("\n4. Testing Job Analysis (Matching)...")
        response = await client.post(f"{API_URL}/jobs/analyze/1", headers=headers, timeout=60.0)
        print(f"Job Analysis status: {response.status_code}")
        if response.status_code == 200:
            print("Job matched successfully.")
        else:
            print(f"Analysis failed: {response.text}")

        # 5. Trigger Resume Tailoring
        print("\n5. Testing Resume Tailoring & Cover Letter Engine...")
        response = await client.post(f"{API_URL}/resume/tailor/1", headers=headers, timeout=60.0)
        print(f"Tailoring status: {response.status_code}")
        if response.status_code == 200:
            print("Tailoring successful.")
        else:
            print(f"Tailoring failed: {response.text}")

if __name__ == "__main__":
    asyncio.run(test_all_endpoints())
