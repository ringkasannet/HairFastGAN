FROM runpod/pytorch:2.0.1-py3.10-cuda11.8.0-devel-ubuntu22.04


WORKDIR /code

COPY . .

RUN conda  create -n hairfast python=3.10 -y
RUN source activate hairfast
RUN conda activate hairfast
RUN wget / git / zip

# RUN chmod u+x ./start.sh
# RUN . ./start.sh




# RUN pip install -r requirements.txt

# CMD [ "python","serve.py" ]

