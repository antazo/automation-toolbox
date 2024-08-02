# Work with containers on GCP

## Overview

Docker is an open platform for developing, shipping, and running applications. With Docker, you can separate your applications from your infrastructure and treat your infrastructure like a managed application. Docker helps you ship code faster, test faster, deploy faster, and shorten the cycle between writing code and running code.

Docker does this by combining kernel containerization features with workflows and tooling that helps you manage and deploy your applications.

Docker containers can be directly used in Kubernetes, which allows them to be run in the Kubernetes Engine with ease. After learning the essentials of Docker, you will have the skillset to start developing Kubernetes and containerized applications.

What you'll learn
In this lab, you will learn how to do the following:

How to build, run, and debug Docker containers.
How to pull Docker images from Docker Hub and Google Artifact Registry.
How to push Docker images to Google Artifact Registry.

### Activate Cloud Shell

You can list the active account name with this command:
gcloud auth list

You can list the project ID with this command:
gcloud config list project

In Cloud Shell enter the following command to run a hello world container to get started:
docker run hello-world

Run the following command to take a look at the container image it pulled from Docker Hub:
docker images

### Task 1. Hello world

Run the container again:
docker run hello-world

Notice the second time you run this, the Docker daemon finds the image in your local registry and runs the container from that image. It doesn't have to pull the image from Docker Hub.

Finally, look at the running containers by running the following command:
docker ps

In order to see all containers, including ones that have finished executing, run docker ps -a:
docker ps -a

### Task 2. Build

Execute the following command to create and switch into a folder named test.
mkdir test && cd test

Create a Dockerfile:

```
cat > Dockerfile <<EOF
# Use an official Node runtime as the parent image
FROM node:lts

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Make the container's port 80 available to the outside world
EXPOSE 80

# Run app.js using node when the container launches
CMD ["node", "app.js"]
EOF
```

This file instructs the Docker daemon on how to build your image.

The initial line specifies the base parent image, which in this case is the official Docker image for node version long term support (lts).
In the second, you set the working (current) directory of the container.
In the third, you add the current directory's contents (indicated by the "." ) into the container.
Then expose the container's port so it can accept connections on that port and finally run the node command to start the application.

Run the following to create the node application:

```
cat > app.js <<EOF
const http = require('http');

const hostname = '0.0.0.0';
const port = 80;

const server = http.createServer((req, res) => {
    res.statusCode = 200;
    res.setHeader('Content-Type', 'text/plain');
    res.end('Hello World\n');
});

server.listen(port, hostname, () => {
    console.log('Server running at http://%s:%s/', hostname, port);
});

process.on('SIGINT', function() {
    console.log('Caught interrupt signal and will exit');
    process.exit();
});
EOF
```

This is a simple HTTP server that listens on port 80 and returns "Hello World".

Now build the image.

Note again the ".", which means current directory so you need to run this command from within the directory that has the Dockerfile:

```
docker build -t node-app:0.1 .
```

The -t is to name and tag an image with the name:tag syntax. The name of the image is node-app and the tag is 0.1. The tag is highly recommended when building Docker images. If you don't specify a tag, the tag will default to latest and it becomes more difficult to distinguish newer images from older ones. Also notice how each line in the Dockerfile above results in intermediate container layers as the image is built.

Now, run the following command to look at the images you built:
docker images

### Task 3. Run

Use this code to run containers based on the image you built:
docker run -p 4000:80 --name my-app node-app:0.1

The --name flag allows you to name the container if you like. The -p instructs Docker to map the host's port 4000 to the container's port 80. Now you can reach the server at http://localhost:4000. Without port mapping, you would not be able to reach the container at localhost.

Open another terminal (in Cloud Shell, click the + icon), and test the server:
curl http://localhost:4000

