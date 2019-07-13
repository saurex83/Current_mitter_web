# Настройка RPI

## Установка ОС
Установил ОС Raspbian Buster Lite  https://www.raspberrypi.org/downloads/raspbian/

## Доступ по ssh 
Добавил файл ssh в раздел /boot для разрешения доступа по ssh

## Пользователи
Добавил пользователя saurex83 и удалил pi

adduser saurex83
usermod saurex83 -a -G sudo
userdel -r pi

## fstab
Запрещаем запись логов и временных файлов на sd карту

tmpfs           /tmp                tmpfs   defaults,noatime,nosuid,size=100m                   0   0
tmpfs           /var/tmp            tmpfs   defaults,noatime,nosuid,size=30m                    0   0
tmpfs           /var/log            tmpfs   defaults,noatime,nosuid,mode=0755,size=100m         0   0
tmpfs           /var/spool/mqueue   tmpfs   defaults,noatime,nosuid,mode=0700,gid=12,size=10m   0   0

## swap
Отключаем файл подкачки

dphys-swapfile swapoff
dphys-swapfile uninstall
systemctl disable dphys-swapfile

## Видеопамять
Уменьшаем количество видеопамяти до 1 МБ
raspi-config

## Bluetooth
systemctl disable bluetooth
systemctl stop bluetooth

## Брандмауер
Закроем все кроме
apt install iptables-persistent
Создаст правила на основе текущих и их нужно поменять. Сделаю позже.

## Часы реального времени
Устанавливаем утилиты для работы с i2c
  sudo apt-get install i2c-tools

Редактируем настройки и разрешаем i2c
sudo nano /boot/config.txt
  dtparam=i2c_arm=on
  dtoverlay=i2c-rtc,pcf8523  (добавить внизу)
  
raspi-config Включил i2c
 
sudo modprobe rtc-ds1307

Добавь в /etc/modules
 rtc-ds1307
 
пропишите в /etc/rc.local перед exit0 следующие команды:
  echo ds1307 0x68 > /sys/class/i2c-adapter/i2c-1/new_device
  sudo hwclock -s

Считать время:
  sudo hwclock -r
  
Установить время:
 date --set=”20140125 09:17:00”
 sudo hwclock -w
 
Синхронизация системного времени с аппаратным:
  sudo hwclock -s

Запрет изменения времени через интернет
  sudo update-rc.d ntp disable

# Postgresql
  sudo apt update
  sudo apt-get install postgresql
  
  sudo usermode saurex83 -a -G postgres
  sudo su postgres
  psql
    \du
    CREATE USER saurex83;
    \q
  createdb saurex83 (создает базу для моего пользователя)
Создание базы
=> CREATE DATABASE cmetter;
Просмотр созданых баз
=> select * from pg_database;

# python3
sudo apt install python3-dev
sudo apt install python3-pip

# ngix
sudo apt-get install nginx
sudo systemctl enable nginx
sudo systemctl start nginx

# uwsgi
sudo apt-get install uwsgi

# git
sudo apt install git

# hostname 
sudo nano /etc/hostname
 cmeter

# create ap
Создание точки доступа
git clone https://github.com/oblique/create_ap
sudo apt install hostapd
sudo apt install dnsmasq

cd create_ap
make install


  
