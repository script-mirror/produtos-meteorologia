#!/bin/bash

# Argumentos obrigatórios
modelo=$1
data=$2
hora=$3
resolucao=$4

# Argumentos opcionais
produtos=$5
sfcprefix=$6
plprefix=$7

cmd="docker run --rm \
  -v /projetos/produtos-meteorologia:/app \
  -v /projetos/produtos-meteorologia/tmp:/app/tmp \
  -v /home/admin/.env:/root/.env \
  -v /WX2TB/Documentos:/WX2TB/Documentos \
  -v /projetos/arquivos/meteorologia:/projetos/arquivos/meteorologia \
  -e modelo=$modelo \
  -e data=$data \
  -e hora=$hora \
  -e resolucao=$resolucao"

# Só adiciona se existir
[ -n "$produtos" ] && cmd="$cmd -e produtos=$produtos"
[ -n "$sfcprefix" ] && cmd="$cmd -e sfcprefix=$sfcprefix"
[ -n "$plprefix" ] && cmd="$cmd -e plprefix=$plprefix"

cmd="$cmd produtos"

# Executa
eval $cmd
