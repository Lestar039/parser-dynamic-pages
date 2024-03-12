import uvicorn
from fastapi import FastAPI

from selenium_client import get_text_from_url

app = FastAPI()


@app.get("/get_text")
async def get_text(url: str):
    result = get_text_from_url(url=url)
    if result:
        return {"message": result}
    return {"error": "something went wrong..."}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=3000, reload=True)
