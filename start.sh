 !/bin/bash 
rm /bin/sh && ln -s /bin/bash /bin/sh
apt update
apt install zip -y
apt install wget
apt install git
apt-get install -y git
# mkdir -p ~/miniconda3
# wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
# bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
# rm -rf ~/miniconda3/miniconda.sh
~/miniconda3/bin/conda init bash
~/miniconda3/bin/conda init zsh
source ~/.profile

conda  create -n hairfast python=3.10 -y
source activate hairfast
conda activate hairfast
curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash
apt-get install git-lfs
apt update
apt install zip -y
wget https://github.com/ninja-build/ninja/releases/download/v1.8.2/ninja-linux.zip
unzip ninja-linux.zip -d /usr/local/bin/
update-alternatives --install /usr/bin/ninja ninja /usr/local/bin/ninja 1 --force

