import asyncio
from playwright.async_api import async_playwright

async def test_playwright():
    print("Testing Playwright inside Docker container...")
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto("https://example.com")
            title = await page.title()
            print(f"Successfully loaded example.com! Page Title: '{title}'")
            await browser.close()
            print("Playwright test PASSED successfully!")
            return True
    except Exception as e:
        print(f"Playwright test FAILED: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test_playwright())
