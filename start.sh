#  !/bin/bash 
rm /bin/sh && ln -s /bin/bash /bin/sh
# apt update
# RUN conda  create -n hairfast python=3.10 -y
# RUN source activate hairfast
# RUN conda activate hairfast

apk update
apk add zip -y
apk add wget
apk add git
apk add build-essential
apk add -y git
curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash
apk add  git-lfs
apk add zip -y

# git clone https://huggingface.co/AIRI-Institute/HairFastGAN
# cd HairFastGAN && git lfs pull && cd ..
# mv HairFastGAN/pretrained_models pretrained_models
# mv HairFastGAN/input input
# rm -rf HairFastGAN

