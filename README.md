# Test API for social network
This is a simple RESTful API for a social networking application. It's written with FastAPI and SQLite3 as DBMS.
## List of realised functions:
### Users:
 - Create user (a.k.a. sign-in) `POST: /users/`
 - View a list of users `GET: /users/?limit={int}&offset={int}`
 - Delete user `DELETE: /users/{id: int}`
 - Login `POST: /users/login`
>Authentification and autherization made via JWT

### Posts:
> Autentification is required

- Create post `POST: /posts/`
- Edit your post `PUT: /posts/edit?post_id={int}` (Only author of the post can edit it)
- Delete your post `DELETE: /posts/{post_id: int}` (Only author of the post can delete it)
- React to post (a.k.a. like or dislike it) `PUT: /posts/react?post_id={int}`
- View scope of posts `GET: /posts/?limit={int}&offset={int}`
- View post by it id `GET: /posts/{post_id: int}`

## Requirements

| Library | Version |
| :------- | :------- |
|FastAPI|0.89.0|
|AuthLib|1.2.0|
|SQLAlchemy|1.4.46|
|SQLite|3.0|
|Pydantic|1.10.4|
|Passlib|1.7.4|

## Deployment
> uvicorn 0.20.0 version

- Create _app/.env_ file
- In that file create two variables:
- - JWT_SECRET_KEY
- - JWT_REFRESH_SECRET_KEY
- (and come up with some values)
- In cmd or terminal write
```sh
...
cd webtronic_api
uvicorn app.webtronic:app 
```

##### Documentation

FastAPI provides auto-generated doc which you can find at  _host/docs_

Verify the deployment by navigating to your server address in
your preferred browser.

```sh
127.0.0.1:8000/ # main page
127.0.0.1:8000/docs # documentation page
```
