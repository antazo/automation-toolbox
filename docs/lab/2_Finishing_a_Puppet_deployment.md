# Finishing a Puppet deployment

## Install packages

'''
ssh -i xxx.ppk user@cloud
'''

'''
cd /etc/puppet/code/environments/production/modules/packages
cat manifests/init.pp
'''

'''
class packages {
   package { 'python-requests':
       ensure => installed,
   }
   if $facts[os][family] == "Debian" {
     package { 'golang':
       ensure => installed,
     }
  }
   if $facts[os][family] == "RedHat" {
     package { 'nodejs':
       ensure => installed,
     }
  }
}
'''

Once you've edited the file and added the necessary resources, you'll want to check that the rules work successfully. We can do this by connecting to another machine in the network and verifying that the right packages are installed.

We will be connecting to linux-instance using its external IP address. To fetch the external IP address of linux-instance, use the following command:

'''
gcloud compute instances describe linux-instance --zone=us-central1-f --format='get(networkInterfaces[0].accessConfigs[0].natIP)'
# student-01-f3190cff24a6@34.27.96.239
'''

This command outputs the external IP address of linux-instance. Copy the linux-instance external IP address, open another terminal and connect to it. Follow the instructions given in the section Accessing the virtual machine by clicking on Accessing the virtual machine from the navigation pane at the right side.

Now manually run the Puppet client on your linux-instance VM instance terminal:

'''
sudo puppet agent -v --test
apt policy golang
'''

## Fetch machine information

'''
class machine_info {
	if $facts[kernel] == "windows" {
		$info_path = "C:\Windows\Temp\Machine_Info.txt"
	} else {
		$info_path = "/tmp/machine_info.txt"
	}
	file { 'machine_info':
		path => $info_path,
		content => template('machine_info/info.erb'),
	}
}
'''

### Puppet Templates

Templates are documents that combine code, data, and literal text to produce a final rendered output. The goal of a template is to manage a complicated piece of text with simple inputs.

In Puppet, you'll usually use templates to manage the content of configuration files (via the content attribute of the file resource type).

Templates are written in a templating language, which is specialized for generating text from data. Puppet supports two templating languages:

Embedded Puppet (EPP) uses Puppet expressions in special tags. It's easy for any Puppet user to read, but only works with newer Puppet versions. (≥ 4.0, or late 3.x versions with future parser enabled.)
Embedded Ruby (ERB) uses Ruby code in tags. You need to know a small bit of Ruby to read it, but it works with all Puppet versions.
Now, take a look at the template file using the following command.

'''
cat templates/info.erb
sudo chmod 646 templates/info.erb
nano templates/info.erb
'''

'''
Machine Information
-------------------
Disks: <%= @disks %>
Memory: <%= @memory %>
Processors: <%= @processors %>
Network Interfaces: <%= @interfaces %>
}
'''

linux_instance VM:

'''
sudo puppet agent -v --test
'''

puppet VM:

'''
cat /tmp/machine_info.txt
'''

## Reboot machine

For the last exercise, we will be creating a new module named reboot, that checks if a node has been online for more than 30 days. If so, then reboot the computer.

To do that, you'll start by creating the module directory.

Switch back to puppet VM terminal and run the following command:

'''
sudo mkdir -p /etc/puppet/code/environments/production/modules/reboot/manifests
'''

Go to the manifests/ directory.

'''
cd /etc/puppet/code/environments/production/modules/reboot/manifests
'''

Create an init.pp file for the reboot module in the manifests/ directory.

'''
sudo touch init.pp
'''

Open init.pp with nano editor using sudo.

'''
sudo nano init.pp
'''

In this file, you'll start by creating a class called reboot.

The way to reboot a computer depends on the OS that it's running. So, you'll set a variable that has one of the following reboot commands, based on the kernel fact:

 * shutdown /r on windows
 * shutdown -r now on Darwin (macOS)
 * reboot on Linux.

Hence, add the following snippet in the file init.pp:

'''
class reboot {
	if $facts[kernel] == "windows" {
		$cmd = "shutdown /r"
	} elsif $facts[kernel] == "Darwin" {
		$cmd = "shutdown -r now"
	} else {
		$cmd = "reboot"
	}
}
'''

With this variable defined, we will now define an exec resource that calls the command, but only when the uptime_days fact is larger than 30 days.

Add the following snippet after the previous one within the class definition in the file reboot/manifests/init.pp:


'''
class reboot {
  if $facts[kernel] == "windows" {
    $cmd = "shutdown /r"
  } elsif $facts[kernel] == "Darwin" {
    $cmd = "shutdown -r now"
  } else {
    $cmd = "reboot"
  }
  if $facts[uptime_days] > 30 {
    exec { 'reboot':
      command => $cmd,
     }
   }
}
'''

Finally, to get this module executed, make sure to include it in the site.pp file.

So, edit /etc/puppet/code/environments/production/manifests/site.pp using the following command:

'''
sudo nano /etc/puppet/code/environments/production/manifests/site.pp 
'''

'''
node default {
   class { 'packages': }
   class { 'machine_info': }
   class { 'reboot': }
}
'''

Run the client on linux-instance VM terminal:

'''
sudo puppet agent -v --test
'''
