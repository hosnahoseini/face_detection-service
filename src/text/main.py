import uvicorn
from fastapi import APIRouter, FastAPI, Request

PREFIX = "/text/v1"

app = FastAPI(title = "Text", docs_url=PREFIX + "/docs", openapi_url= PREFIX + '/openapi.json' )

@app.get(PREFIX + "/count_word/{text:str}")
def read_main(text):
    return len(text.split(" "))

if __name__ == '__main__':
    uvicorn.run("src.text.main:app",host='0.0.0.0', port=5000, reload=True, debug=True)