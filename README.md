# gcp-ssh-config

Adds all instances in all projects that your user has access to, to your local `~/.ssh/config`. This allows you to use tab autocompletion when `ssh`-ing to a host.

This is only useful if you're trying to autocomplete the `.internal` dns name.

### Set up

Make sure you are authenticated with gcloud:
```
$ gcloud auth application-default login
```

Run `gcp-ssh-config`:
```
$ pip install -r requirements.txt
$ ./gcp-ssh-config.py # this might take a while depending on how many projects you have
$ cat ~/.ssh/config # make sure it worked
$ ssh [instance-name][tab]
```

You can safely run `gcp-ssh-config.py` again and again, the list will be cleared and filled with detected hosts.
