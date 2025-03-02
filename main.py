from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello Pakistan"}


@app.get("/post")
async def post():
    return {"message": "Here is your post"}


#  with out validation of Schema Using body from fastapi params
@app.get("/createPost")
async def create_post(payload: dict = Body(...)):
    print(payload)
    return {"message": "post Created Successfully", "data": payload}
