# Debugging a problem with a Cloud Deployment and Fix it

## Debug the issue

HTTP response status codes indicate whether a specific HTTP request has been successfully completed. Responses are grouped into five classes:

Informational responses (100–199)
Successful responses (200–299)
Redirects (300–399)
Client errors (400–499)
Server errors (500–599)
The HyperText Transfer Protocol (HTTP) 500 Internal Server Error response code indicates that the server encountered an unexpected condition that prevented it from fulfilling the request. Before troubleshooting the error, you'll need to understand more about systemctl.

systemctl is a utility for controlling the systemd system and service manager. It comes with a long list of options for different functionality, including starting, stopping, restarting, or reloading a daemon.

Let's now troubleshoot the issue. Since the webpage returns an HTTP error status code, let's check the status of the web server i.e apache2.

```
sudo systemctl status apache2
sudo systemctl restart apache2
```

To find which processes are listening on which ports, we'll be using the netstat command, which returns network-related information. Here, we'll be using a combination of flags along with the netstat command to check which process is using a particular port:

```
sudo netstat -nlp
```


Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
tcp        0      0 127.0.0.53:53           0.0.0.0:*               LISTEN      345/systemd-resolve
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      781/sshd: /usr/sbin
tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN      1347/python3


1347/python3


```
ps -ax | grep python3
```

    498 ?        Ss     0:00 /usr/bin/python3 /usr/bin/networkd-dispatcher --run-startup-triggers
    531 ?        Ssl    0:00 /usr/bin/python3 /usr/share/unattended-upgrades/unattended-upgrade-shutdown --wait-for-signal
   1347 ?        Ss     0:00 python3 /usr/local/bin/jimmytest.py
   3012 pts/0    S+     0:00 grep --color=auto python3

```
cat /usr/local/bin/jimmytest.py
```

```
sudo kill 1347
```

This time you'll notice that similar process running again with a new PID.

This kind of behavior should be caused by service. Since this is a python script created by Jimmy, let's check for the availability of any service with the keywords "python" or "jimmy".

```
sudo systemctl --type=service | grep jimmy
```

There is a service available named jimmytest.service. We should now stop and disable this service using the following command:

```
sudo systemctl stop jimmytest && sudo systemctl disable jimmytest
```

The service is now removed.

To confirm that no processes are listening on 80, using the following command:

```
sudo netstat -nlp
```

```
sudo systemctl start apache2
```