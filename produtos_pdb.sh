docker run --rm -dit \
  -v /projetos/produtos-meteorologia:/app \
  -v /projetos/produtos-meteorologia/tmp:/app/tmp \
  -v /home/admin/.env:/root/.env \
  -v /WX2TB/Documentos:/WX2TB/Documentos \
  -v /projetos/arquivos/meteorologia:/projetos/arquivos/meteorologia \
  -e modelo=$modelo \
  -e data=$data \
  -e hora=$hora \
  -e resolucao=$resolucao \
  ubuntu tail -f /dev/null