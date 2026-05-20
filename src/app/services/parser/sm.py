from playwright.async_api import async_playwright, Browser, Playwright, Locator
from playwright_stealth import Stealth
from numpy.random import randint

from src.app.core.logger import Logger

logger = Logger.get_logger(__name__)

class SiteManager:
    def __init__(self, headless: bool = True, args: list = None):
        self.headless = headless
        self.args = args or ["--disable-blink-features=AutomationControlled"]
        self.browser = None
        self.page = None
        
    async def init(self):
        self._pw = await Stealth().use_async(async_playwright()).start()
        self.browser = await self._create_browser(self._pw)
        self.page = await self.browser.new_page()
        await self._warm_up_site()
    
    async def get_page(self, url: str, referer: str = None) -> str:
        await self._fetch_url(url, wait=randint(3200, 5200), referer=referer)
        content = await self.page.content()
        
        return content

    async def scroll_page(self, id_element: int | str) -> Locator:
        locator = self.page.locator(f"#i{str(id_element)}")
        await locator.wait_for()
        await locator.scroll_into_view_if_needed()
    
    async def _warm_up_site(self) -> None:
        referer = "https://yandex.ru/search/?text=авито&clid=10472851-71&banerid=6400000000%3A677e7173a4e750a02cde2b54&win=706&lr=11049"
        await self._fetch_url("https://www.avito.ru", wait=randint(2100, 3200), referer=referer)
    
    async def _create_browser(self, p: Playwright) -> Browser:
        return await p.chromium.launch(
                    headless=self.headless,
                    args=self.args,
            )
    
    async def _fetch_url(
        self, url: str,
        timeout: int = 30_000,
        retry: int = 3,
        wait: int = 0,
        referer: str = None,
    ) -> int:
        last_error = None
        for count in range(retry):
            try:
                status = await self.page.goto(url, timeout=timeout, wait_until="domcontentloaded", referer=referer)
                status = status.status
                logger.info("Fetch", url=url, attempt=count, status_code=status, wait=wait, referer=referer)
                if status == 429 or status == 302:
                    await self.page.wait_for_timeout(360_000)
                if status != 200:
                    continue
                await self.page.wait_for_timeout(wait)
                return status
            except Exception as e:
                logger.info(f"Retry", url=url, attempt=count, total=retry, error=str(e))
                last_error = e
        logger.error(f"Error ferch url", url=url, attempt=retry, total=retry, error=str(last_error))