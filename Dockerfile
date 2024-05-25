FROM pytorch/pytorch

WORKDIR /code

COPY . .

RUN chmod u+x ./start.sh
RUN . ./start.sh

RUN mkdir -p ~/miniconda3
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
RUN bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
RUN rm -rf ~/miniconda3/miniconda.sh
RUN ~/miniconda3/bin/conda init bash
RUN ~/miniconda3/bin/conda init zsh
RUN source ~/.profile

RUN conda  create -n hairfast python=3.10 -y
RUN source activate hairfast
RUN conda activate hairfast


RUN pip install -r requirements.txt

# CMD [ "python","serve.py" ]

