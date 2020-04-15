# User Authentication and text saving api

The API is built by using FASTapi framework, This api uses is OAuth2 Authenticationprotocol,OAuth2 is a specification that defines several ways to handle authentication and authorization.
For login api uses "JSON Web Tokens" ie JWT and hashin password for security the token

# Installing

Clone the repository and then run the following command to install all the libraries.

```
    $ pip install -r requirements.txt
```

Or we can intall all libraries one by one by using the below command for windows operating system. 

firstly install fastapi
```
    $ pip intall fastapi
```
install uvicorn to run the fastapi application

```
    $ pip install uvicorn
```
install jwt for python 
```
  $ pip install pyjwt
```

install pymongo

```
    $ pip install pymongo
```
# Getting Started

To run the API in local machine run the following command

```
    $ uvicorn main:app --reload
```
The application will run on http://127.0.0.1:8000/

Now to test the API open a API testing tool such as postman

In postman send a json in a post request to http://127.0.0.1:8000/signup/ url
The formate of json should be
```
{
    "full_name": string,
    "username": string,
    "email": email_string,
    "password": string,
}
```
The responce will be a json describing the user in the same json formate as above that means the signup is successfully executed

Now to login send a Basic Auth using postman in Authentication section

The user will be redirected to http://127.0.0.1:8000/users/me/ url







