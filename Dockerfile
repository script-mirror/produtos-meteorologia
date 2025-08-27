FROM python:3.13

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

ARG GIT_USERNAME
ARG GIT_TOKEN

RUN sed -i "s/\${GIT_USERNAME}/${GIT_USERNAME}/g" requirements.txt && \
    sed -i "s/\${GIT_TOKEN}/${GIT_TOKEN}/g" requirements.txt

RUN git config --global credential.helper store && \
    echo "https://${GIT_USERNAME}:${GIT_TOKEN}@github.com" > ~/.git-credentials

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

ENV modelo=""
ENV data=""
ENV hora=""
ENV resolucao=""

ENTRYPOINT sh -c 'python main.py \
    --modelo_fmt "$modelo" \
    --data "$data" \
    --inicializacao "$hora" \
    --resolucao "$resolucao" \
    --sfc-prefix sfc \
    --pl-prefix pl'