# ImageHub

This is the API for an Image Repository service.

**ImageHub - The place where your images live**


# Installation and Running

This application is built using FastAPI and Python.

It can be run with or without Docker. A relatively recent version of Docker is required.

## Installation Steps without Docker
1. Install required dependencies using `pip3 install -r requirements.txt`.
2. Next, run the server from the root directory using `uvicorn`:
```sh
uvicorn app.main:app --port 3000
```

## Installation Steps with Docker (Recommended)
1. Docker Compose can be used to run the application using `docker-compose up`. Alternatively, the Docker image can be manually built and run using the given `Dockerfile`. 
2. If the latter approach is chosen, a named volume pointing to `/usr/src/app/app/store` should be assigned. 
3. The number of Workers per core, Maximum Workers, and the Port can be given as args to Docker, or can be set as environment variables in the Compose File.

## Running
1. The application starts listening on the provided port.
2. Any API Client can be used to test the endpoints.
3. Alternatively, OpenAPI Swagger UI can be used for testing the functionality of the application (recommended).
4. Open `/docs` url on the browser (Eg: `localhost:3000/docs`) to view the Swagger UI for the application. It should list the schemas and expected responses for each endpoint.
5. Some routes, such as image routes are protected by authentication. They can be used after signing up and then logging in.


# Testing

## Without Docker
To test the application without Docker, from the root directory, run `pytest`.

If import errors occur, please try running `python3 -m pytest` from the root directory.

## With Docker
To test the application with Docker, please run `docker-compose run tests`