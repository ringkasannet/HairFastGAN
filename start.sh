#  !/bin/bash 
rm /bin/sh && ln -s /bin/bash /bin/sh
# apt update
# RUN conda  create -n hairfast python=3.10 -y
# RUN source activate hairfast
# RUN conda activate hairfast

sudo apt update
sudo apt install apt

apt-get update
apt-get install zip -y
apt-get install wget
apt-get install git
apt-get install build-essential
apt-get install -y git
curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash
apt-get install git-lfs
apt-get install zip -y

# git clone https://huggingface.co/AIRI-Institute/HairFastGAN
# cd HairFastGAN && git lfs pull && cd ..
# mv HairFastGAN/pretrained_models pretrained_models
# mv HairFastGAN/input input
# rm -rf HairFastGAN

