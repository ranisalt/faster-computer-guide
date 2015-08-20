# ranisalt's guide to a faster computer

## General recommendations
- **Disable unnecessary services**. You can check what are the major hogs with *systemd-analyze blame*, and it will list processes taking boot time, sorted by heavier first. Then, mask them with *systemctl mask <unit name>* and you're ready, and *systemctl unmask <unit name>* if something goes wrong. You will look forward to disabling Bluetooth, infrared, and even firewalls if you are not concerned with it.
- **Use a lighter display manager**. **SLiM** is always a good option, **LightDM** is good too. You can also go with no DM at all, shaving off precious time. If your distro comes with, consider disabling Plymouth too (we're goind FAST, not EYE-CANDY).
- **Use a lighter bootloader**. GRUB can take a big time just running scripts. If you have only one boot option or you can use the UEFI bootloader, you can use lighter options such as **Syslinux** and **Gummiboot**, or if you are savvy you can give a shot to [EFI stub](https://wiki.archlinux.org/index.php/EFISTUB).
- **Use a lighter desktop environment (or none)**. Run away from **GNOME** and **KDE** if you are pursuing performance, as those giants can consume up to one gigabyte of memory and lots of CPU cycles. Opt to a lighter alternative, such as **XFCE** and **LXDE**, or even better, give up completely on DEs and use only a window manager, such as **dwm**, **i3** (my personal choice) or **xmonad**.
- **Avoid using fancy disk settings**, such as LVM, if you don't need to. Also, don't use encrypted partitions (*/home* is fine). Also remember to set your SATA disks to run in AHCI mode, not IDE.
- **Replace your HDD with SSD**. This is probably the simplest option. You don't need to run your entire system on SSD to get a boost, you only need to have your boot files (*/boot* partition) and executables (*/usr*), although personally I only have */home* and swap on HDD.
- **Use lighter software always**. From personal experience, I found that **wicd** is faster and lighter on resources than **NetworkManager**. **Firefox** tends to use less memory than **Chrome**. **mpv** is a simple but amazingly complete media player, usually better than **Totem** and **VLC**. Consider learning **vim** instead of an IDE or graphical editors. Also, you do not need an office suite since Google Docs is great.

If you followed the guide religiously up to here, you are ready to dig into more command line stuff. Don't be scared, I won't brick your computer.

## Finer system tuning
- **Decrease output during boot**. Your system might spit out a ton of information during boot, but really it's too much and too fast to care. Go to your bootloader configuration (Google it) and append the following to the kernel command line:

  ```
  quiet loglevel=3 splash
  ```

  It removes most of the messages and sets the log level to display only error messages. You can read the boot output later using *dmesg* and *journalctl*.
- **Finer tuning of _/etc/fstab_**. First of all, you can use the *noatime* option on ext filesystems to prevent updating access time of files, thus not writing to the disk every time you touch a file (although *touch* still works). You can also specify *discard* on SSD partitions to activate TRIM (Google it), and *commit=60* on SSD to sync to disk less frequently. For example, the full line for my */* partition:

  ```
  /dev/sdb3	/	ext4	discard,noatime,commit=60	0	0
  ```

- **Optimize your initrd**. On Arch Linux, you can modify */etc/mkinitcpio.conf* and it is very well documented and I intend to have a deeply optimized example soon, but you can change the *COMPRESSION* to *cat* on SSD to generate a larger initrd in favor of faster (instant) decompression, a fine trade-off around 10 times faster than gzip. On other distros, refer to the official guides and manuals.
- **Use [profile-sync-daemon](https://wiki.archlinux.org/index.php/Profile-sync-daemon)**. It is a great tool by [@graysky2](https://github.com/graysky2) to manage your browser profile on tmpfs, and it both increases performance and reduces disk wear. If supported, use it in "overlayfs" mode to minimize sync delay. To check if your system supports it, run:

  ```bash
  $ zgrep OVERLAY /proc/config.gz
  ```

  And it should output either `CONFIG_OVERLAY_FS=m` or `CONFIG_OVERLAY_FS=y`, else you need to recompile your kernel. Then, edit */etc/psd.conf* and uncomment `USE_OVERLAYFS="yes"`. Reboot and check.

- **Replace bash by dash on boot**. This is a tricky one. **dash** is a very slim alternative to **bash** and it can be used on boot to shave off some milliseconds. You need to redirect */usr/bin/sh* to */usr/bin/dash* if it was linked to bash. Check it first:

  ```bash
  $ ls -og /usr/bin/sh
  lrwxrwxrwx 1 4 Aug 14 03:03 /usr/bin/sh -> bash
  ```

  So yes, it was linking bash. Go to */usr/bin* and change it:

  ```bash
  $ cd /usr/bin
  $ ln -s dash sh
  ```

  And you are good to go. Just remeber to update your scripts if they rely heavily on bash and are configured to use */usr/bin/sh*.

There's more to come.

## License
[This work is under public domain](https://github.com/ranisalt/faster-computer-guide/blob/master/LICENSE).
