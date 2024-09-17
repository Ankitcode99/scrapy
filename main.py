from fastapi import Depends, FastAPI
import Database
from middleware.auth import verify_token
from models.Product import Product
from dotenv import load_dotenv
import os
load_dotenv()
app = FastAPI(title="BE Assignment ft. Atlys",
    description="This is a description of my API.",
    version="1.0.0")
db_client = Database.DatabaseClient()

@app.get("/health-check")
async def health_check():
    response = db_client.insert(product=Product(product_title='A Sample Product', product_price=120.00, path_to_image='sample_path'))
    print('SAVE TO DB RESPONSE - ',response)
    return {"message": "Scrapy Backend is UP!"}

@app.get("/single")
async def all_key(product_name:str=""):
    response = db_client.fetchOne(product_name)
    print("Fetch One response - ", response)
    return {"Response": response}


@app.get('/static-token')
async def get_scrapy_token():
    return {"token":"static_scrapy_token"}

@app.get('/protected-route')
async def protected_route(token: str = Depends(verify_token)):
    return {"msg":"Accessed protected route"}