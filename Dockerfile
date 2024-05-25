FROM pytorch/pytorch

WORKDIR /code

COPY . .

RUN chmod u+x ./start.sh
RUN source ./start.sh

RUN pip install -r requirements.txt

# CMD [ "python","serve.py" ]

