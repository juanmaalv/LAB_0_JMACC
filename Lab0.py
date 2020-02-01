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

#%% -- ------------------------------------------------------------- Importar con funciones -- #
import funciones as fn
import visualizaciones as vs
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# -- --------------------------------------------------------- Descargar precios de OANDA -- #

#%% token de OANDA
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

#%% multiplicador de precios
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

df_pe['mes'] = [df_pe['TimeStamp'][i].month for i in range(0, len(df_pe['TimeStamp']))]

#%% -- 02: Sesion de la vela.
df_pe["sesion"] = np.zeros(len(df_pe['High']))

for i in range(1, len(df_pe['High'])):
    
    if  df_pe["hora"] > 21 or df_pe["hora"] <8:
        df_pe['sesion'][i] = "asia"
        
    elif  df_pe["hora"] == 0:
        df_pe['sesion'][i] = "asia_europa"
        
    elif  df_pe["hora"] > 8 and df_pe["hora"] <13:
        df_pe['sesion'][i] = "europa"
        
    elif  df_pe["hora"] > 12 and df_pe["hora"] <17:
        df_pe['sesion'][i] = "europa_america"
        
    else:
        df_pe['sentido_c'][i] = "america"


#%% -- 03: Amplitud OC esperada de vela para cualquier dia de la semana (Dist de Freq).
df_pe['oc'] = [pip_mult*(float(df_pe['Close'][i])-float(df_pe['Open'][i])) for i in range(0, len(df_pe['Close']))]

#%% -- 04: Amplitud HL esperada de vela para cualquier dia de la semana (Dist de Freq).
df_pe['hl'] = [pip_mult*(float(df_pe['High'][i])-float(df_pe['Low'][i])) for i in range(0, len(df_pe['High']))]

#%% -- 05: Evolucion de velas consecutivas (1: Alcistas, 0: Bajistas).
df_pe["sentido"] = np.where(df_pe["oc"] > 0, 1, 0)

#%% -- 06: Maxima evolucion esperada de velas consecutivas (Dist Acum de Freq).
df_pe["sentido_c"] = np.zeros(len(df_pe['High']))

for i in range(1, len(df_pe['High'])):
    
    if  df_pe['sentido'][i] == df_pe['sentido'][i-1]:
        df_pe['sentido_c'][i] = df_pe['sentido_c'][i-1]+1
        
    else:
        df_pe['sentido_c'][i] = 0

#%% -- 07 Volatilidad Móvil

df_pe["volatilidad5"] = [df_pe.iloc[i-5:i,9].std() for i in range(0, len(df_pe['High']))]
df_pe["volatilidad25"] = [df_pe.iloc[i-25:i,9].std() for i in range(0, len(df_pe['High']))]
df_pe["volatilidad50"] = [df_pe.iloc[i-50:i,9].std() for i in range(0, len(df_pe['High']))]
        

#%% -- 08: Calculo + Grafica autopropuesta.

fig = px.histogram(df_pe, x= "sentido_c",
                   title='Histograma de repetición de tendencias',
                   labels={'# de días'}, # can specify one label per df column
                           )
fig.update_layout(
    xaxis_title_text='Días Consecutivos Con Misma Tendencia', # xaxis label
    yaxis_title_text='Frecuencia', # yaxis label
    )
    
    
fig.show()

