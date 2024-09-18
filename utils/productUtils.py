import asyncio
from typing import List, Optional

import aiohttp
from bs4 import BeautifulSoup

import Database
from models.Product import Product


def generate_id_from_product_title(product_title: str) -> str:
    return product_title.strip().lower().replace(' ','_')

async def scrape_page(page_number: int, proxy: Optional[str], retry_after:int=5) -> List[Product]:
    url = f"https://dentalstall.com/shop/page/{page_number}/"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, proxy=proxy) as response:
                response.raise_for_status()
                soup = BeautifulSoup(await response.text(), 'html.parser')
                product_list = []
                
                product_items = soup.find_all('li', class_='type-product')
                
                for product_item in product_items:
                    # Extract image data
                    image_tag = product_item.find('img', class_='attachment-woocommerce_thumbnail')
                    image_src = image_tag['data-lazy-src'] if image_tag else None 
                    image_alt = image_tag['alt'] if image_tag else None
                    # Extract price data
                    price_tag = product_item.find('span', class_='woocommerce-Price-amount')
                    price_text = price_tag.text.strip() if price_tag else None
                    price = float(price_text.replace('₹', '')) if price_text else 0
                    
                    product_list.append({
                        'path_to_image': image_src,
                        'product_title': image_alt,
                        'product_price': price
                    })
                
                return product_list
        except Exception as e:
            print(f"Error scraping page {page_number}: {e}")
            await asyncio.sleep(retry_after)  # Retry after 5 seconds on failure
            return []  # Return an empty list on error

async def update_db_values(products: List[Product]) -> int :
    update_count = 0
    # db_client = 
    for product in products:
        old_product_details = Database.DatabaseClient().fetchOne(product["product_title"])
        if old_product_details is None:
            Database.DatabaseClient().insert(product=Product(product_price=product["product_price"], product_title=product["product_title"], path_to_image=product["path_to_image"]))
            pass
        else: 
            old_product_price = old_product_details["product_price"]
            if(old_product_price != product["product_price"]):
                if product["product_title"] != "Anabond Blu-Bite - Dentalstall India":
                    print(f"Price of \"{product['product_title']}\" changed from {old_product_price} to {product['product_price']}")
                    Database.DatabaseClient().update(product=Product(product_price=product["product_price"], product_title=product["product_title"], path_to_image=product["path_to_image"]))
                    update_count += 1


    return update_count
    


async def start_scraping_pages(pages: List[int], proxy: Optional[str] = None, retry_after:int=5)->dict[str,int]:
    tasks = [scrape_page(page_number, proxy) for page_number in pages]
    
    results = await asyncio.gather(*tasks)

    scraped_count = sum(len(products) for products in results)

    print("Scraped count -", scraped_count)
    update_tasks = [update_db_values(products) for products in results]

    updated_results = await asyncio.gather(*update_tasks)
    
    updated_count = sum(updates for updates in updated_results)

    return {
        "scraped_count": scraped_count,
        "updated_count": updated_count
    }

