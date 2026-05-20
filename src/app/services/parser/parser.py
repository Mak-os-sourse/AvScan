import re
from bs4 import BeautifulSoup

from src.app.types.parser import Product

class Parser:
    def parse_products(self, html: str) -> dict[int, Product]:
        result = {}
            
        soup = BeautifulSoup(html, "lxml")
        for id_product, item in self._get_products(soup):
            result[id_product] = Product(
                id=id_product,
                name=self._get_name_product(item),
                price=self._get_price_product(item),
                description=self._get_description_product(item),
                image=self._get_image_product(item),
                url=self._get_url_product(item),
            )
        return result
    
    def get_count_pages(self, html: str) -> int:
        soup = BeautifulSoup(html, "lxml")
        
        pages = soup.find("ul", attrs={"data-marker": "pagination-button"})
        if pages is None:
            return 0
        list_pages = pages.find_all("li")
        if not list_pages:
            return 0
        return int(list_pages[-2].text)
        
    def _get_products(self, soup: BeautifulSoup) -> list[tuple[int, BeautifulSoup]]:
        div = soup.find("div", attrs={"data-marker": "catalog-serp"})
        if div is None:
            return []
        products = div.find_all("div", attrs={"data-marker": "item"})
        if not products:
            return []
        result = [(int(item["data-item-id"]), item) for item in products]
        return result

    def _get_description_product(self, soup: BeautifulSoup) -> str:
        items = soup.find("div", class_=re.compile(r"^iva-item-bottomBlock"))
        if items is None:
            return
        description = items.find("div", class_=re.compile(r"^iva-item-ivaItemRedesign"))
        if description is None:
            return None
        return description.find('p').text

    def _get_url_product(self, soup: BeautifulSoup) -> str:
        return "https://www.avito.ru" + soup.find("a", attrs={"data-marker": "item-title"})["href"]
    
    def _get_price_product(self, soup: BeautifulSoup) -> str:
        return soup.find("span", attrs={"data-marker": "item-price-value"}).text
    
    def _get_name_product(self, soup: BeautifulSoup) -> str:
        return soup.find("a", attrs={"data-marker": "item-title"}).text

    def _get_image_product(self, soup: BeautifulSoup) -> str | None:
        data = soup.find_all("img", class_="photo-slider-image-cD891")
        if data:
            return data[0]["src"]
