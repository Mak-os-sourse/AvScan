import re
from numpy.random import randint
import structlog

from parser.types_parser import Product
from parser.parser import Parser
from parser.sm import SiteManager
from core.logger import Logger

url = "https://www.avito.ru/shahty/igry_pristavki_i_programmy/igrovye_pristavki_i_aksessuary-ASgBAgICAUSSAsoJ?q=meta+quest+3"

logger = Logger.get_logger(__name__)

class Scraper:
    def __init__(self):
        self.parser = Parser()
        self.sm = SiteManager(headless=True)
    
    def scrape(self, url: str):
        result = {}
        count = 1
        count_pages = 1
        try:
            while True:
                url = self._format_url(url, page_count=count, local_priority=1)
                html = self.sm.get_page(url)
                products = self.parser.parse_products(html)
                
                if not products:
                    return result
                    
                self._simulate_get_product(products)
                result.update(products)
                
                if count == 1:
                    count_pages = self.parser.get_count_pages(html)
                if count == count_pages:
                    return result
                count += 1
        except Exception as e:
            logger.error("Error scrape", url=url, error=str(e))
    
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
    
    def _simulate_get_product(self, products: dict[int, Product]) -> None:
        index = randint(0, len(products) - 1)
        site = list(products.values())[index]
        self.sm.scroll_page(site.id)
        self.sm.get_page(site.url)

scraper = Scraper()
print(scraper.scrape(url))