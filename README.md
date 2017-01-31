# gols

**Installation**

* `git clone https://github.com/euri10/gols.git`
* either use a virtual env or your distro packages, I use python3 and didn't test on python2
* if you use a venv please refer to my blog post below on the pygobject dependency, or see [this](http://stackoverflow.com/a/31609727/3581357)
* run `python3 setup.py install`, or if you prefer `pip install -e .` within your venv
* you can now run gols as a cli, `gols --help` will show you the options, your watch need to ne mounted
* should you want to automate the upload a little more by triggering the script automatically, please refer to my blog post [here](https://medium.com/@euri10/gols-garmin-on-linux-sucks-f1f065f7529a#.3htyjn6q8)
or install the following systemd unit after you created the correct /etc/fstab entry

```bash
#garmin fenix 2
UUID=489A-9E97 /media/fenix2 vfat auto,nofail,rw,user,uid=1000,gid=1000 0 2
```
```systemd
[Unit]
Description=gols a little less now
Requires=media-fenix2.mount
After=media-fenix2.mount
[Service]
ExecStart=/home/user/PycharmProjects/gols/gols.sh
[Install]
WantedBy=media-fenix2.mount
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