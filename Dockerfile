FROM python:3.13

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

ARG GIT_USERNAME
ARG GIT_TOKEN
ARG modelo
ARG data
ARG hora
ARG resolucao

RUN sed -i "s/\${GIT_USERNAME}/${GIT_USERNAME}/g" requirements.txt && \
    sed -i "s/\${GIT_TOKEN}/${GIT_TOKEN}/g" requirements.txt


RUN git config --global credential.helper store && \
    echo "https://${GIT_USERNAME}:${GIT_TOKEN}@github.com" > ~/.git-credentials

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app



CMD ["python", "main.py", "${modelo}", "${data}", "${hora}", "${resolucao}", "--sfc-prefix", "sfc", "--pl-prefix", "pl"]
