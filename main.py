
# Contando o tempo de execução
import time
from datetime import datetime
import argparse
start_time = time.time()

# Importando o módulo principal
from middle.meteorologia.processamento.produtos import ConfigProdutosPrevisaoCurtoPrazo, ConfigProdutosObservado
from middle.meteorologia.processamento.produtos import GeraProdutosPrevisao, GeraProdutosObservacao
from middle.meteorologia.processamento.pipelines import pipelines
from middle.meteorologia.consts.constants import CONSTANTES
from middle.utils import Constants

###################################################################################################################

shapefiles = [
    '/projetos/arquivos/meteorologia/Bacias_Hidrograficas_SIN.shp', 
    '/projetos/arquivos/meteorologia/estados_2010.shp',
]

###################################################################################################################

download_sfc_params = {

    'ecmwf-ens': {
        'type_ecmwf_opendata': ['cf', 'pf'],
        'levtype_ecmwf_opendata': 'sfc',
        'stream_ecmwf_opendata': 'enfo',
        'steps': [i for i in range(0, 366, 6)],
        'variables': ['tp', 'ttr'],
        'provedor_ecmwf_opendata': 'ecmwf'
    },

    'ecmwf-ens-membros': {
        # 'type_ecmwf_opendata': ['cf', 'pf'],
        # 'levtype_ecmwf_opendata': 'sfc',
        # 'stream_ecmwf_opendata': 'enfo',
        # 'steps': [i for i in range(0, 366, 6)],
        # 'variables': ['tp'],
        # 'provedor_ecmwf_opendata': 'ecmwf'
        'wait_members': True,
        'modelo_last_member': 'ecmwf-ens0p25',
        'last_member_file': '360.grib2'
    },

    'ecmwf': {
        'type_ecmwf_opendata': 'fc',
        'levtype_ecmwf_opendata': 'sfc',
        'stream_ecmwf_opendata': 'oper',
        'steps': [i for i in range(0, 366, 6)],
        'variables': ['tp', 'msl', '2t', 'ttr', '100u', '100v'],
        'provedor_ecmwf_opendata': 'ecmwf',
    },

    'ecmwf-aifs': {
        'type_ecmwf_opendata': 'fc',
        'levtype_ecmwf_opendata': 'sfc',
        'stream_ecmwf_opendata': 'oper',
        'steps': [i for i in range(0, 366, 6)],
        'variables': ['tp', 'msl'],
        'model_ecmwf_opendata': 'aifs-single',

    },

    'ecmwf-aifs-ens': {
        'type_ecmwf_opendata': ['cf', 'pf'],
        'levtype_ecmwf_opendata': 'sfc',
        'stream_ecmwf_opendata': 'enfo',
        'steps': [i for i in range(0, 366, 6)],
        'variables': ['tp'],
        'model_ecmwf_opendata': 'aifs-ens',

    },

    'ecmwf-aifs-ens-membros': {
        # 'type_ecmwf_opendata': ['cf', 'pf'],
        # 'levtype_ecmwf_opendata': 'sfc',
        # 'stream_ecmwf_opendata': 'enfo',
        # 'steps': [i for i in range(0, 366, 6)],
        # 'variables': ['tp'],
        # 'model_ecmwf_opendata': 'aifs-ens',
        'wait_members': True,
        'modelo_last_member': 'ecmwf-aifs-ens0p25',
        'last_member_file': '360.grib2'

    },

    'gefs': {
        'variables': '&var_ULWRF=on&var_APCP=on&var_PRMSL=on',
        'levels': '&lev_top_of_atmosphere=on&lev_surface=on&lev_mean_sea_level=on',
        'sub_region_as_gribfilter': '&subregion=&toplat=20&leftlon=240&rightlon=360&bottomlat=-60',        
    },

    'gefs-estendido': {
        'variables': '&var_ULWRF=on&var_APCP=on&var_PRMSL=on',
        'levels': '&lev_top_of_atmosphere=on&lev_surface=on&lev_mean_sea_level=on',
        'sub_region_as_gribfilter': '&subregion=&toplat=20&leftlon=240&rightlon=360&bottomlat=-60',       
        'steps': [i for i in range(0, 846, 6)]     
    },

    'gefs-estendido-membros': {
        'variables': '&var_APCP=on',
        'levels': '&lev_surface=on',
        'sub_region_as_gribfilter': '&subregion=&toplat=20&leftlon=240&rightlon=360&bottomlat=-60',       
        'steps': [i for i in range(0, 846, 6)]     
    },

    'gfs': {
        'variables': '&var_ULWRF=on&var_APCP=on&var_PRMSL=on&var_TMP=on&var_UGRD=on&var_VGRD=on',
        'levels': '&lev_top_of_atmosphere=on&lev_surface=on&lev_mean_sea_level=on&lev_2_m_above_ground=on&lev_100_m_above_ground=on',
        'sub_region_as_gribfilter': '&subregion=&toplat=20&leftlon=240&rightlon=360&bottomlat=-60', 
    },

    'gefs-membros': {
        'variables': '&var_APCP=on',
        'levels': '&lev_surface=on',
        'sub_region_as_gribfilter': '&subregion=&toplat=20&leftlon=240&rightlon=360&bottomlat=-60',
        'file_size': 0,  # Tamanho mínimo do arquivo para considerar que o download foi bem-sucedido        
    },

    'ecmwf-ens-estendido': {
        'last_member_file': None

    },

    'ecmwf-ens-estendido-membros': {
        'last_member_file': None

    },

}

