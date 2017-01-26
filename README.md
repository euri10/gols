# gols

**Installation**

* `git clone https://github.com/euri10/gols.git`
* either use a virtual env or your distro packages, I use python3 and didn't test on python2
* if you use a venv please refer to my blog post below on the pygobject dependency, or see http://stackoverflow.com/a/31609727/3581357
* run `python3 setup.py install`, or if you prefer `pip install -e .` within your venv
* you can now run gols as a cli, `gols --help` will show you the options, your watch need to ne mounted
* should you want to automate the upload a little more by triggering the script automatically, please refer to my blog post here

```
(gols) ➜  gols git:(master) ✗ gols --help                          
Usage: gols [OPTIONS]

Options:
  -d, --directory_fit DIRECTORY   Path of your .fit files on your watch mount
                                  path  [required]
  -n, --notifcation / --no_notification
                                  Get notified
  -m, --move / --no_move          Move files upon upload
  --debug / --no_debug            Set to true to see debug logs on top of info
  --help                          Show this message and exit.
  ```
  
**Issues**

More than happy to try to help, this isn't extensively tested, other distro may have other settings I don't know, I'm on Debian testing by the way