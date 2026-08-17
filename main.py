from fastapi import FastAPI, Query
from router import route_request

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur ILMR - Intelligent LLM Model Router"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/route")
def route(query: str = Query(...)):
    return route_request(query)