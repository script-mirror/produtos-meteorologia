#!/bin/bash

modelo=$1
data=$2
hora=$3
resolucao=$4
sfcprefix=$5
plprefix=$6
shift 6  # remove os 6 primeiros argumentos fixos
produtos="$@"  # tudo que sobrar vira lista de produtos

cmd="docker run --rm \
  -v /projetos/produtos-meteorologia:/app \
  -v /projetos/produtos-meteorologia/tmp:/app/tmp \
  -v /home/admin/.env:/root/.env \
  -v /WX2TB/Documentos:/WX2TB/Documentos \
  -v /projetos/arquivos/meteorologia:/projetos/arquivos/meteorologia \
  -v /usr/local/grads-2.0.2.oga.2/Contents/opengrads:/app/tmp/opengrads \
  -e modelo=$modelo \
  -e data=$data \
  -e hora=$hora \
  -e resolucao=$resolucao"

[ -n "$sfcprefix" ] && cmd="$cmd -e sfcprefix=$sfcprefix"
[ -n "$plprefix" ] && cmd="$cmd -e plprefix=$plprefix"
[ -n "$produtos" ] && cmd="$cmd -e produtos=\"$produtos\""

cmd="$cmd produtos"

eval $cmd
