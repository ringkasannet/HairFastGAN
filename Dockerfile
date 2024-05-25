FROM pytorch/conda-cuda

WORKDIR /code

COPY . .

RUN chmod u+x ./start.sh
RUN . ./start.sh




RUN pip install -r requirements.txt

# CMD [ "python","serve.py" ]

