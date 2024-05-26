FROM pytorch/conda-cuda

WORKDIR /code

COPY . .

RUN rm /bin/sh && ln -s /bin/bash /bin/sh
RUN conda create -n hairfast python=3.10 -y
SHELL ["conda","run","-n","hairfast","/bin/bash","-c"]
# RUN conda activate hairfast

RUN chmod u+x ./start.sh
RUN . ./start.sh

RUN pip install -r requirements.txt



# RUN pip install -r requirements.txt

# CMD [ "python","serve.py" ]

