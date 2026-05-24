import re
from numpy.random import randint

from src.app.core.settings import settings
from src.app.exceptions.parser import ListProductError
from src.app.services.parser.sm import SiteManager
from src.app.services.parser.parser import Parser
from src.app.types.parser import Product
from src.app.core.logger import Logger

logger = Logger.get_logger(__name__)

class Scraper:
    def __init__(self, headless: bool):
        self.parser = Parser()
        self.sm = SiteManager(headless=headless)
    
    async def scrape(self, url: str) -> dict[int, Product]:
        if self.sm.browser is None:
            await self.sm.init()
        result = {}
        count = 1
        count_pages = 1
        try:
            while True:
                formatted_url  = self._format_url(url, page_count=count, local_priority=1)
                html = await self.sm.get_page(formatted_url)
                products = self.parser.parse_products(html)
                
                if not products and count == 1:
                    raise ListProductError()
                if not products:
                    return result
                
                await self._simulate_get_product(products)
                result.update(products)
                
                if count == 1:
                    count_pages = self.parser.get_count_pages(html)
                if count == count_pages:
                    return result
                count += 1
        except ListProductError:
            raise
        except Exception as e:
            logger.error("Error scrape", url=formatted_url , error=str(e))
    
    def _format_url(self, url: str, page_count: int = 1, local_priority: int = 1):
        priority = re.search(r"localPriority=\d+", url)
        count = re.search(r"p=\d+", url)
        
        if priority is not None:
            url = re.sub(r"localPriority=\d+", f"localPriority={local_priority}", url)
        else:
            url = self._replace_parm_url(url, f"localPriority={local_priority}")
            
        if count is not None:
            url = re.sub(r"p=\d+", f"p={page_count}", url)
        else:
            url = self._replace_parm_url(url, f"p={page_count}")
        return url
    
    def _replace_parm_url(self, url: str, param: str):
        if url[-1] == "?":
            url += f"{param}"
        elif url.find("?") == -1:
            url += f"?{param}"
        else:
            url += f"&{param}"
        return url
    
    async def _simulate_get_product(self, products: dict[int, Product]) -> None:
        len_list = len(products) - 1
        if len_list == 0:
            return
        index = randint(0, len_list)
        site = list(products.values())[index]
        await self.sm.scroll_page(site.id)
        await self.sm.get_page(site.url)

scraper = Scraper(settings.HEADLESS)