#  !/bin/bash 
rm /bin/sh && ln -s /bin/bash /bin/sh
# apt update
# RUN conda  create -n hairfast python=3.10 -y
# RUN source activate hairfast
# RUN conda activate hairfast

apt-get update
apt-get install zip -y
apt-get install wget
apt-get install git
apt-get install build-essential
apt-get install -y git
conda install ipykernel
ipython kernel install --user --name=hairfast
curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash
apt-get install git-lfs
apt-get install zip -y
wget https://github.com/ninja-build/ninja/releases/download/v1.8.2/ninja-linux.zip
unzip ninja-linux.zip -d /usr/local/bin/
update-alternatives --install /usr/bin/ninja ninja /usr/local/bin/ninja 1 --force


# git clone https://huggingface.co/AIRI-Institute/HairFastGAN
# cd HairFastGAN && git lfs pull && cd ..
# mv HairFastGAN/pretrained_models pretrained_models
# mv HairFastGAN/input input
# rm -rf HairFastGAN

