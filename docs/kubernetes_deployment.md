# Kubernetes Deployment

A Kubernetes Deployment is typically defined using a YAML file that specifies these components. Here is an example YAML manifest.

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: example-deployment
spec:
  replicas: 3
  selector:
	matchLabels:
  	app: example-app
  template:
	metadata:
  	labels:
    	app: example-app
	spec:
  	containers:
  	- name: example-container
    	image: example-image:latest
    	ports:
    	- containerPort: 80
```

This Deployment specifies that it should maintain three replicas of the example-container Pod template. The Pods are labeled with app: example-app, and the container runs an image tagged as example-image:latest on port 80. The default rolling update strategy will be used for any updates to this Deployment. 

By utilizing Deployments, you can manage your Python web server's life cycle more efficiently, ensuring its high availability, scalability, and smooth updates. 