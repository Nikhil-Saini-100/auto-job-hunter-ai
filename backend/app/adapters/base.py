from abc import ABC, abstractmethod
from typing import List, Dict, Any
from playwright.async_api import Page, Browser

class BaseAdapter(ABC):
    """
    Abstract Base Class for all Job Board automation adapters (Indeed, Internshala, etc.)
    """

    def __init__(self, name: str, browser: Browser):
        self.name = name
        self.browser = browser

    @abstractmethod
    async def authenticate(self, page: Page, credentials: Dict[str, str]) -> bool:
        """
        Log into the job board platform. Must handle OTP/CAPTCHA fallback if needed.
        """
        pass

    @abstractmethod
    async def discover_jobs(self, page: Page, search_params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Search for jobs based on preferences and return a list of raw job dictionaries.
        """
        pass

    @abstractmethod
    async def extract_job_details(self, page: Page, job_url: str) -> Dict[str, Any]:
        """
        Visit a specific job URL and extract full description, salary, requirements.
        """
        pass

    @abstractmethod
    async def autofill_application(self, page: Page, profile: Dict[str, Any]) -> bool:
        """
        Navigate the application form and autofill details. Returns True if successful.
        """
        pass

    @abstractmethod
    async def submit_application(self, page: Page) -> bool:
        """
        Finalize and submit the application. Should pause in fallback mode if unsafe.
        """
        pass
        
    @abstractmethod
    async def fallback_mode(self, page: Page, reason: str):
        """
        Called when automation is blocked (CAPTCHA, complex form). Pauses and alerts the user.
        """
        print(f"[{self.name}] Automation blocked. Reason: {reason}. Switching to manual assist mode.")
        # In a real implementation, this would send a WebSocket or DB notification to the frontend.
