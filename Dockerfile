FROM 3.9-slim-buster

WORKDIR /Autoscaler

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python","./main.py"]