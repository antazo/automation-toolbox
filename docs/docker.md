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

# Starting multiple containers

As a programmer, you’ve been asked to set up a WordPress blog. You know WordPress requires a database to store its content. You create and start two containers, wordpress and db, using the following command:

```
$ docker run -d --name db --restart always \
    -v db_data:/var/lib/mysql -p 3306 -p 33060 \
    -e MYSQL_ROOT_PASSWORD=somewordpress \
    -e MYSQL_DATABASE=wordpress \
    -e MYSQL_USER=wordpress \
    -e MYSQL_PASSWORD=wordpress \
    mariadb:10
```

This command starts the mariadb database, determines a storage volume, and sets the initial password for the WordPress user. It declares two network ports open to other containers, but it is not shown on the host machine.

Now, start the WordPress container using the following command:

```
$ docker run -d --name wordpress --restart always \
    -v wp_data:/var/www/html -p 80:80 \
    -e WORDPRESS_DB_HOST=db \
    -e WORDPRESS_DB_USER=wordpress \
    -e WORDPRESS_DB_PASSWORD=wordpress \
    -e WORDPRESS_DB_NAME=wordpress \
    wordpress:latest
```

Note: The environment variable WORDPRESS_DB_HOST is set to db on the third line. This line of code is needed to refer to another container. Docker provides domain name system (DNS) services that allow containers to find each other by their name.

# Networking with multiple containers

Docker allows you to create private networks for a container or groups of containers. These private containers are able to discover each other, but no other networks will be able to find the private containers you’ve started. Let’s look at an example: modifying the wordpress and db containers by putting them on a private network.

First, stop and delete both containers:

```
$ docker stop wordpress && docker rm wordpress
$ docker stop db && docker rm db
```

Then, create a private network for both containers to use:

```
$ docker network create myblog
0f6abeb9d85a7063298cd70082ac5e5a2f0d1624bae06619fd14dbaa0942b0e2
```

Once the containers are on private networks, restart them with the additional option -network myblog. This appears on the second to last line for both container commands.

```
$ docker run -d --name db --restart always \
    -v db_data:/var/lib/mysql -p 3306 -p 33060 \
    -e MYSQL_ROOT_PASSWORD=somewordpress \
    -e MYSQL_DATABASE=wordpress \
    -e MYSQL_USER=wordpress \
    -e MYSQL_PASSWORD=wordpress \
    --network myblog \
    mariadb:10
```

```
$ docker run -d --name wordpress --restart always \
    -v wp_data:/var/www/html -p 80:80 \
    -e WORDPRESS_DB_HOST=db \
    -e WORDPRESS_DB_USER=wordpress \
    -e WORDPRESS_DB_PASSWORD=wordpress \
    -e WORDPRESS_DB_NAME=wordpress \
    --network myblog \
    wordpress:latest
```

It’s good practice to verify that containers on other networks can’t access the private networks you created. To check this, start a new container and attempt to find the private containers you created.

```
$ docker run -it debian:latest 
root@7240f1e3ddab:/# ping db.myblog
ping: db.myblog: Name or service not known
```

# Docker Compose

The Compose file communicates with Docker and identifies the containers you need and how you should configure them. The containers in a Compose file are called services. Let’s look at how you can use Compose to recreate the private networks from the  wordpress and db example. Run the following on your machine.

1. Create an empty folder and save the file below as docker-compose.yml.

```
version: '3.3'
services:
  db:
    image: mariadb:10
    volumes:
      - db_data:/var/lib/mysql
    restart: always
    environment:
      - MYSQL_ROOT_PASSWORD=somewordpress
      - MYSQL_DATABASE=wordpress
      - MYSQL_USER=wordpress
      - MYSQL_PASSWORD=wordpress
    networks:
      - myblog
    expose:
      - 3306
      - 33060
  wordpress:
    image: wordpress:latest
    volumes:
      - wp_data:/var/www/html
    ports:
      - 80:80
    networks:
      - myblog
    restart: always
    environment:
      - WORDPRESS_DB_HOST=db
      - WORDPRESS_DB_USER=wordpress
      - WORDPRESS_DB_PASSWORD=wordpress
      - WORDPRESS_DB_NAME=wordpress
volumes:
  db_data:
  wp_data:
networks:
  myblog:
```

2. Run the command docker compose up. This pulls up the images, creates two empty data volumes, and starts both services. The output from both services will intermingle on your screen.

Pro tip: You can also express any option you pass to the docker run command as YAML in a Compose file.

# Kubernetes (or K8s) on Docker Desktop

The Kubernetes server runs as containers and installs the 

```
/usr/local/bin/kubect1
```

 command on your machine.
