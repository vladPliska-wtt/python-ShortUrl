FROM python:3
ENV PYTHONUNBUFFERED=1
COPY . /app
WORKDIR /app
COPY requirements.txt /
RUN pip3 install -r ./requirements.txt
#COPY manage.py /
#RUN python manage.py migrate
COPY . /
