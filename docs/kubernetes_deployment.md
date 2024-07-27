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

# Deployments and Python

The following Python script uses the Kubernetes Python client to create, list, and delete Kubernetes Services in a given namespace.

```
from kubernetes import client, config

def create_deployment(api_instance, namespace, deployment_name, image, replicas):
	# Define the Deployment manifest with the desired number of replicas and container image.
	deployment_manifest = {
    	"apiVersion": "apps/v1",
    	"kind": "Deployment",
    	"metadata": {"name": deployment_name},
    	"spec": {
        	"replicas": replicas,
        	"selector": {"matchLabels": {"app": deployment_name}},
        	"template": {
            	"metadata": {"labels": {"app": deployment_name}},
            	"spec": {
                	"containers": [
                    	{"name": deployment_name, "image": image, "ports": [{"containerPort": 80}]}
                	]
            	},
        	},
    	},
	}

	# Create the Deployment using the Kubernetes API.
	api_response = api_instance.create_namespaced_deployment(
    	body=deployment_manifest,
    	namespace=namespace,
	)
	print(f"Deployment '{deployment_name}' created. Status: {api_response.status}")

def update_deployment_image(api_instance, namespace, deployment_name, new_image):
	# Get the existing Deployment.
	deployment = api_instance.read_namespaced_deployment(deployment_name, namespace)

	# Update the container image in the Deployment.
	deployment.spec.template.spec.containers[0].image = new_image

	# Patch the Deployment with the updated image.
	api_response = api_instance.patch_namespaced_deployment(
    	name=deployment_name,
    	namespace=namespace,
    	body=deployment
	)
	print(f"Deployment '{deployment_name}' updated. Status: {api_response.status}")

def delete_deployment(api_instance, namespace, deployment_name):
	# Delete the Deployment using the Kubernetes API.
	api_response = api_instance.delete_namespaced_deployment(
    	name=deployment_name,
    	namespace=namespace,
    	body=client.V1DeleteOptions(
        	propagation_policy="Foreground",
        	grace_period_seconds=5,
    	)
	)
	print(f"Deployment '{deployment_name}' deleted. Status: {api_response.status}")


if __name__ == "__main__":
	# Load Kubernetes configuration (if running in-cluster, this might not be necessary)
	config.load_kube_config()

	# Create an instance of the Kubernetes API client for Deployments
	v1 = client.AppsV1Api()

	# Define the namespace where the Deployment will be created
	namespace = "default"

	# Example: Create a new Deployment
	create_deployment(v1, namespace, "example-deployment", image="nginx:latest", replicas=3)

	# Example: Update the image of the Deployment
	update_deployment_image(v1, namespace, "example-deployment", new_image="nginx:1.19.10")

	# Example: Delete the Deployment
	delete_deployment(v1, namespace, "example-deployment")
```
