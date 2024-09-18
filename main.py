import asyncio
from datetime import datetime
from typing import Optional
from fastapi import Depends, FastAPI, HTTPException
import Database
from middleware.auth import verify_token
from models.Product import Product
from dotenv import load_dotenv
import os

from utils.productUtils import start_scraping_pages
load_dotenv()
app = FastAPI(title="BE Assignment ft. Atlys",
    description="This is a description of my API.",
    version="1.0.0")

db_client = Database.DatabaseClient()

@app.on_event("shutdown")
def shutdown_event():
    db_client.close()

@app.get("/health-check")
async def health_check():
    return {"message": "Scrapy Backend is UP!"}

# @app.get("/single")
# async def all_key(product_name:str=""):
#     response = db_client.fetchOne(product_name)
#     print("1. Fetch One response - ", response, response["product_price"], type(response["product_price"]),"\n\n")
#     if "_id" in response:
#         response["_id"] = str(response["_id"])

#     # response.pop("_id", None)
#     print("2. Fetch One response - ", response, type(response),"\n\n")
#     return {"data": response}


@app.get('/static-token')
async def get_scrapy_token():
    return {"token":"static_scrapy_token"}

@app.post('/scrape-data')
async def protected_route(token: str = Depends(verify_token), pages: int = 1, proxy: Optional[str] = None, retry_after:Optional[int]=5):
    if(pages<1):
        raise HTTPException(status_code=400, detail='Pages should be more than or equal to 1')
    
    start_time = datetime.now()
    page_numbers = [i for i in range(1,pages+1)];
    result = await start_scraping_pages(page_numbers, proxy, retry_after)
    print("Scrape result : ",result)
    
    return {"scrape_result":result,"response_time": f"{(datetime.now()-start_time).total_seconds()} seconds"}