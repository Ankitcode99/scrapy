# scrapy
Website scraping with fastApi 

## Prerequisites
Before setting up the project locally, ensure that you have the following installed:
1. Python (version 3.7 or higher)
2. pip (Python package installer)

## Local Setup
Follow these steps to set up the project on your local machine:
1. Clone the repository:
```
git clone https://github.com/Ankitcode99/scrapy.git
```

2. Navigate to the project directory:
```
cd scrapy
```
3. Install dependencies from requirements.txt:
```
pip install -r requirements.txt
```

4. Run the FastAPI application:
```
uvicorn main:app --reload
```
- main corresponds to the Python file (without the .py extension) that contains the FastAPI instance.
- `app` is the FastAPI instance defined in the `main` file.
- `--reload` enables automatic reloading of the server when changes are made to the code.

# Access the API:
- Swagger UI: Open your web browser and visit http://localhost:8000/docs. You will see the interactive Swagger UI documentation.
- Redoc: Open your web browser and visit http://localhost:8000/redoc. You will see the Redoc documentation.