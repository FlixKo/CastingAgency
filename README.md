# CastingAgency
Udacity Full Stack Developer Course Final Project

This API lets Casting Assistants, Casting Directors, Executive Producers read, add, change and delete movies and actors.

# Heroku
The App is deployed on Heroku on the following link:
https://casting-agency-200501.herokuapp.com/

# Authentication
This app uses Auth0 as Authentication provider.
- Application Name: CastingAgency
- Application Domain: udacity.eu.auth0.com
- ClientID: E7jCXUVwJ5I8s1RcWjrqLHDyjraKq22C
- LoginLink: https://udacity.eu.auth0.com/authorize?audience=casting&response_type=token&client_id=E7jCXUVwJ5I8s1RcWjrqLHDyjraKq22C&redirect_uri=https://casting-agency-200501.herokuapp.com/login-result

The Logininformation to update the JWT are as follows:
- castingdirector@test.de Test1234
- castingdirector@test.de Test1234
- executive@test.de Test1234

# API:
## GET /movies
- list available movies
- curl -X GET http://127.0.0.1:5000/movies
### Response
```
 {"movies":[{"id":1,"releaseDate":"Fri, 01 May 2020 17:03:59 GMT","title":"Updated Title"}],"success":true,"total_movies":1}
```


## GET /actors
- list available actors
- curl -X GET http://127.0.0.1:5000/actors
### Response
```
 {"actors":[{"age":42,"gender":"M","id":3,"name":"Hugo"}],"success":true,"total_actors":1}
```

## POST /movies
- create a new movie

## DELTE /movies/<movie_id>
- deletes the movie with corresponding id

## PATCH /movies/<movie_id>
- changes the movie with the corresponding id


# Roles:
## Casting Assistant
- Can view actors and movies

## Casting Director
- All permissions a Casting Assistant has and…
- Add or delete an actor from the database
- Modify actors or movies

## Executive Producer
- All permissions a Casting Director has and…
- Add or delete a movie from the database