!/bin/bash 
rm /bin/sh && ln -s /bin/bash /bin/sh
apt-get update
apt-get install zip -y
apt-get install wget
curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash
apt-get install git-lfs

mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p /workspace/miniconda3
rm -rf ~/miniconda3/miniconda.sh

/workspace/miniconda3/bin/conda  create -n hairfast python=3.10 -y
/workspace/miniconda3/bin/conda init bash
/workspace/miniconda3/bin/conda init zsh
source ~/.profile

/workspace/miniconda3/bin/conda  create -n hairfast python=3.10 -y
/workspace/miniconda3/bin/activate hairfast
/workspace/miniconda3/bin/conda install ipykernel
ipython kernel install --user --name=hairfast

wget https://github.com/ninja-build/ninja/releases/download/v1.8.2/ninja-linux.zip
unzip ninja-linux.zip -d /usr/local/bin/
update-alternatives --install /usr/bin/ninja ninja /usr/local/bin/ninja 1 --force

git clone https://huggingface.co/AIRI-Institute/HairFastGAN
cd HairFastGAN && git lfs pull && cd ..
mv HairFastGAN/pretrained_models pretrained_models
mv HairFastGAN/input input
rm -rf HairFastGAN

pip install -r requirements.txt