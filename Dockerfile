FROM runpod/pytorch:2.0.1-py3.10-cuda11.8.0-devel-ubuntu22.04


WORKDIR /code

COPY . .

RUN rm /bin/sh && ln -s /bin/bash /bin/sh

RUN chmod u+x ./start.sh
RUN ./start.sh

RUN wget https://github.com/ninja-build/ninja/releases/download/v1.8.2/ninja-linux.zip
RUN unzip ninja-linux.zip -d /usr/local/bin/

RUN update-alternatives --install /usr/bin/ninja ninja /usr/local/bin/ninja 1 --force


RUN conda create -n hairfast python=3.10 -y
SHELL ["conda","run","-n","hairfast","/bin/bash","-c"]
# RUN conda activate hairfast


RUN pip install -r requirements.txt



# RUN pip install -r requirements.txt

# CMD [ "python","serve.py" ]

