# mappage des appareils en /dev/ttyACMxx et /dev/USBxx avec des symlink fiables

# afficher les infos de l'appareil serial sur ttyACM0:
# udevadm info --attribute-walk --name=ttyACM0

# ajouter l'appareil aux udev rules (alias dans les /dev):
# recup le idVendor et idProduct avec la commande du dessus
# echo 'SUBSYSTEM=="tty", ATTRS{idVendor}=="xxxx", ATTRS{idProduct}=="xxxx", SYMLINK+="gps"' >> /etc/udev/rules.d/99-usb-gps.rules

# ne pas oublier les usermod
# usermod -a -G dialout $USER
# usermod -a -G tty $USER

# automount du periph de stockage
# faire le backup du fstab avant de modifier, chiant a reparer
# cp /etc/fstab /etc/fstab.bak
# echo 'LABEL=TOSHIBA /media/usb auto auto,nofail,noatime,umask=000 0 0' >> /etc/fstab