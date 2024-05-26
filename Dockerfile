FROM runpod/pytorch:2.0.1-py3.10-cuda11.8.0-devel-ubuntu22.04

WORKDIR /code

COPY . .

RUN rm /bin/sh && ln -s /bin/bash /bin/sh

RUN chmod u+x ./setconda.sh
RUN bash -i ./setconda.sh

RUN chmod u+x ./start.sh
RUN . ./start.sh




# RUN pip install -r requirements.txt

# CMD [ "python","serve.py" ]

