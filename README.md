# Album-Art-Tool -> see [NR1-UI-Remote]() for more details

## This tool must be running as service in Background.

## What is it good for?

### This tool takes the actuall Albumart from Volumio, resizes it to 90x90 and places it in /home/volumio/ as album.bmp
### The NR1-UI-Remote requieres this file to be aviable via ftp.

## Please set up FTP first:
### [Instruction to Setup proftpd](https://www.thomas-krenn.com/de/wiki/FTP-Server_unter_Debian_einrichten)

### Make sure that the FTP Server matches this configuration:
* No IPv6
* Username: volumio
* Password: volumio
* Default Directory is set to "home/volumio"
```
# Default directory is ftpusers home
DefaultRoot ~ volumio
```
Make these folder: /home/volumio/proftpd
```
sudo mkdir /home/volumio/proftpd
```
make this two files: /home/volumio/proftpd/controls.log and proftpd.log
```
cd proftpd

sudo nano controls.log
-> add one "whitespace" and save the file

sudo nano proftpd.log
-> add one "whitespace" and save the file
```
Edit the proftpd.conf file:
```
sudo nano /etc/proftpd/proftpd.conf
```
line 89 & 90:
```
#TransferLog /home/volumio/proftpd/xferlog
#SystemLog   /home/volumio/proftpd/proftpd.log
```
line 120:
```
#ControlsLog           /var/log/proftpd/controls.log
```
save the file.
Restart FTP service:
```
sudo service proftpd restart
```
Check if FTP is working with FileZilla/WinSCP.

## Continue when FTP is working fine:

```
git clone https://github.com/Maschine2501/Album-Art-Tool.git

sudo cp /home/volumio/Album-Art-Tool/AlbumImage.service /lib/systemd/system/

sudo systemctl daemon-reload

sudo systemctl enable AlbumImage.service

```
You can now either reboot or start the service manually:
```
sudo systemctl start AlbumImage.service
```
Or stop the service:
```
sudo systemctl stop AlbumImage.service
```

## Maybe you need to install some modules, please check the journal to see what is needed:
```
sudo journalctl -fu AlbumImage.service
```

