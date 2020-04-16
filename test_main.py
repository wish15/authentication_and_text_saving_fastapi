from main import app
from fastapi import Form
from fastapi.testclient import TestClient
from requests.auth import HTTPBasicAuth
from fastapi.security import HTTPBasic, HTTPBasicCredentials
client=TestClient(app)
def test_root_url():
    response=client.get("/")
    assert response.status_code==200
    assert response.json()=={"msg":"Hello and wellcome plase goto /login to login"}

def test_login_with_correct_credentials():
    auth=HTTPBasicAuth(username="wishcode",password="vishal")
    response=client.get("/login",auth=auth)
    assert response.status_code==200
    assert response.json()=={
        "full_name":"Vishal",
        "username":"wishcode",
        "email":"vishal@gmail.com"
    } 

def test_login_with_wrong_credentils():
    response=client.get("/login",headers={"username":"hello","password":"word"})
    assert response.status_code==401
    assert response.headers["WWW-Authenticate"] == 'Basic'
    assert response.json()=={"detail":"Incorrect username or password"} or response.json()=={"detail":"Not authenticated"}
