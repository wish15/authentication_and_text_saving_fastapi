# User Authentication and text saving api

The API is built by using FASTapi framework, This api uses is OAuth2 Authenticationprotocol,OAuth2 is a specification that defines several ways to handle authentication and authorization. For login api uses "JSON Web Tokens" ie JWT and hashing password using hashing algorithms for security.

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

# Sign Up

In postman send a json in a POST request to http://127.0.0.1:8000/signup/ url
The formate of json should be
```
{
    "full_name": string,
    "username": string,
    "email": email_string,
    "password": string,
}
```
![](images/signup.png)

The responce will be a json object which contains the ObjecId coresponding to the signed up user which get stored in mongodb user collection, that shows that the signup is successfully executed.
If the username or email already exists a error massage in the json formate will arrive.

![](images/emailexists.png)
![](images/usernameexists.png)

# Login

Now to login send a Basic Auth using postman in Authorization section


![](images/Basic_Auth-1.png)


Now put the username nd password in the Basic Auth Credentials form and sent a GET request to http://127.0.0.1:8000/login/ url 

![](images/login.png)

If the credentials were correct the user will be redirected to http://127.0.0.1:8000/users/me/ url with a json response of details of user

if credetials were wrong an error massage will be displayed

![](images/incorrect_credentials.png)

# text saving 

to save a text user need to login first if not logged in an error massage will be displayed.

After login send the message in the jason by POST request to http://127.0.0.1:8000/users/me/sendmassage url in the following formate

```
{
    "massage": string
}
```
![](images/user_me_sendmassage.png)

If user is not loged in the erroe massage will be displayed.

![](images/validationerrormassage.png)


# Get all the texts of the logged in user

To get all the texts in the json formate send a GET request to http://127.0.0.1:8000/users/me/massages/ url

The response will be a json of all the massages stored by user.

![](images/user_me_massages.png)

# Get details of current logged in user

To get the details of current logged in user sen a GET request to http://127.0.0.1:8000/users/me url

A json respons will be sent with details of user if user in not logged in a error massage will get displayed.

![](images/user_me.png)








