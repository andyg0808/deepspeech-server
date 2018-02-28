FROM python:3

RUN pip install --no-cache-dir pipenv

# Derived from Docker docs
RUN apt-get update && apt-get install -y \
  libsox2

RUN apt-get install

WORKDIR /usr/src/app

COPY Pipfile .
COPY Pipfile.lock .
RUN pipenv install --system

COPY . .

#RUN python ./taskcluster.py --target=native --arch=cpu
ENV FLASK_APP=server.py

EXPOSE 80
CMD ["flask", "run", "--host=0.0.0.0", "--port=80"]
