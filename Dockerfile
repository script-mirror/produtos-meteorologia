FROM python:3.11

WORKDIR /app

# RUN http://downloads.sourceforge.net/project/opengrads/grads2/2.0.2.oga.1/Linux/grads-2.0.2.oga.1-bundle-x86_64-unknown-linux-gnu.tar.gz
# RUN tar -vzxf grads-2.0.2.oga.1-bundle-x86_64-unknown-linux-gnu.tar.gz
# RUN cd grads-2.0.2.oga.1
# RUN export PATH=$PATH:$HOME/grads-2.0.2.oga.1/bin
# RUN source ~/.bashrc

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

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

ENV modelo=""
ENV data=""
ENV hora=""
ENV resolucao=""
ENV produtos=""
ENV sfcprefix=""
ENV plprefix=""
ENV PYTHONUNBUFFERED=1

ENTRYPOINT sh -c 'python main.py \
    --modelo_fmt "$modelo" \
    --data "$data" \
    --inicializacao "$hora" \
    --resolucao "$resolucao" \
    --sfc-prefix "$sfcprefix" \
    --pl-prefix "$plprefix" \
    --produtos "$produtos" \
    '