The container will run as long as the initial terminal is running. If you want the container to run in the background (not tied to the terminal's session), you need to specify the -d flag.

Close the initial terminal and then run the following command to stop and remove the container:
docker stop my-app && docker rm my-app

Now run the following command to start the container in the background:
docker run -p 4000:80 --name my-app -d node-app:0.1

docker ps

Notice the container is running in the output of docker ps. You can look at the logs by executing docker logs [container_id].
Note: You don't have to write the entire container ID, as long as the initial characters uniquely identify the container. For example, you can execute docker logs 17b if the container ID is 17bcaca6f....
docker logs [container_id]

Now modify the application.

In your Cloud Shell, open the test directory you created earlier in the lab:
cd test
Copied!
Edit app.js with a text editor of your choice (for example nano or vim) and replace "Hello World" with another string:

....
const server = http.createServer((req, res) => {
    res.statusCode = 200;
    res.setHeader('Content-Type', 'text/plain');
    res.end('Welcome to Cloud\n');
});
....

Build this new image and tag it with 0.2:
docker build -t node-app:0.2 .

Notice in Step 2 that you are using an existing cache layer. From Step 3 and on, the layers are modified because you made a change in app.js.

Run another container with the new image version. Notice how we map the host's port 8080 instead of 80. You can't use host port 4000 because it's already in use.
docker run -p 8080:80 --name my-app-2 -d node-app:0.2
docker ps

Test the containers:
curl http://localhost:8080

And now test the first container you made:
curl http://localhost:4000

### Task 4. Debug

Now that you're familiar with building and running containers, go over some debugging practices.

You can look at the logs of a container using docker logs [container_id]. If you want to follow the log's output as the container is running, use the -f option.
docker logs -f [container_id]

Sometimes you will want to start an interactive Bash session inside the running container.

You can use docker exec to do this. Open another terminal (in Cloud Shell, click the + icon) and enter the following command:
docker exec -it [container_id] bash

The -it flags let you interact with a container by allocating a pseudo-tty and keeping stdin open. Notice bash ran in the WORKDIR directory (/app) specified in the Dockerfile. From here, you have an interactive shell session inside the container to debug.

```
exit
```

You can examine a container's metadata in Docker by using Docker inspect:
docker inspect [container_id]

Use --format to inspect specific fields from the returned JSON. For example:
docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' [container_id]

### Task 5. Publish

Now you're going to push your image to the Google Artifact Registry. After that you'll remove all containers and images to simulate a fresh environment, and then pull and run your containers. This will demonstrate the portability of Docker containers.

To push images to your private registry hosted by Artifact Registry, you need to tag the images with a registry name. The format is <regional-repository>-docker.pkg.dev/my-project/my-repo/my-image.

Create the target Docker repository
You must create a repository before you can push any images to it. Pushing an image can't trigger creation of a repository and the Cloud Build service account does not have permissions to create repositories.

From the Navigation Menu, under CI/CD navigate to Artifact Registry > Repositories.

Click Create Repository.

Specify my-repository as the repository name.

Choose Docker as the format.

Under Location Type, select Region and then choose the location : us-central1 (Iowa).

Click Create.

Configure authentication
Before you can push or pull images, configure Docker to use the Google Cloud CLI to authenticate requests to Artifact Registry.

To set up authentication to Docker repositories in the region us-central1, run the following command in Cloud Shell:
gcloud auth configure-docker us-central1-docker.pkg.dev
Copied!
Enter Y when prompted.
The command updates your Docker configuration. You can now connect with Artifact Registry in your Google Cloud project to push and pull images.

Push the container to Artifact Registry
Run the following commands to set your Project ID and change into the directory with your Dockerfile.
export PROJECT_ID=$(gcloud config get-value project)
cd ~/test
Copied!
Run the command to tag node-app:0.2.
docker build -t us-central1-docker.pkg.dev/$PROJECT_ID/my-repository/node-app:0.2 .
Copied!
Run the following command to check your built Docker images.
docker images

Push this image to Artifact Registry.
docker push us-central1-docker.pkg.dev/$PROJECT_ID/my-repository/node-app:0.2

### Test the image

You could start a new VM, ssh into that VM, and install gcloud. For simplicity, just remove all containers and images to simulate a fresh environment.

Stop and remove all containers:
docker stop $(docker ps -q)
docker rm $(docker ps -aq)

You have to remove the child images (of node:lts) before you remove the node image.

Run the following command to remove all of the Docker images.
docker rmi us-central1-docker.pkg.dev/$PROJECT_ID/my-repository/node-app:0.2
docker rmi node:lts
docker rmi -f $(docker images -aq) # remove remaining images
docker images

At this point you should have a pseudo-fresh environment.

Pull the image and run it.
docker pull us-central1-docker.pkg.dev/$PROJECT_ID/my-repository/node-app:0.2
docker run -p 4000:80 -d us-central1-docker.pkg.dev/$PROJECT_ID/my-repository/node-app:0.2
curl http://localhost:4000