download_pl_params = {

    'ecmwf': {
        'type_ecmwf_opendata': 'fc',
        'levtype_ecmwf_opendata': 'pl',
        'stream_ecmwf_opendata': 'oper',
        'steps': [i for i in range(0, 366, 6)],
        'variables': ['gh', 'u', 'v', 't', 'q'],
        'levlist_ecmwf_opendata': [1000, 925, 850, 700, 600, 500, 400, 300, 200]        
    },

    'ecmwf-aifs': {
        'type_ecmwf_opendata': 'fc',
        'levtype_ecmwf_opendata': 'pl',
        'stream_ecmwf_opendata': 'oper',
        'steps': [i for i in range(0, 366, 6)],
        'variables': ['gh'],
        'levlist_ecmwf_opendata': [500]        
    },

    'ecmwf-ens': {
        'type_ecmwf_opendata': 'em',
        'levtype_ecmwf_opendata': 'pl',
        'stream_ecmwf_opendata': 'enfo',
        'steps': [i for i in range(0, 366, 6)],
        'variables': ['gh'],
        'levlist_ecmwf_opendata': [500]        
    },

    'ecmwf-aifs-ens': {
        'type_ecmwf_opendata': 'em',
        'levtype_ecmwf_opendata': 'pl',
        'stream_ecmwf_opendata': 'enfo',
        'steps': [i for i in range(0, 366, 6)],
        'variables': ['gh'],
        'levlist_ecmwf_opendata': [500]         
    },

    'gfs': {
        'variables': '&var_HGT=on&var_UGRD=on&var_VGRD=on&var_SPFH=on&var_TMP=on',
        'levels': '&lev_1000_mb=on&lev_975_mb=on&lev_950_mb=on&lev_925_mb=on&lev_900_mb=on&lev_875_mb=on&lev_850_mb=on&lev_825_mb=on&lev_800_mb=on&lev_775_mb=on&lev_750_mb=on&lev_725_mb=on&lev_700_mb=on&lev_675_mb=on&lev_650_mb=on&lev_625_mb=on&lev_600_mb=on&lev_575_mb=on&lev_550_mb=on&lev_525_mb=on&lev_500_mb=on&lev_475_mb=on&lev_450_mb=on&lev_425_mb=on&lev_400_mb=on&lev_375_mb=on&lev_350_mb=on&lev_325_mb=on&lev_300_mb=on&lev_200_mb=on',
        'sub_region_as_gribfilter': '&subregion=&toplat=20&leftlon=240&rightlon=360&bottomlat=-60',
    },

    'gefs': {
        'variables': '&var_HGT=on&var_UGRD=on&var_VGRD=on&var_TMP=on',
        'levels': '&lev_top_of_atmosphere=on&lev_200_mb=on&lev_925_mb=on&lev_500_mb=on&lev_850_mb=on&lev_surface=on&lev_mean_sea_level=on',
        'sub_region_as_gribfilter': '&subregion=&toplat=20&leftlon=240&rightlon=360&bottomlat=-60',        
    },

    'gefs-estendido': {
        'variables': '&var_UGRD=on&var_VGRD=on',
        'levels': '&lev_925_mb=on&lev_850_mb=on',
        'sub_region_as_gribfilter': '&subregion=&toplat=20&leftlon=240&rightlon=360&bottomlat=-60',   
        'steps': [i for i in range(0, 846, 6)]      
    },

}

