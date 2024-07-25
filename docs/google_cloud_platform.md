# Creating a VM template and Automating deployment

## On VM

```
git clone https://www.github.com/google/it-cert-automation-practice.git
cd ~/it-cert-automation-practice/Course5/Lab3
```

In order to enable hello_cloud.py to run on boot, copy the file hello_cloud.py to the /usr/local/bin/ location.

```
sudo cp hello_cloud.py /usr/local/bin/
```

Also copy hello_cloud.service to the /etc/systemd/system/ location.

```
sudo cp hello_cloud.service /etc/systemd/system
```

Now, use the systemctl command to enable the service hello_cloud.

```
sudo systemctl enable hello_cloud.service
```

Created symlink /etc/systemd/system/default.target.wants/hello_cloud.service → /etc/systemd/system/hello_cloud.service.


## On local

Additionally, while "gcloud init" is not always required for every lab, it can sometimes help in setting up your environment correctly. You can try running "gcloud init" before creating the instances to ensure everything is set up properly:

```
gcloud init
```

Create new VM instances with the template named vm1-template from your terminal using gcloud command-line interface. To do this, enter the following command:

```
gcloud compute instances create --zone us-central1-a --source-instance-template vm1-template vm2 vm3 vm4 vm5 vm6 vm7 vm8
```

Wait for the command to finish. Once it's done, you can view the instances through the Console or by using the following gcloud command on your local terminal:

```
gcloud compute instances list
```
