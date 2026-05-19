from typing import List, Dict, Any
from playwright.async_api import Page, Browser, expect
from app.adapters.base import BaseAdapter
import asyncio

class IndeedAdapter(BaseAdapter):
    """
    Playwright automation adapter for Indeed.com.
    Note: Indeed has strict anti-bot measures. Use with caution and consider proxy rotation.
    """

    def __init__(self, browser: Browser):
        super().__init__("Indeed", browser)

    async def authenticate(self, page: Page, credentials: Dict[str, str]) -> bool:
        """Log into Indeed."""
        try:
            await page.goto("https://secure.indeed.com/account/login")
            await page.fill("input[name='__email']", credentials["email"])
            await page.click("button[type='submit']")
            
            # Wait for password field (or OTP fallback)
            # This is highly variable depending on Indeed's security flow
            await page.wait_for_selector("input[name='__password']", timeout=5000)
            await page.fill("input[name='__password']", credentials["password"])
            await page.click("button[type='submit']")
            
            # Verify login success by checking for user avatar or specific redirect
            await page.wait_for_url("**/", timeout=10000)
            return True
        except Exception as e:
            await self.fallback_mode(page, f"Authentication failed or blocked: {e}")
            return False

    async def discover_jobs(self, page: Page, search_params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Search Indeed for jobs matching preferences."""
        jobs_found = []
        try:
            query = search_params.get("q", "software engineer")
            location = search_params.get("l", "remote")
            
            await page.goto(f"https://www.indeed.com/jobs?q={query}&l={location}")
            await page.wait_for_selector("td.resultContent", timeout=10000)
            
            # Extract basic job cards from the first page
            job_cards = await page.query_selector_all("td.resultContent")
            for card in job_cards[:5]: # Limit to top 5 for demo
                title_elem = await card.query_selector("h2.jobTitle span[title]")
                company_elem = await card.query_selector("span[data-testid='company-name']")
                link_elem = await card.query_selector("h2.jobTitle a")
                
                title = await title_elem.inner_text() if title_elem else "Unknown"
                company = await company_elem.inner_text() if company_elem else "Unknown"
                url_path = await link_elem.get_attribute("href") if link_elem else ""
                
                if url_path:
                    jobs_found.append({
                        "title": title,
                        "company": company,
                        "url": f"https://www.indeed.com{url_path}"
                    })
                    
            return jobs_found
        except Exception as e:
            await self.fallback_mode(page, f"Job discovery blocked: {e}")
            return []

    async def extract_job_details(self, page: Page, job_url: str) -> Dict[str, Any]:
        """Visit specific job URL and scrape full description."""
        try:
            await page.goto(job_url)
            await page.wait_for_selector("div#jobDescriptionText")
            description = await page.inner_text("div#jobDescriptionText")
            
            return {
                "url": job_url,
                "description": description
            }
        except Exception as e:
            await self.fallback_mode(page, f"Job details extraction blocked: {e}")
            return {}

    async def autofill_application(self, page: Page, profile: Dict[str, Any]) -> bool:
        """Autofill 'Indeed Apply' form."""
        # Indeed Apply flows are extremely complex and dynamic (multistep forms)
        # This requires an advanced state machine to navigate. 
        # For safety and demo purposes, we trigger fallback mode immediately to allow user manual assist.
        await self.fallback_mode(page, "Complex dynamic application form detected. Pausing for user manual review.")
        return False

    async def submit_application(self, page: Page) -> bool:
        # Stub
        return False
        
    async def fallback_mode(self, page: Page, reason: str):
        print(f"[{self.name}] FALLBACK MODE TRIGGERED: {reason}")
        # Here we would pause the page and notify the websocket
        await asyncio.sleep(60) # Pause for 1 minute for manual intervention