###################################################################################################################

open_model_params = {

    'ecmwf': {

        'tp_params': {
            'ajusta_acumulado': True,
            'm_to_mm': True,
            'sel_area': True,
        },

        'pl_params': {
            'sel_area': True,
        }

    },

    'ecmwf-ens': {

        'tp_params': {
            'ajusta_acumulado': True,
            'm_to_mm': True,
            'cf_pf_members': True,
            'sel_area': True,
        },

        'pl_params': {
            'sel_area': True,
            'expand_isobaric_dims': True,
        }

    },

    'ecmwf-ens-membros': {

        'tp_params': {
            'ajusta_acumulado': True,
            'm_to_mm': True,
            'cf_pf_members': True,
            'sel_area': True,
            'membros_prefix': True,
        },

        'pl_params': {
            'sel_area': True,
        }

    },

    'ecmwf-aifs': {

        'tp_params': {
            'ajusta_acumulado': True,
            'sel_area': True,
        },

        'pl_params': {
            'sel_area': True,
            'expand_isobaric_dims': True,
        }

    },

    'ecmwf-aifs-ens': {

        'tp_params': {
            'ajusta_acumulado': True,
            'm_to_mm': False,
            'cf_pf_members': True,
            'sel_area': True,
        },

        'pl_params': {
            'sel_area': True,
            'expand_isobaric_dims': True,
        }

    },

    'ecmwf-aifs-ens-membros': {

        'tp_params': {
            'ajusta_acumulado': True,
            'm_to_mm': False,
            'cf_pf_members': True,
            'sel_area': True,
            'membros_prefix': True,
        },

        'pl_params': {
            'sel_area': True,
            'expand_isobaric_dims': True,
        }

    },

    'gfs': {

        'tp_params': {
            'sel_area': True,
        },

        'pl_params': {
            'sel_area': True,
            'ajusta_longitude': True
        }

    },

    'gefs': {

        'tp_params': {
            'sel_area': True,
        },

        'pl_params': {
            'sel_area': True,
            'ajusta_longitude': True,
        }

    },

    'gefs-estendido': {

        'tp_params': {
            'sel_area': True,
        },

        'pl_params': {
            'sel_area': True,
            'ajusta_longitude': True,
        }

    },

    'gefs-estendido-membros': {

        'tp_params': {
            'sel_area': True,
            'arquivos_membros_diferentes': True,
        },

        'pl_params': {
            'sel_area': True,
            'ajusta_longitude': True,
        }

    },

    'gefs-membros': {

        'tp_params': {
            'arquivos_membros_diferentes': True,
            'sel_area': True,
            # 'membros_prefix': True,
        },

        'pl_params': {
            'sel_area': True,
        }

    },

    'ecmwf-ens-estendido': {

        'tp_params': {
            'ajusta_acumulado': True,
            'm_to_mm': True,
            'cf_pf_members': True,
            'sel_12z': True,
            'sel_area': True,
        },

        'pl_params': {
            'cf_pf_members': True,
            'sel_12z': True,
            'expand_isobaric_dims': True,
            'sel_area': False
        }
    },

    'ecmwf-ens-estendido-membros': {

        'tp_params': {
            'ajusta_acumulado': True,
            'm_to_mm': True,
            'cf_pf_members': True,
            'sel_12z': True,
            'sel_area': True,
        },

        'pl_params': {
            # 'cf_pf_members': True,
            # 'sel_12z': True,
            # 'expand_isobaric_dims': True,
            # 'sel_area': False
        }
    }

}

