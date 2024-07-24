FROM python:3.11.7-alpine3.17
WORKDIR /NightWing

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD ["flask", "run", "--host=0.0.0.0"]