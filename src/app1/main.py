import uvicorn
from fastapi import APIRouter, FastAPI, Request
app = FastAPI(title = "Text")
PREFIX = "/text/v1"

@app.get(PREFIX + "/")
def read_main():
    return {"message": "Hello World"}
    
@app.get(PREFIX + "/count_word/{text:str}")
def read_main(text):
    return len(text.split(" "))



if __name__ == '__main__':
    uvicorn.run("src.app1.main:app",host='0.0.0.0', port=5000, reload=True, debug=True)