###################################################################################################################

# mapeamento nome->função (um "catálogo" de produtos)
def map_produtos(produtos=None, tipo='forecast'):

    if tipo == 'forecast':

        return {
            # Probabilidade / Climatologia
            "prob_clim": lambda: produtos.gerar_probabilidade_climatologia(ensemble=False, anomalia_sop=True),
            "prob_clim_membros": lambda: produtos.gerar_probabilidade_climatologia(ensemble=False),
            "prob_limiar": lambda: produtos.gerar_probabilidade_limiar(ensemble=False),
            "desvpad": lambda: produtos.gerar_desvpad(ensemble=False),

            # Semanas / Médias
            "semanas_op": lambda: produtos.gerar_semanas_operativas(extent=CONSTANTES['extents_mapa']['brasil'], add_valor_bacias=True),
            "semanas_op_anom_sop": lambda: produtos.gerar_semanas_operativas(extent=CONSTANTES['extents_mapa']['brasil'], add_valor_bacias=True, anomalia_sop=True),
            "semanas_op_membros": lambda: produtos.gerar_semanas_operativas(extent=CONSTANTES['extents_mapa']['brasil'], add_valor_bacias=False, ensemble=False),
            "media_bacia": lambda: produtos.gerar_media_bacia_smap(plot_graf=True, ensemble=True, salva_db=False),
            "media_bacia_membros": lambda: produtos.gerar_media_bacia_smap(plot_graf=False, ensemble=False, salva_db=False),

            # Chuva / Temperatura
            "prec24h": lambda: produtos.gerar_prec24h(extent=CONSTANTES['extents_mapa']['brasil']),
            "prec24h_biomassa": lambda: produtos.gerar_prec24h_biomassa(extent=CONSTANTES['extents_mapa']['biomassa']),
            "acum_total": lambda: produtos.gerar_acumulado_total(extent=CONSTANTES['extents_mapa']['brasil']),
            "acum_total_anom_mensal": lambda: produtos.gerar_acumulado_total(extent=CONSTANTES['extents_mapa']['brasil'], anomalia_mensal=True),
            "prec_pnmm_sop": lambda: produtos.gerar_prec_pnmm(margin_y=-90, resample_freq='sop'),
            "prec_pnmm": lambda: produtos.gerar_prec_pnmm(margin_y=-90),
            "dif_tp": lambda: produtos.gerar_diferenca_tp(extent=CONSTANTES['extents_mapa']['brasil']),
            "dif_tp_all": lambda: produtos.gerar_diferenca_tp(extent=CONSTANTES['extents_mapa']['brasil'], dif_01_15d=True, dif_15_final=True),

            # Estação Chuvosa
            "estacao_chuvosa_se": lambda: produtos.gerar_estacao_chuvosa(regiao_estacao_chuvosa='sudeste'),
            "estacao_chuvosa_no": lambda: produtos.gerar_estacao_chuvosa(regiao_estacao_chuvosa='norte'),

            # Dinâmica Atmosférica
            "jato200": lambda: produtos.gerar_jato_div200(margin_y=-90),
            "jato200_sop": lambda: produtos.gerar_jato_div200(margin_y=-90, resample_freq='sop'),
            "psi_sop": lambda: produtos.gerar_psi(margin_y=-90, extent=CONSTANTES['extents_mapa']['global'], central_longitude=180, figsize=(17, 17), resample_freq='sop', anomalia_mensal=True),
            "psi": lambda: produtos.gerar_psi(margin_y=-90, extent=CONSTANTES['extents_mapa']['global'], central_longitude=180, figsize=(17, 17)),
            "vento850_temp": lambda: produtos.gerar_vento_temp850(margin_y=-90),
            "vento850_temp_sop": lambda: produtos.gerar_vento_temp850(margin_y=-90, resample_freq='sop'),
            "vento850_div": lambda: produtos.gerar_vento_div850(margin_y=-90),
            "vento850_div_sop": lambda: produtos.gerar_vento_div850(margin_y=-90, resample_freq='sop'),
            "geop500": lambda: produtos.gerar_geop500(margin_y=-90),
            "geop500_sop": lambda: produtos.gerar_geop500(margin_y=-90, resample_freq='sop'),
            "geop500_sop_anom": lambda: produtos.gerar_geop500(margin_y=-90, resample_freq='sop', anomalia_sop=True, anomalia_mensal=True),
            "geop500_vort": lambda: produtos.gerar_geop_vort500(margin_y=-90),
            "geop500_vort_sop": lambda: produtos.gerar_geop_vort500(margin_y=-90, resample_freq='sop'),
            "ivt": lambda: produtos.gerar_ivt(margin_y=-90),
            "ivt_sop": lambda: produtos.gerar_ivt(margin_y=-90, resample_freq='sop'),
            "olr": lambda: produtos.gerar_olr(margin_y=-90),
            "olr_sop": lambda: produtos.gerar_olr(margin_y=-90, resample_freq='sop'),
            "frentes": lambda: produtos.gerar_frentes_frias(margin_y=-90, anomalia_frentes=True),
            "chuva_geop500_v850": lambda: produtos.gerar_chuva_geop500_vento850(extent=CONSTANTES['extents_mapa']['brasil']),
            "pnmm_vento850": lambda: produtos.gerar_pnmm_vento850(margin_y=-90),

            # Vento
            "mag_v100": lambda: produtos.gerar_mag_vento100(extent=CONSTANTES['extents_mapa']['brasil']),
            "mag_v100_sop": lambda: produtos.gerar_mag_vento100(extent=CONSTANTES['extents_mapa']['brasil'], resample_freq='sop'),

            # Gráficos
            "graf_chuva": lambda: produtos.gerar_graficos_chuva(),
            "graf_temp": lambda: produtos.gerar_graficos_temp(),
            "graf_v100": lambda: produtos.gerar_graficos_v100(),

            # Outros
            "salva_nc": lambda: produtos.salva_netcdf(variavel='tp'),
            "geada_inmet": lambda: produtos.gerar_geada_inmet(),
            "geada_cana": lambda: produtos.gerar_geada_cana(),
            "indices_itcz": lambda: produtos.gerar_indices_itcz(),
        }

    elif tipo == 'observed':

        return {
            "prec24h": lambda: produtos.gerar_prec24h(extent=CONSTANTES['extents_mapa']['brasil'], add_valor_bacias=True),
            "acumulado_mensal": lambda: produtos.gerar_acumulado_mensal(extent=CONSTANTES['extents_mapa']['brasil']),
            "dif_prev": lambda: produtos.gerar_dif_prev(tipo_plot='tp_db'),
            "bacias_smap": lambda: produtos.gerar_bacias_smap(salva_db=False),
            "temp_diario": lambda: produtos.gerar_temp_diario(extent=CONSTANTES['extents_mapa']['brasil']),
            "temp_mensal": lambda: produtos.gerar_temp_mensal(extent=CONSTANTES['extents_mapa']['brasil']),
        }

