mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p /workspace/miniconda3
rm -rf ~/miniconda3/miniconda.sh

/workspace/miniconda3/bin/conda  create -n hairfast python=3.10 -y
/workspace/miniconda3/bin/conda init bash
/workspace/miniconda3/bin/conda init zsh
source ~/.profile

/workspace/miniconda3/bin/conda activate hairfast

conda install ipykernel
ipython kernel install --user --name=hairfast

