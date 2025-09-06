# A. Môi trường dev
## I. Deployment
### 0. Install packages and Python3.12.10
```
sudo apt install python3-virtualenv
sudo apt install python3-pip
pip3 install virtualenv

sudo apt install virtualenv
sudo apt install software-properties-common
sudo apt install wget build-essential checkinstall
sudo apt install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev
cd /opt
sudo wget https://www.python.org/ftp/python/3.12.10/Python-3.12.10.tgz
sudo tar xzf Python-3.12.10.tgz
cd Python-3.12.10
sudo ./configure --enable-optimizations
sudo make altinstall
sudo rm -f /opt/Python-3.12.10.tgz
```

### 1. Copy source code và cài đặt các gói python
```bash
mkdir /home/laptop029/fast-code-challenge
cd /home/laptop029/fast-code-challenge
mkdir logs
** Copy source code vào /home/laptop029/fast-code-challenge
virtualenv venv --python='/usr/local/bin/python3.12'
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
deactivate
```

### 2. Viết service
Nội dung file fast_code_challenge.service xem trong fast_code_challenge.service
```bash
sudo nano /etc/systemd/system/fast_code_challenge.service
sudo systemctl daemon-reload
sudo systemctl start fast_code_challenge.service
```

## II. Deployment (update new version)
### 1. Stop service
```bash
sudo systemctl stop fast_code_challenge.service
```
### 2. Cập nhật source code và cài đặt các gói python
```bash
cd /home/laptop029/fast-code-challenge
sudo rm -rf *
mkdir logs
** Copy source code vào /home/laptop029/fast-code-challenge
virtualenv venv --python='/usr/local/bin/python3.12'
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
deactivate
```

### 3. Start service
```bash
sudo systemctl start fast-code-challenge.service
```