###################################################################################################################

def main():

    # dicionário mestre de produtos
    mapa = map_produtos()
    produtos_disponiveis = list(mapa.keys())

    parser = argparse.ArgumentParser(description="Processa inicialização de modelo meteorológico.")
    parser.add_argument("--modelo_fmt", help="Nome do modelo (ex: gfs, ecmwf, merge)")
    parser.add_argument("--data", help="Data no formato YYYY-MM-DD", default='')
    parser.add_argument("--inicializacao", help="Hora da inicialização (ex: 0, 12)", default='')
    parser.add_argument("--resolucao", help="Resolução do modelo (ex: 0p50, 1p00)", default='')
    parser.add_argument("--sfc-prefix", default='', help="Prefixo para superfície (ex: sfc)")
    parser.add_argument("--pl-prefix", default='', help="Prefixo para pressão em níveis (ex: pl)")
    
    # NOVO: escolher produtos específicos
    parser.add_argument("--produtos", nargs="+", help="Produtos disponíveis" + "\n".join(produtos_disponiveis))

    args = parser.parse_args()

    # valores que consideramos "vazios"
    null_values = (None, "", "null", "None", [""])

    # pega todos os argumentos como dicionário
    args_dict = vars(args)

    # Modelos observados
    modelos_observados = ['merge', 'samet']

    # verifica se todos, exceto `modelo_fmt`, estão "vazios"
    outros_vazios = all(
        args_dict[k] in null_values
        for k in args_dict if k != "modelo_fmt"
    )

    # Caso para rodar automaticamente apenas colocando o nome do modelo
    if outros_vazios:

        # Selecionando data e hora automaticamente
        DIA_ATUAL = datetime.now()
        DIA_ATUAL_FMT = DIA_ATUAL.strftime(f'%Y-%m-%d')
        HORA = DIA_ATUAL.hour        

        if args.modelo_fmt == 'pconjunto-ons':
            inicializacao = 0

        elif 'ecmwf' in args.modelo_fmt:

            if args.modelo_fmt == 'ecmwf-ens-estendido' or args.modelo_fmt == 'ecmwf-ens-estendido-membros':
                inicializacao = 0

            else:
                if HORA >= 0 and HORA < 16:
                    inicializacao = 0
                else:
                    inicializacao = 12

        else:

            if args.modelo_fmt == 'gefs-membros-estendido' or args.modelo_fmt == 'gefs-estendido':
                inicializacao = 0


            else:
                if HORA >= 0 and HORA < 6:
                    inicializacao = 0
                elif HORA >= 6 and HORA < 12:
                    inicializacao = 6
                elif HORA >= 12 and HORA < 18:
                    inicializacao = 12
                else:
                    inicializacao = 18

        args.data = DIA_ATUAL_FMT
        args.inicializacao = inicializacao if args.modelo_fmt not in modelos_observados else None

        # Resolução dependendo do modelo
        if args.modelo_fmt in ['gfs', 'gefs', 'gefs-membros', 'gefs-membros-estendido', 'gefs-estendido', 'pconjunto-ons', 'gefs-membros-estendido']:
            args.resolucao = '0p50'

        elif args.modelo_fmt in ['ecmwf', 'ecmwf-ens', 'ecmwf-ens-membros', 'ecmwf-aifs', 'ecmwf-aifs-ens', 'ecmwf-aifs-ens-membros', 'ecmwf-ens-estendido', 'ecmwf-ens-estendido-membros']:
            args.resolucao = '0p25'

        else:
            args.resolucao = None

        # Prefixos
        if args.modelo_fmt in ['gfs', 'gefs', 'ecmwf', 'ecmwf-ens', 'ecmwf-aifs', 'ecmwf-aifs-ens', 'gefs-estendido']:
            args.sfc_prefix = 'sfc'
            args.pl_prefix = 'pl'

        elif args.modelo_fmt in ['gefs-membros', 'gefs-membros-estendido', 'ecmwf-ens-membros', 'ecmwf-aifs-ens-membros', 'ecmwf-ens-estendido', 'ecmwf-ens-estendido-membros', 'pconjunto-ons']:
            args.sfc_prefix = 'sfc'
            args.pl_prefix = None

        else:
            args.sfc_prefix = None
            args.pl_prefix = None

    if args.inicializacao in null_values:
        args.inicializacao = None

    if args.resolucao in null_values:
        args.resolucao = None

    if args.sfc_prefix in null_values:
        args.sfc_prefix = None

    if args.pl_prefix in null_values:
        args.pl_prefix = None

    if args.produtos in null_values:
        args.produtos = None

    # Corrige caso tenha um único item com espaços
    if args.produtos is not None:
        if len(args.produtos) == 1 and " " in args.produtos[0]:
            args.produtos = args.produtos[0].split()

    print(args)
   
    if args.modelo_fmt not in modelos_observados:

        # Produtos de sfc
        produto_config_sf = ConfigProdutosPrevisaoCurtoPrazo(
            modelo=args.modelo_fmt,
            inicializacao=args.inicializacao,
            data=args.data,
            resolucao=args.resolucao,
            name_prefix=args.sfc_prefix if args.sfc_prefix else None
        )

        # Produtos de pl
        produto_config_pl = ConfigProdutosPrevisaoCurtoPrazo(
            modelo=args.modelo_fmt,
            inicializacao=args.inicializacao,
            data=args.data,
            resolucao=args.resolucao,
            name_prefix=args.pl_prefix if args.pl_prefix else None
        )

        # Configuração do produto
        produtos = GeraProdutosPrevisao(
            produto_config_sf=produto_config_sf, 
            produto_config_pl=produto_config_pl, 
            tp_params=open_model_params.get(args.modelo_fmt, {}).get('tp_params', {}), 
            pl_params=open_model_params.get(args.modelo_fmt, {}).get('pl_params', {}), 
            shapefiles=shapefiles
        )

        # dicionário mestre de produtos
        mapa = map_produtos(produtos)

        for variavel in [args.sfc_prefix, args.pl_prefix]:

            if variavel is None:
                continue

            if variavel == 'sfc':
                # Download dos arquivos sfc
                download_params = download_sfc_params.get(args.modelo_fmt, {})
                if download_params:
                    produto_config_sf.download_files_models(**download_params)

            elif variavel == 'pl':
                # Download dos arquivos pl
                download_params = download_pl_params.get(args.modelo_fmt, {})
                if download_params:
                    produto_config_pl.download_files_models(**download_params)

            else:
                # Download dos arquivos sfc
                download_params = download_sfc_params.get(args.modelo_fmt, {})
                if download_params:
                    produto_config_sf.download_files_models(**download_params)             

            # Executando os produtos
            if args.produtos:
                # Executa apenas os selecionados
                for p in args.produtos:
                    if p in mapa:
                        print(f"[INFO] Executando produto específico: {p}")
                        mapa[p]()
                    else:
                        print(f"[WARN] Produto '{p}' não encontrado no mapa.")

            else:
                # Executa pipeline completo
                for func in pipelines(modelo=args.modelo_fmt, produtos=produtos, tipo=variavel, hora=args.inicializacao):
                    if func is not None:
                        func()

        # Remove arquivos
        produtos.remove_files()

    else:

        if args.modelo_fmt == 'merge':
            output_path = Constants().PATH_DOWNLOAD_ARQUIVOS_MERGE
            
        elif args.modelo_fmt == 'samet':
            output_path = Constants().PATH_DOWNLOAD_ARQUIVOS_SAMET

        produto_config = ConfigProdutosObservado(
            modelo=args.modelo_fmt,
            data=args.data,
            output_path=output_path
        )

        produto_config.download_files()

        # Configuração do produto
        produtos = GeraProdutosObservacao(
            produto_config=produto_config,
            shapefiles=shapefiles,
        )

        # dicionário mestre de produtos
        mapa = map_produtos(produtos, tipo='observed')

        # Executando os produtos
        if args.produtos:
            # Executa apenas os selecionados
            for p in args.produtos:
                if p in mapa:
                    print(f"[INFO] Executando produto específico: {p}")
                    mapa[p]()
                else:
                    print(f"[WARN] Produto '{p}' não encontrado no mapa.")

        else:
            # Executa pipeline completo
            for func in pipelines(modelo=args.modelo_fmt, produtos=produtos):
                func()

###################################################################################################################

if __name__ == "__main__":
    main()
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Tempo de execução: {execution_time/60} minutos")

