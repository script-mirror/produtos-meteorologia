# Produtos Meteorológicos

Sistema automatizado para processamento e geração de produtos meteorológicos baseado em modelos numéricos de previsão do tempo.

## Visão Geral

Este projeto é uma aplicação Python que processa dados de modelos meteorológicos (ECMWF, GFS, CFSv2, GEFS, entre outros) e gera produtos meteorológicos específicos como mapas de precipitação, análises atmosféricas, probabilidades climáticas e diversos outros produtos de apoio à tomada de decisão meteorológica.

## Características Principais

- **Processamento Automático**: Execução automatizada de produtos meteorológicos
- **Múltiplos Modelos**: Suporte para ECMWF, GFS, CFSv2, GEFS, CMC-ENS, ETA, MERGE, SAMET, CPC
- **Produtos Diversos**: Mais de 40 produtos meteorológicos diferentes
- **Containerização**: Suporte completo ao Docker
- **Análise de Bacias**: Integração com shapefiles para análises regionais

## Estrutura do Projeto

```
produtos-meteorologia/
├── main.py                 # Script principal
├── requirements.txt        # Dependências Python
├── Dockerfile             # Configuração do container
├── docker-compose.yml     # Orquestração Docker
├── produtos.sh           # Script de execução
├── produtos_build.sh     # Script de build
├── produtos_pdb.sh       # Script de debug
└── README.md            # Este arquivo
```

## Instalação

### Pré-requisitos

- Python 3.8+
- Docker (opcional, mas recomendado)
- Git

### Instalação Local

1. Clone o repositório:
```bash
git clone https://github.com/wx-middle/produtos-meteorologia.git
cd produtos-meteorologia
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

### Instalação com Docker

1. Configure as variáveis de ambiente no arquivo `.env`:
```bash
git_username=seu_usuario
git_token=seu_token
modelo=nome_do_modelo
data=2025-10-02
hora=00
resolucao=0p50
```

2. Execute o build:
```bash
./produtos_build.sh
```

3. Execute o container:
```bash
docker-compose up
```

## Uso

### Uso Básico

Execute o script principal com o modelo desejado:

```bash
python main.py --modelo_fmt ecmwf
```

### Uso Avançado

Especifique parâmetros personalizados:

```bash
python main.py --modelo_fmt ecmwf \
               --data 2025-10-02 \
               --inicializacao 00 \
               --resolucao 0p50 \
               --produtos prob_clim semanas_op prec24h
