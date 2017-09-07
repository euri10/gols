=====
Usage
=====

The CLI way
-----------

You can use gols with your favorite command line terminal, that's fine, just run `gols --help` and see what commands, switches you need to enter !

.. code-block:: bash

    Usage: gols [OPTIONS] COMMAND [ARGS]...

    Options:
      --debug / --no_debug  Set to true to see debug logs on top of info
      --help                Show this message and exit.

    Commands:
      upload  uploads .fit files to your garmin connect account

The upload command needs in particular your username and password account. You can pass them with the `-u` and `-p` switches respectively, however it's recommended you use the environment variables.
So either you do:
.. code-block:: bash

    export GARMINCONNECT_USERNAME=user GARMINCONNECT_PASSWORD=password gols --debug upload blabblablabla

Either you add those variables in your favorite .zshrc, if you just have a .bashrc go get zsh and oh-my-zsh !

The automatic way
-----------------

To use gols in a more user friendly manner, you'll need 3 things, this assumes your distribution uses systemd, should it not be the case you can adapt using udev rules !
The installation is a little-bit involved but worth the effort, I now just plugs my watch and bam, it's uploaded !

1. Add your Garmin device to your /etc/fstab, mine for instance

    .. code-block:: bash

        #garmin fenix 2
        UUID=489A-9E97 /media/fenix2 vfat auto,nofail,rw,user,uid=1000,gid=1000 0 2

Then endpoint `/media/fenix2` is created by the user who will upload its activities and you'll have to run `sudo blkid` to get the device UUID.
Issue a `systemd daemon-reload` so that you get the mount name systemd will assign to your new entry.

2. Create a systemd user unit with `systemctl --user edit gols.service --force`.

What is important in that file is the `media-fenix2.mount`, adapt yours with what systemd came up after step 1.

    .. code-block:: bash

        [Unit]
        Description=gols a little less now
        Requires=media-fenix2.mount
        After=media-fenix2.mount
        [Service]
        ExecStart=gols -d /media/fenix2/Garmin/Activity -m /home/lotso/.config/gols/fit
        [Install]
        WantedBy=media-fenix2.mount
