#!/usr/bin/env bash

sed -i "s/^login.*=.*\'.*\'/login = \'your_login\'/g" downloader.py
sed -i "s/^password.*=.*\'.*\'/password = \'your_password\'/g" downloader.py
sed -i "s/^my_id.*=.*\'.*\'/my_id = \'your_vk_id\'/g" downloader.py