```

### Parâmetros Disponíveis

- `--modelo_fmt`: Nome do modelo (ecmwf, gfs, cfsv2, etc.)
- `--data`: Data no formato YYYY-MM-DD
- `--inicializacao`: Hora da inicialização (0, 6, 12, 18)
- `--resolucao`: Resolução do modelo (0p25, 0p50, 1p00)
- `--sfc-prefix`: Prefixo para arquivos de superfície
- `--pl-prefix`: Prefixo para arquivos de níveis de pressão
- `--produtos`: Lista de produtos específicos a serem gerados

## Produtos Disponíveis

### Produtos de Previsão (Forecast)

#### Probabilidade e Climatologia
- `prob_clim`: Probabilidade climatológica com anomalia SOP
- `prob_clim_cfsv2_12rod`: Probabilidade climatológica CFSv2 (12 rodadas)
- `prob_clim_cfsv2_28rod`: Probabilidade climatológica CFSv2 (28 rodadas)
- `prob_limiar`: Probabilidade por limiar
- `desvpad`: Desvio padrão

#### Semanas Operativas e Médias
- `semanas_op`: Semanas operativas com valores por bacia
- `prec_db`: Precipitação para banco de dados (semana + acumulado + 24h)
- `semanas_op_anom_sop`: Semanas operativas com anomalia SOP
- `semanas_op_anom_sop_cfsv2_12rod`: Semanas operativas CFSv2 12 rodadas com anomalia SOP
- `semanas_op_anom_sop_cfsv2_28rod`: Semanas operativas CFSv2 28 rodadas com anomalia SOP
- `semanas_op_membros`: Semanas operativas membros individuais
- `media_bacia`: Média por bacia SMAP com gráficos (ensemble)
- `media_bacia_membros`: Média por bacia SMAP membros individuais

#### Precipitação e Temperatura
- `prec24h`: Precipitação 24 horas
- `prec24h_biomassa`: Precipitação 24h para região de biomassa
- `acum_total`: Acumulado total com valores por bacia
- `acum_total_anom_mensal`: Acumulado total com anomalia mensal
- `prec_pnmm_sop`: Precipitação com pressão ao nível médio do mar (SOP)
- `prec_pnmm`: Precipitação com pressão ao nível médio do mar
- `dif_tp`: Diferença de precipitação total
- `dif_tp_all`: Diferença completa (1-15 dias e 15-final)

#### Estação Chuvosa
- `estacao_chuvosa_se`: Análise estação chuvosa região Sudeste
- `estacao_chuvosa_no`: Análise estação chuvosa região Norte

#### Dinâmica Atmosférica
- `jato200`: Corrente de jato e divergência 200 hPa
- `jato200_sop`: Corrente de jato 200 hPa (SOP)
- `psi_sop`: Função corrente 200 hPa com anomalia (SOP)
- `psi`: Função corrente 200 hPa
- `vento850_temp`: Vento e temperatura 850 hPa
- `vento850_temp_sop`: Vento e temperatura 850 hPa (SOP)
- `vento850_div`: Vento e divergência 850 hPa
- `vento850_div_sop`: Vento e divergência 850 hPa (SOP)
- `geop500`: Geopotencial 500 hPa
- `geop500_sop`: Geopotencial 500 hPa (SOP)
- `geop500_sop_anom`: Geopotencial 500 hPa com anomalia (SOP)
- `geop500_vort`: Geopotencial e vorticidade 500 hPa
- `geop500_vort_sop`: Geopotencial e vorticidade 500 hPa (SOP)
- `ivt`: Transporte integrado de vapor d'água
- `ivt_sop`: Transporte integrado de vapor (SOP)
- `olr`: Radiação de onda longa emergente
- `olr_sop`: Radiação de onda longa emergente (SOP)
- `frentes`: Análise de frentes frias com anomalias
- `chuva_geop500_v850`: Precipitação com geopotencial 500 e vento 850
- `pnmm_vento850`: Pressão nível mar com vento 850 hPa
- `anomalia_vento850`: Anomalia de vento 850 hPa (SOP mensal)

#### Análises CFSv2
- `sst_cfsv2_12rod`: Temperatura superfície do mar CFSv2 (12 rodadas)
- `sst_cfsv2_28rod`: Temperatura superfície do mar CFSv2 (28 rodadas)
- `psi_cfsv2_12rod`: Função corrente CFSv2 (12 rodadas)
- `psi_cfsv2_28rod`: Função corrente CFSv2 (28 rodadas)

#### Análises de Vento
- `mag_v100`: Magnitude do vento 100m
- `mag_v100_sop`: Magnitude do vento 100m (SOP)

#### Produtos Gráficos
- `graf_chuva`: Gráficos de precipitação
- `graf_temp`: Gráficos de temperatura
- `graf_v100`: Gráficos de vento 100m

#### Produtos Especializados
- `salva_nc`: Salva dados em formato NetCDF
- `geada_inmet`: Análise de geada baseada em dados INMET
- `geada_cana`: Análise de geada para cultura de cana-de-açúcar
- `indices_itcz`: Índices da Zona de Convergência Intertropical
- `vento_weol`: Análise de vento para energia eólica

### Produtos Observacionais (Observed)

#### Precipitação Observada
- `prec24h`: Precipitação 24h observada com valores por bacia
- `acumulado_mensal`: Acumulado mensal observado com valores por bacia
- `dif_prev`: Diferença entre previsão e observação
- `bacias_smap`: Análise por bacias hidrográficas SMAP

#### Temperatura Observada
- `temp_diario`: Temperatura diária observada
- `temp_mensal`: Temperatura mensal observada

## Modelos Suportados

### Modelos de Previsão
- **ECMWF**: European Centre for Medium-Range Weather Forecasts
- **ECMWF-ENS**: Ensemble ECMWF
- **ECMWF-AIFS**: Artificial Intelligence Forecasting System
- **GFS**: Global Forecast System
- **GEFS**: Global Ensemble Forecast System
- **CFSv2**: Climate Forecast System version 2
- **CMC-ENS**: Canadian Meteorological Centre Ensemble
- **ETA**: Modelo ETA regional

### Modelos Observacionais
- **MERGE**: Dados de precipitação observada
- **SAMET**: Sistema de Análise Meteorológica
- **CPC**: Climate Prediction Center

## Configuração de Ambiente

O projeto utiliza variáveis de ambiente para configuração. Configure seu arquivo `.env`:

```bash
# Credenciais Git (para dependências privadas)
git_username=seu_usuario_git
git_token=seu_token_git

# Configurações do modelo
modelo=ecmwf
data=2025-10-02
hora=00
resolucao=0p50

# Prefixos opcionais
sfcprefix=sfc
plprefix=pl
```

## Scripts de Conveniência

- **produtos.sh**: Execução padrão do sistema
- **produtos_build.sh**: Build do container Docker
- **produtos_pdb.sh**: Execução com debugger

## Dependências Principais

- **middle-meteorologia**: Biblioteca principal de processamento
- **geopandas**: Manipulação de dados geoespaciais
- **xarray**: Arrays multidimensionais
- **cartopy**: Projeções cartográficas
- **matplotlib**: Visualização
- **ecmwf-opendata**: Interface para dados ECMWF
- **metpy**: Cálculos meteorológicos

## Licença

Este projeto é propriedade da WX-Middle. Todos os direitos reservados.

## Suporte

Para suporte técnico ou dúvidas sobre o projeto, entre em contato com a equipe de desenvolvimento.

## Changelog

### v1.0.0
- Implementação inicial do sistema
- Suporte para modelos ECMWF, GFS, CFSv2
- Produtos básicos de precipitação e análise atmosférica
- Integração com Docker

---

*Última atualização: Outubro 2025*