FROM pytorch/pytorch/conda-cuda

WORKDIR /code

COPY . .

RUN rm /bin/sh && ln -s /bin/bash /bin/sh
RUN 
RUN chmod u+x ./setconda.sh
RUN bash -i ./setconda.sh

RUN chmod u+x ./start.sh
RUN . ./start.sh




# RUN pip install -r requirements.txt

# CMD [ "python","serve.py" ]

