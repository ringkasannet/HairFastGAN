#  !/bin/bash 
rm /bin/sh && ln -s /bin/bash /bin/sh
# apt update
# RUN conda  create -n hairfast python=3.10 -y
# RUN source activate hairfast
# RUN conda activate hairfast

apt update
apt install zip -y
apt install wget
apt install git
apt install build-essential
apt install -y git
curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash
apt install git-lfs


# git clone https://huggingface.co/AIRI-Institute/HairFastGAN
# cd HairFastGAN && git lfs pull && cd ..
# mv HairFastGAN/pretrained_models pretrained_models
# mv HairFastGAN/input input
# rm -rf HairFastGAN

