FROM python:3.9

RUN export PATH=$PATH:/usr/local/bin

WORKDIR /app

COPY ./Pipfile /app/Pipfile
COPY ./Pipfile.lock /app/Pipfile.lock

RUN pip install pipenv && pipenv install

COPY . /app

#### Install docker
RUN apt-get update -y
RUN apt-get install ca-certificates curl gnupg lsb-release -y
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
RUN echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
RUN apt-get install docker.io -y

# Install kubectl
RUN curl -LO https://storage.googleapis.com/kubernetes-release/release/`curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt`/bin/linux/amd64/kubectl && \
    chmod +x ./kubectl && \
    mv ./kubectl /usr/local/bin/kubectl

CMD ["pipenv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "40080"]

## docker build -t k8s-pod-health . && docker run --rm -v //var/run/docker.sock:/var/run/docker.sock --name k8s-pod-health -p 40080:80 k8s-pod-health