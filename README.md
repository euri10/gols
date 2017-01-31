# gols

**Installation**

* `git clone https://github.com/euri10/gols.git`
* either use a virtual env or your distro packages, I use python3 and didn't test on python2 yet, but  want to learn Tox more so this is a work in progress
* if you use a venv please refer to my blog post below on the pygobject dependency, or see [this](http://stackoverflow.com/a/31609727/3581357)
* run `python3 setup.py install`, or if you prefer `pip install -e .` within your venv
* you can now run gols as a cli, `gols --help` will show you the commands and subsequent options, your watch needs to be mounted
* should you want to automate the upload a little more by triggering the script automatically, please refer to my blog post [here](https://medium.com/@euri10/gols-garmin-on-linux-sucks-f1f065f7529a#.3htyjn6q8)
or install the following systemd unit after you created the correct /etc/fstab entry

```bash
#garmin fenix 2
UUID=489A-9E97 /media/fenix2 vfat auto,nofail,rw,user,uid=1000,gid=1000 0 2
```

You'll get the UUID running `sudo blkid`.
The important parts of the entry are `auto` to tell systemd to mount the filesystem as soon as the device is available and `nofail` to ensure that boot does not fail when the device is not available (you've been warned)
(see [here](https://ddumont.wordpress.com/2016/04/24/automount-usb-devices-with-systemd/))
`rw,user,uid=1000,gid=1000` express the fact the mount will be under read-write and that the user who will run the script will have the correct permissions

```systemd
[Unit]
Description=gols a little less now
# systemctl --user list-units '*mount' might give you the exact unit name for 
# lines below
Requires=media-fenix2.mount
After=media-fenix2.mount
[Service]
# the path of a bash script that will launch the python cli with the command
# options you want, see example below
ExecStart=/home/user/PycharmProjects/gols/gols.sh
[Install]
WantedBy=media-fenix2.mount
```
Finally a bash script where you specify what upload options you want to trigger

```bash
#!/bin/bash
/home/user/venv/gols/bin/python /home/user/PycharmProjects/gols/gols/gols.py upload -d /media/fenix2/Garmin/Activity -n -m
```

```bash
(gols) ➜  gols git:(master) ✗ gols
Usage: gols [OPTIONS] COMMAND [ARGS]...

Options:
  --debug / --no_debug  Set to true to see debug logs on top of info
  --help                Show this message and exit.

Commands:
  upload  uploads .fit files to your garmin connect account
  ```
  
**Issues**

More than happy to try to help, this isn't extensively tested, other distro may have other settings I don't know, I'm on Debian testing by the way