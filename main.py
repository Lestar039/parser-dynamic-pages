import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.requests import Request

from selenium_client import get_text_from_url

app = FastAPI()


class UrlModel(BaseModel):
    url: str


@app.post("/get_text")
async def get_text(url: UrlModel):
    result = get_text_from_url(url=url.url)
    if result:
        return {"message": result}
    return {"error": "something went wrong..."}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=3000, reload=True)
