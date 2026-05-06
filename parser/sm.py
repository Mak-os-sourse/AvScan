from playwright.sync_api import sync_playwright, Browser, Playwright, Locator
from playwright_stealth import Stealth
from numpy.random import randint

from core.logger import Logger

logger = Logger.get_logger(__name__)

class SiteManager:
    def __init__(self, headless: bool = True, args: list = None):
        self.headless = headless
        self.args = args or ["--disable-blink-features=AutomationControlled"]
        self._pw = Stealth().use_sync(sync_playwright()).start()
        self.browser = self._create_browser(self._pw)
        self.page = self.browser.new_page()
        self._warm_up_site()
    
    def get_page(self, url: str, referer: str = None) -> str:
        self._fetch_url(url, wait=randint(1200, 4200), referer=referer)
        content = self.page.content()
        
        return content

    def scroll_page(self, id_element: int | str) -> Locator:
        locator = self.page.locator(f"#i{str(id_element)}")
        locator.wait_for()
        locator.scroll_into_view_if_needed()
    
    def _warm_up_site(self) -> None:
        referer = "https://yandex.ru/search/?text=авито&clid=10472851-71&banerid=6400000000%3A677e7173a4e750a02cde2b54&win=706&lr=11049"
        self._fetch_url("https://www.avito.ru", wait=randint(2100, 3200), referer=referer)
    
    def _create_browser(self, p: Playwright) -> Browser:
        return p.chromium.launch(
                    headless=self.headless,
                    args=self.args,
            )
    
    def _fetch_url(
        self, url: str,
        timeout: int = 30_000,
        retry: int = 3,
        wait: int = 0,
        referer: str = None,
    ) -> int:
        last_error = None
        for count in range(retry):
            try:
                status = self.page.goto(url, timeout=timeout, wait_until="domcontentloaded", referer=referer).status
                logger.info("Fetch", url=url, attempt=count, status_code=status, wait=wait, referer=referer)
                if status != 200:
                    continue
                if status == 429 or status == 302:
                    self.page.wait_for_timeout(360_000)
                self.page.wait_for_timeout(wait)
                return status
            except Exception as e:
                logger.info(f"Retry", url=url, attempt=count, total=retry, error=str(e))
                last_error = e
        logger.error(f"Error ferch url", url=url, attempt=retry, total=retry, error=str(last_error))