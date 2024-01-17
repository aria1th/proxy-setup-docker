import json
from fastapi import FastAPI
import uvicorn
import requests
from pydantic import BaseModel
# auth  
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import Depends, Response, status, Form
import secrets
from fastapi.exceptions import HTTPException
import logging


security = HTTPBasic()

auth_dict = {
    "user": "user",
    "password": "password_notdefault"
}

def check_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    """
    Check credentials
    """
    correct_username = secrets.compare_digest(credentials.username, auth_dict["user"])
    correct_password = secrets.compare_digest(credentials.password, auth_dict["password"])
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

class ModelResponse(BaseModel):
    """
    Response content from url
    """
    response: str
    success: bool = True

app = FastAPI()

@app.get("/")
def read_root():
    """
    curl +x http://127.0.0.1:8000/
    """
    logging.info("GET /")
    return {"success": True}

@app.get("/get_response", response_model=ModelResponse, dependencies=[Depends(check_credentials)])
def get_response(url):
    """
    Get response from url.
    Use curl +x http://127.0.0.1:8000/get_response?url=<url>
    """
    r = requests.get(url)
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        logging.info(f"GET {url} returned {r.status_code}")
        return ModelResponse(response=str(e), success=False)
    logging.info(f"GET {url} returned {r.status_code}")
    return ModelResponse(response=r.text, success=True)

@app.post("/post_response", response_model=ModelResponse, dependencies=[Depends(check_credentials)])
def post_response(url : str = Form(...), args_json : str = Form(...)):
    """
    Post response to url.
    Use curl +x http://127.0.0.1:8000/post_response?url=<url>
    """
    args = json.loads(args_json)
    data = args.get("data", {})
    headers = args.get("headers", {})
    r = requests.post(url, data=json.dumps(data), headers=headers)
    try:
        r.raise_for_status()
        return ModelResponse(response=r.text, success=True)
    except requests.exceptions.HTTPError as e:
        logging.info(f"POST {url} returned {r.status_code}")
        return ModelResponse(response=f"Response returned {r.status_code}, {e}", success=False)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--log-level", type=str, default="info")
    parser.add_argument("--log-file", type=str, default="proxy.log")
    parser.add_argument("--auth", type=str, default="user:password_notdefault")
    args = parser.parse_args()
    auth_dict["user"], auth_dict["password"] = args.auth.split(":")
    logging_level = args.log_level.upper()
    level = logging.getLevelName(logging_level)
    logging.basicConfig(filename=args.log_file, level=level, format='%(asctime)s %(levelname)s %(message)s')
    # debug for more info if needed

    uvicorn.run(app, host=args.host, port=args.port) #starts local server at port 8000
