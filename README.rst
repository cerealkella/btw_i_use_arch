==============
BTW I Use Arch
==============


.. image:: https://img.shields.io/pypi/v/btw_i_use_arch.svg
        :target: https://pypi.python.org/pypi/btw_i_use_arch

.. image:: https://img.shields.io/travis/kellerjustin/btw_i_use_arch.svg
        :target: https://travis-ci.com/kellerjustin/btw_i_use_arch

.. image:: https://readthedocs.org/projects/btw-i-use-arch/badge/?version=latest
        :target: https://btw-i-use-arch.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/kellerjustin/btw_i_use_arch/shield.svg
     :target: https://pyup.io/repos/github/kellerjustin/btw_i_use_arch/
     :alt: Updates



Helper menu-driven CLI for installing packages and setting up Linux components on an 
Arch-based system.
If performing a clean install - ALWAYS RUN PACMAN SYSTEM UPDATES FIRST!
Disclaimer: I have built precisely one Arch system and spend the majority of my time 
using Manjaro KDE, which suits my needs nicely. I like Arch! But I think I might 
actually prefer Manjaro. This package works equally well for either distro. 


* Free software: MIT license
* Documentation: https://btw-i-use-arch.readthedocs.io.


Features
--------

* Menu-driven (uses simple-term-menu)
* Update components and perform setup tasks more simply


Notes for specific packages:
----------------------------

Spelling check packages
^^^^^^^^^^^^^^^^^^^^^^^

``aspell
hunspell-en_US
hspell
libviokko``

DB Drivers for GNUCash
^^^^^^^^^^^^^^^^^^^^^^

``libdbi
libdbi-drivers``

Packages required to enable gestures for touchpad
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``xdotool
xf86-input-synaptics
libinput-gestures``

KDE-Specific Widget for setting up like Mac-like dock
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``latte-dock``

KDE-Specific Widget - Configures Title bar in Global Menu
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

https://www.dedoimedo.com/computers/plasma-look-like-mac.html
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``plasma5-applets-active-window-control``

Post-installation Tasks:
------------------------

Set up latte dock and widgets
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If going for the dock / top menu bar look, search the apps menu for dock and add it.
Drag the menu bar from the bottom to the top and add the global menu, active window control, and a spacer (L-to-R). Edit the settings of
active window control so it shows the Minimize and Maximize buttons.
Run this to remove the top title bar when windows are maximized:
``kwriteconfig5 --file ~/.config/kwinrc --group Windows --key BorderlessMaximizedWindows true
qdbus org.kde.KWin /KWin reconfigure``
`Reference for removing title bar <https://askubuntu.com/questions/253337/remove-title-bar-and-borders-on-maximized-windows-in-kubuntu>`_

initialize postgres:
^^^^^^^^^^^^^^^^^^^^

https://lobotuerto.com/blog/how-to-install-postgresql-in-manjaro-linux/
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

restore database dumps manually
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

e.g.:
^^^^^

.. code-block::

   psql -U justin -d gnucash-kff -f ./Desktop/dumpfile

set up cron jobs, e.g. [./dev/pg-db-backup/db-export.py]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Mounting an NFS Share
^^^^^^^^^^^^^^^^^^^^^

Substitute the relevant server and local share directory
as necessary. Optionally backup /etc/fstab

.. code-block::

   sudo cp /etc/fstab /etc/fstab_bkp

and add the following line:
192.168.100.100:/mnt/tank /home/justin/nfs_share nfs _netdev 0 0

Restoring a user profile
^^^^^^^^^^^^^^^^^^^^^^^^

Navigate to user directory and run:

.. code-block::

   tar xzvf /backup/location/mybackup.tar.gz

Setting up .pypirc file
^^^^^^^^^^^^^^^^^^^^^^^

Use template provided and plug in keys from gitlab
and pypi, place in home directory for easy deployments

Accessing USB Devices / Microcontrollers without sudo:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Find the device:
``sudo dmesg | grep tty``
Find the Group ID by running this command: (change tty device accordingly)
``stat /dev/ttyUSB0``
Add your Linux user to the gid determined in the previous command ("uucp" in this case)
``sudo gpasswd -a $USER uucp``

Issues I've encountered + Fixes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Issue
     - Fix
   * - Blocky, weird looking text rendered in PDFs and Webpages
     - epifonts was causing a conflict with Helvetica (\ ``yay -R epifonts``\ )
   * - Spotify Problem importing key
     - Run this: ``curl -sS https://download.spotify.com/debian/pubkey.gpg | gpg --import -`` and choose No when yay asks to import key during installation
   * - Slow Wi-Fi
     - https://wiki.archlinux.org/title/NetworkManager#Using_iwd_as_the_Wi-Fi_backend - set iwd as Wi-Fi Backend


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.
It also utilizes simple-term-menu_ by IngoMeyer441.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _simple-term-menu: https://github.com/IngoMeyer441/simple-term-menu
