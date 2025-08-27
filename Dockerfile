FROM python:3.11

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
        ffmpeg \
        tzdata \
        xvfb \
        locales \
    && ln -sf /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime \
    && echo "America/Sao_Paulo" > /etc/timezone \
    && rm -rf /var/lib/apt/lists/*

RUN sed -i 's/# pt_BR.UTF-8 UTF-8/pt_BR.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen

ENV LANG=pt_BR.UTF-8 \
    LC_ALL=pt_BR.UTF-8 \
    TZ=America/Sao_Paulo


COPY ./requirements.txt /app/requirements.txt

ARG GIT_USERNAME
ARG GIT_TOKEN

RUN sed -i "s/\${GIT_USERNAME}/${GIT_USERNAME}/g" requirements.txt && \
    sed -i "s/\${GIT_TOKEN}/${GIT_TOKEN}/g" requirements.txt

RUN git config --global credential.helper store && \
    echo "https://${GIT_USERNAME}:${GIT_TOKEN}@github.com" > ~/.git-credentials

RUN pip install -r requirements.txt

COPY . /app

ENV modelo=""
ENV data=""
ENV hora=""
ENV resolucao=""
ENV produtos=""
ENV sfcprefix=""
ENV plprefix=""

ENTRYPOINT sh -c 'python main.py \
    --modelo_fmt "$modelo" \
    --data "$data" \
    --inicializacao "$hora" \
    --resolucao "$resolucao" \
    --sfc-prefix "$sfcprefix" \
    --pl-prefix "$plprefix" \
    --produtos "$produtos" \
    '