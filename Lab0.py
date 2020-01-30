# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 09:58:59 2020

@author: juanm
"""


# -- ------------------------------------------------------------------------------------ -- #
# -- Proyecto: Describir brevemente el proyecto en general                                -- #
# -- Codigo: RepasoPython.py - describir brevemente el codigo                             -- #
# -- Repositorio: https://github.com/                                                     -- #
# -- Autor: Nombre de autor                                                               -- #
# -- ------------------------------------------------------------------------------------ -- #

# -- ------------------------------------------------------------- Importar con funciones -- #
import funciones as fn
import visualizaciones as vs

import pandas as pd

# -- --------------------------------------------------------- Descargar precios de OANDA -- #

# token de OANDA
OA_Ak = '630eb7b990acb33732bc201e28bf0d80-52218bf769c37309bee9440932b0f008'
OA_In = "EUR_USD"                  # Instrumento
OA_Gn = "D"                       # Granularidad de velas
fini = pd.to_datetime("2019-01-06 00:00:00").tz_localize('GMT')  # Fecha inicial
ffin = pd.to_datetime("2019-12-06 00:00:00").tz_localize('GMT')  # Fecha final

df_pe = fn.f_precios_masivos(p0_fini=fini, p1_ffin=ffin, p2_gran=OA_Gn,
                             p3_inst=OA_In, p4_oatk=OA_Ak, p5_ginc=4900)

# -- --------------------------------------------------------------- Graficar OHLC plotly -- #

vs_grafica1 = vs.g_velas(p0_de=df_pe.iloc[0:120, :])
vs_grafica1.show()

# -- ------------------------------------------------------------------- Conteno de velas -- #

# multiplicador de precios
pip_mult = 10000

# -- 0A.1: Hora
df_pe['hora'] = [df_pe['TimeStamp'][i].hour for i in range(0, len(df_pe['TimeStamp']))]

# -- 0A.2: Dia de la semana.
df_pe['dia'] = [df_pe['TimeStamp'][i].weekday() for i in range(0, len(df_pe['TimeStamp']))]

# -- 0B: Boxplot de amplitud de velas (close - open).
df_pe['co'] = (df_pe['Close'] - df_pe['Open'])*pip_mult

# -- ------------------------------------------------------------ Graficar Boxplot plotly -- #
vs_grafica2 = vs.g_boxplot_varios(p0_data=df_pe[['co']], p1_norm=False)
vs_grafica2.show()


#%%# -- 01: Mes de la vela.

df_pe['Mes'] = [df_pe['TimeStamp'][i].month for i in range(0, len(df_pe['TimeStamp']))]

# -- 02: Sesion de la vela.





# -- 03: Amplitud OC esperada de vela para cualquier dia de la semana (Dist de Freq).
# -- 04: Amplitud HL esperada de vela para cualquier dia de la semana (Dist de Freq).
# -- 05: Evolucion de velas consecutivas (1: Alcistas, 0: Bajistas).
# -- 06: Maxima evolucion esperada de velas consecutivas (Dist Acum de Freq).
# -- 07: Calculo + Grafica autopropuesta.
