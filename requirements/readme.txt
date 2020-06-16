pip download -d pkgs -r requirements.txt
pip install --no-index --find-links=pkgs -r requirements.txt

安装sshpass:
tar -zxvf sshpass-1.06.tar.gz
cd sshpass-1.06
./configure
sudo make
sudo make install