# How to build a Docker image (or Dockerfile)


```
# sudo docker run hello-world
```

A common process is to start with a base image such as Debian Linux or Python 3.10, install the libraries your application requires, then copy the application and any related files into the image. Let’s take a look at a simple Dockerfile for a Python application example:

```
FROM python:3.9
```

This line of code says that you’re starting from the Python 3.9 base image.

```
COPY *.py setup.cfg LICENSE README.md requirements.txt /app/
WORKDIR /app
```

This command says to copy all of the application’s files to a folder inside the container named /app and make it the current working directory.

```
RUN pip install -r requirements.txt
RUN python setup.py install
```

These two lines of code run the Python commands to install the libraries required by the app. When that step is complete, build and install the app inside the container.

```
EXPOSE 8000
CMD [ "/usr/local/bin/my-application" ]
```

This command tells Docker what executable should run when the container starts and that the container will listen for network connections on port 8000.

Pro tip: To build this image from the Dockerfile, use the command: docker build. If the build is successful, Docker outputs the ID of the new image, which you can then use to start a container.