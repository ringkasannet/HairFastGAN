FROM pytorch/conda-cuda

WORKDIR /code

COPY . .

RUN rm /bin/sh && ln -s /bin/bash /bin/sh
RUN conda create -n hairfast python=3.10 -y
RUN conda activate hairfast

RUN chmod u+x ./start.sh
RUN . ./start.sh




# RUN pip install -r requirements.txt

# CMD [ "python","serve.py" ]

