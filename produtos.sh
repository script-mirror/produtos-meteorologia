docker run --rm \
  -v ./:/app \
  -v ./tmp:/app/tmp \
  -v /home/admin/.env:/root/.env \
  -v /WX2TB/Documentos:/WX2TB/Documentos \
  -v /projetos/arquivos/meteorologia:/projetos/arquivos/meteorologia \
  -e modelo=$modelo \
  -e data=$data \
  -e hora=$hora \
  -e resolucao=$resolucao \
  -e produtos \
  -e sfcprefix \
  -e plprefix \
  produtos