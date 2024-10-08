# Kubernetes

## Pods and Python

To manage Kubernetes pods using Python, you can use the kubernetes library. Here is some example code of how to create, read, update, and delete a Pod using Python.

```
from kubernetes import client, config

# Load the Kubernetes configuration from the default location
config.load_kube_config()

# Alternatively, you can load configuration from a specific file
# config.load_kube_config(config_file="path/to/config")

# Initialize the Kubernetes client
v1 = client.CoreV1Api()

# Define the Pod details
pod_name = "example-pod"
container_name = "example-container"
image_name = "nginx:latest"
port = 80

# Create a Pod
def create_pod(namespace, name, container_name, image, port):
	container = client.V1Container(
    	name=container_name,
    	image=image,
    	ports=[client.V1ContainerPort(container_port=port)],
	)

	pod_spec = client.V1PodSpec(containers=[container])
	pod_template = client.V1PodTemplateSpec(
    	metadata=client.V1ObjectMeta(labels={"app": name}), spec=pod_spec
	)

	pod = client.V1Pod(
    	api_version="v1",
    	kind="Pod",
    	metadata=client.V1ObjectMeta(name=name),
    	spec=pod_spec,
	)

	try:
    	response = v1.create_namespaced_pod(namespace, pod)
    	print("Pod created successfully.")
    	return response
	except Exception as e:
    	print("Error creating Pod:", e)


# Read a Pod
def get_pod(namespace, name):
	try:
    	response = v1.read_namespaced_pod(name, namespace)
    	print("Pod details:", response)
	except Exception as e:
    	print("Error getting Pod:", e)


# Update a Pod (e.g., change the container image)
def update_pod(namespace, name, image):
	try:
    	response = v1.read_namespaced_pod(name, namespace)
    	response.spec.containers[0].image = image

    	updated_pod = v1.replace_namespaced_pod(name, namespace, response)
    	print("Pod updated successfully.")
    	return updated_pod
	except Exception as e:
    	print("Error updating Pod:", e)


# Delete a Pod
def delete_pod(namespace, name):
	try:
    	response = v1.delete_namespaced_pod(name, namespace)
    	print("Pod deleted successfully.")
	except Exception as e:
    	print("Error deleting Pod:", e)


if __name__ == "__main__":
	namespace = "default"

	# Create a Pod
	create_pod(namespace, pod_name, container_name, image_name, port)

	# Read a Pod
	get_pod(namespace, pod_name)

	# Update a Pod
	new_image_name = "nginx:1.19"
	update_pod(namespace, pod_name, new_image_name)

	# Read the updated Pod
	get_pod(namespace, pod_name)

	# Delete the Pod
	delete_pod(namespace, pod_name)
```

## Services and Python

Here’s an example of some Python code that uses the Kubernetes Python client to create, list, and delete Kubernetes Services in a given namespace.

```
from kubernetes import client, config

def create_service(api_instance, namespace, service_name, target_port, port, service_type):
	# Define the Service manifest based on the chosen Service type
	service_manifest = {
    	"apiVersion": "v1",
    	"kind": "Service",
    	"metadata": {"name": service_name},
    	"spec": {
        	"selector": {"app": "your-app-label"},
        	"ports": [
            	{"protocol": "TCP", "port": port, "targetPort": target_port}
        	]
    	}
	}

	if service_type == "ClusterIP":
    	# No additional changes required for ClusterIP, it is the default type
    	pass
	elif service_type == "NodePort":
    	# Set the NodePort field to expose the service on a specific port on each node
    	service_manifest["spec"]["type"] = "NodePort"
	elif service_type == "LoadBalancer":
    	# Set the LoadBalancer type to get an external load balancer provisioned
    	service_manifest["spec"]["type"] = "LoadBalancer"
	elif service_type == "ExternalName":
    	# Set the ExternalName type to create an alias for an external service
    	service_manifest["spec"]["type"] = "ExternalName"
    	# Set the externalName field to the DNS name of the external service
    	service_manifest["spec"]["externalName"] = "my-external-service.example.com"

	api_response = api_instance.create_namespaced_service(
    	body=service_manifest,
    	namespace=namespace,
	)
	print(f"Service '{service_name}' created with type '{service_type}'. Status: {api_response.status}")


def list_services(api_instance, namespace):
	api_response = api_instance.list_namespaced_service(namespace=namespace)
	print("Existing Services:")
	for service in api_response.items:
    	print(f"Service Name: {service.metadata.name}, Type: {service.spec.type}")


def delete_service(api_instance, namespace, service_name):
	api_response = api_instance.delete_namespaced_service(
    	name=service_name,
    	namespace=namespace,
	)
	print(f"Service '{service_name}' deleted. Status: {api_response.status}")


if __name__ == "__main__":
	# Load Kubernetes configuration (if running in-cluster, this might not be necessary)
	config.load_kube_config()

	# Create an instance of the Kubernetes API client
	v1 = client.CoreV1Api()

	# Define the namespace where the services will be created
	namespace = "default"

	# Example: Create a ClusterIP Service
	create_service(v1, namespace, "cluster-ip-service", target_port=8080, port=80, service_type="ClusterIP")

	# Example: Create a NodePort Service
	create_service(v1, namespace, "node-port-service", target_port=8080, port=30000, service_type="NodePort")

	# Example: Create a LoadBalancer Service (Note: This requires a cloud provider supporting LoadBalancer)
	create_service(v1, namespace, "load-balancer-service", target_port=8080, port=80, service_type="LoadBalancer")

	# Example: Create an ExternalName Service
	create_service(v1, namespace, "external-name-service", target_port=8080, port=80, service_type="ExternalName")

	# List existing Services
	list_services(v1, namespace)

	# Example: Delete a Service
	delete_service(v1, namespace, "external-name-service")
```

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

# Parameterizing YAML files with Python

As you’ve seen, YAML files are the backbone of defining and managing resources. However, static YAML files can be limiting, especially when you need to manage different configurations for different environments or deployment scenarios. This is where Python comes in, offering a dynamic and flexible approach to parameterize your YAML files.

For instance, you can customize your rolling update strategy using Python with the following example code.

```
from kubernetes import client, config

def update_deployment_strategy(deployment_name, namespace, max_unavailable):
    config.load_kube_config()
    apps_v1 = client.AppsV1Api()

    deployment = apps_v1.read_namespaced_deployment(deployment_name, namespace)
    deployment.spec.strategy.rolling_update.max_unavailable = max_unavailable
    apps_v1.patch_namespaced_deployment(deployment_name, namespace, deployment)

if __name__ == "__main__":
    update_deployment_strategy('my-deployment', 'my-namespace', '25%')
```

This is just one example of how Python provides a powerful and flexible way to parameterize your YAML files in Kubernetes. 

