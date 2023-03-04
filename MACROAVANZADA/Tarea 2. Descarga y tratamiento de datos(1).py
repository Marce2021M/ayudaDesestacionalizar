#!/usr/bin/env python
# coding: utf-8

# # Hechos estilizados del ciclo económico Mexicano
# 
# En un cuaderno anterior analizábamos las propiedades del ciclo económico en Estados Unidos desde 1947. 
# 
# En este cuaderno vamos a analizar las características del ciclo económico Mexicano, comparándolas con el de Estados Unidos desde 1993, fecha desde la que podemos encontrar contabilidad nacional por el lado del gasto en México.
# 
# Tomamos datos de consumo e inversión, privados y del gobierno, consumo en bienes duraderos, no duraderos y de servicios, inversión en edificios, estructuras y equipo para México. Vamos a descargar datos sin ajustar estacionalmente en pesos nominales trimestrales y en pesos reales trimestrales, ya que con la ratio de ambos obtenermos los índices de precios. La OCDE tiene datos desde el primer trimestre de 1993. 
# 
# Tomamos datos de las mismas variables para Estados Unidos de la página del "Bureau of Economic Analysis", pero hay que mencionar que los datos de Estados Unidos solo están disponibles como índices encadenados. El Buró de Análisis Económico tiene datos comparables con México desde 2002 sin ajustar estacionalmente, pero es un periodo complicado, sólo 5 años antes de la Gran Recesión, que nos deja solo 8 años antes del Gran Confinamiento, aunque no quiere decir que no podamos hacerlo, pero teniendo esto en mente.
# 
# En este cuaderno vamos a comparar también los mercados laborales de México y Estados Unidos. Para eso vamos a usar datos de población de más de 15 años empleada, desempleada y autoempleada usando una variedad de datos de la OCDE, del Buró de Servicios Laborales de Estados Unidos y el Instituto Nacional de Estadística y Geografía Mexicano.
# 
# ## Carga y procesamiento de todos los datos
# Vamos cargar primero todos los datos anuales y mensuales que usaremos posteriormente y los vamos a ajustar estacionalmente y a salvar para que puedan ser posteriormente utilizados y no tener que desestacionalizarlos de vuelta.

# In[19]:


# Cargamos librerías
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Cargamos datos
import os
os.chdir('/home/MACROAVANZADA') #directorio de la carpeta
## Datros trimestrales

### Datos para México
#### Contabilidad Nacional
mex_qnaq = pd.read_excel('MEXqna_nsa.xlsx', sheet_name='Deflactados')
mex_qnap = pd.read_excel('MEXqna_nsa.xlsx', sheet_name='precios')

#### También cargamos datos sobre inversion y consumo duradero nacional
#### e importado
###mex_qna_imp = pd.read_excel('MEXqna_nsa.xlsx', sheet_name='importados')

#### Mercados laborales trimestrales (nos encargaremos de los mensuales más
#### adelante)
mex_trab = pd.read_excel('MEXqna_nsa.xlsx', sheet_name='trabajo')

## Datos mensuales
### México
mex_trabm = pd.read_excel('MEXqna_nsa.xlsx', sheet_name='mensuales')


# Vamos aplicar un ajuste estacional a todos los datos para garantizar que no exista ningún patrón de estacionalidad y salvar los datos para que puedan usarse posteriormente en situaciones en las que no podemos desestacionalizar datos.
# 
# Primero creamos índices temporales:


T = len(mex_qnaq['PC'])
idx = pd.date_range('1993-03-01', periods=T, freq='Q')

# Primero establecemos el índice temporal para las series de contabilidad
# nacional de Estados Unidos y México desde 1993-Q1
mex_qnaq = mex_qnaq.set_index(idx)
mex_qnap = mex_qnap.set_index(idx)
###mex_qna_imp = mex_qna_imp.set_index(idx)
# Usamos un índice distinto para los datos laborales trimestrales de 
# México porque empiezan en 2005-Q1
T = len(mex_trab['POP'])
idx = pd.date_range('2005-03-01', periods=T, freq='Q')
mex_trab = mex_trab.set_index(idx)

# También asignamos índices a los datos mensuales
## México
T = len(mex_trabm['POP'])
idx = pd.date_range('2005-01-01', periods=T, freq='M')
mex_trabm = mex_trabm.set_index(idx)



mex_qnaq_sa = pd.DataFrame(index=mex_qnaq.index, columns=mex_qnaq.columns)


# Con esto tenemos suficiente para eliminar la estacionalidad de todas las series y crear las economías que necesitamos.
# 
# ### Eliminando la estacionalidad de las series trimestrales y mensuales
# Primero vamos a eliminar la estacionalidad de las series y salvarlas, para que así podamos usar los datos en otras plataformas.


import statsmodels.api as sm
import warnings
warnings.filterwarnings('ignore')
x13path = './'


mex_qnaq_sa = pd.DataFrame(index=mex_qnaq.index, columns=mex_qnaq.columns)
mex_qnap_sa = pd.DataFrame(index=mex_qnap.index, columns=mex_qnap.columns)

mex_trab_sa = pd.DataFrame(index=mex_trab.index, columns=mex_trab.columns)

mex_trabm_sa = pd.DataFrame(index=mex_trabm.index, columns=mex_trabm.columns)


for col in mex_qnaq.columns:
    x = sm.tsa.x13_arima_analysis(
        endog=mex_qnaq[col].dropna(),
        x12path=x13path,
        prefer_x13=True,
        freq='Q',
        outlier=False,
        trading=False,
        log=True
    )
    mex_qnaq_sa[f'{col}'] = x.seasadj


    
    
for col in mex_qnap.columns:
    x = sm.tsa.x13_arima_analysis(
        endog=mex_qnap[col].dropna(),
        x12path=x13path,
        prefer_x13=True,
        freq='Q',
        outlier=False,
        trading=False,
        log=True
    )
    mex_qnap_sa[f'{col}'] = x.seasadj


for col in mex_trab.columns:
    x = sm.tsa.x13_arima_analysis(
        endog=mex_trab[col].dropna(),
        x12path=x13path,
        prefer_x13=True,
        freq='Q',
        outlier=False,
        trading=False,
        log=True
    )
    mex_trab_sa[f'{col}'] = x.seasadj
    
# También ajustamos estacionalmente los datos mensuales
for col in mex_trabm.columns:
    x = sm.tsa.x13_arima_analysis(
        endog=mex_trabm[col].dropna(),
        x12path=x13path,
        prefer_x13=True,
        freq='M',
        outlier=False,
        trading=False,
        log=True
    )
    mex_trabm_sa[f'{col}'] = x.seasadj
    


T = len(mex_price_month['PE'])
idx = pd.date_range('1993-01-01', periods=T, freq='M')
mex_price_month_sa = pd.DataFrame(index=idx, columns=mex_price_month.columns)

# También desestacionalizamos los datos mensuales de consumo, inversión...

mex_qnaq['DC'].plot()
mex_qnaq_sa['DC'].plot()


# Ahora podemos salvar la información para usarla posteriormente

# In[13]:


mex_qnaq_sa.to_excel('mex_qnaq_sa.xlsx')
mex_qnap_sa.to_excel('mex_qnap_sa.xlsx')
mex_trab_sa.to_excel('mex_trab_sa.xlsx')
mex_trabm_sa.to_excel('mex_trabm_sa.xlsx')
mex_qna_month_sa.to_excel('mex_qna_month.xlsx')


# ### Creación de economías
# Vamos a crear tres tipos de economías privadas. En la primera no consideramos el sector exterior, en la segunda consideramos el sector exterior a través de la balanza comercial, pero como debemos asignarla a consumo, inversión o una combinación de ambas, decidimos asignar toda la balanza comercial como inversión. La última economía asigna la balanza comercial al consumo. Hago estos dos supuestos porque no sabemos dentro del modelo neoclásico de un sector porque solo sabemos que la balanza comercial es la diferencia entre ahorro e inversión.
# 
# En las tres economías consideramos que solo hay un sector y que el deflactor del consumo no duradero funge como numerario de la economía. Además el consumo duradero es considerado inversión y se imputan ciertos servicios que redundan en el PIB y el consumo no duradero y de servicios de la economía.
# 
# El consumo semiduradero es considerado directamente consumo no duradero, poque a pesar de tener un comportamiento casi igual de volatil que el consumo no duradero, no cumple un papel tan distinto que el consumo no duradero. Podría ser interesante estudiar más detalladamente lo que es consumo o una inversión para el hogar. Un buen proyecto sería estudiar qué papel juega cada insumo en el hogar con una tecnología de producción doméstica que combine elementos como consumo no duradero, bienes duraderos y semiduraderos, tiempo y energía o algún tipo de combustible. 
# 
# Igualmente podemos pensar en la utildad derivada del ocio como función de tiempo, pero también de bienes y servicios. Esto requeriría de una discusión demasiado larga y mucho trabajo --construir una contabilidad nacional de los hogares, por lo que lo dejaremos para una ocasión posterior.
# 
# #### Consumo, inversión y balanza comercial
# Vamos primero a crear las grandes catergorías de nuestras dos economías privadas. Primero con México

# In[14]:


cols = ['C', 'I', 'CD', 'Y']
mex_qnar = pd.DataFrame(index=mex_qnaq.index, columns=cols)

# Vamos a considerar que la balanza comercial es inversión para una economía
# cerrada
mex_qnar['C'] = (mex_qnaq_sa['PC']-mex_qnaq_sa['DC'])/mex_qnap_sa['NDC']*100.
mex_qnar['I'] = (mex_qnaq_sa['I']+mex_qnaq_sa['DC']-mex_qnaq_sa['GI']               + mex_qnaq_sa['X']-mex_qnaq_sa['M'])/mex_qnap_sa['NDC']*100.
mex_qnar['CD'] = mex_qnaq_sa['DC'] / mex_qnap_sa['NDC']*100.  
mex_qnar['Y'] = mex_qnar['C'] + mex_qnar['I']
mex_qnar['PDC'] = mex_qnap_sa['DC']
mex_qnar['PNDC'] = mex_qnap_sa['NDC']

# Vamos también a considerar únicamente el empleo privado
mex_trab['EMPP'] = (mex_trab['EMP15'] - mex_trab['EMPG'])*1000.

mex_qnar = pd.merge(
    mex_qnar,
    mex_trab[['POP15', 'EMPP']],
    left_index=True,
    right_index=True,
    how='outer'
)

cols = ['C', 'I', 'CD', 'CDI', 'CDN', 'EQI', 'EQN', 'X', 'M', 'Y']
mex_qnar_plus = pd.DataFrame(index=mex_qnaq_sa.index, columns=cols)

# Vamos a considerar que la balanza comercial es INVERSIÓN para una economía
# cerrada
mex_qnar_plus['C'] = (mex_qnaq_sa['PC']-mex_qnaq_sa['DC'])/mex_qnap_sa['NDC']*100.
mex_qnar_plus['I'] = (mex_qnaq_sa['I']+mex_qnaq_sa['DC']-mex_qnaq_sa['GI']               + mex_qnaq_sa['X']-mex_qnaq_sa['M'])/mex_qnap_sa['NDC']*100.
mex_qnar_plus['CD'] = mex_qnaq_sa['DC']/mex_qnap_sa['NDC']*100.
mex_qnar_plus['CDI'] = mex_qnaq_sa['DCI']/mex_qnap_sa['NDC']*100.
mex_qnar_plus['CDN'] = mex_qnaq_sa['DCN']/mex_qnap_sa['NDC']*100.
mex_qnar_plus['EQI'] = mex_qnaq_sa['EQI']/mex_qnap_sa['NDC']*100.
mex_qnar_plus['EQN'] = mex_qnaq_sa['EQN']/mex_qnap_sa['NDC']*100.
mex_qnar_plus['X'] = mex_qnaq_sa['X']/mex_qnap_sa['NDC']*100.
mex_qnar_plus['M'] = mex_qnaq_sa['M']/mex_qnap_sa['NDC']*100.
mex_qnar_plus['Y'] = mex_qnar_plus['C'] + mex_qnar_plus['I']
mex_qnar_plus['PDC'] = mex_qnap_sa['DC']
mex_qnar_plus['PNDC'] = mex_qnap_sa['NDC']

# Vamos también a considerar únicamente el empleo privado
mex_trab['EMPP'] = (mex_trab['EMP15'] - mex_trab['EMPG'])*1000.

mex_qnar_plus = pd.merge(
    mex_qnar_plus,
    mex_trab[['POP15', 'EMPP']],
    left_index=True,
    right_index=True,
    how='outer'
)

# Vamos a considerar que la balanza comercial es CONSUMO para una economía
# cerrada
cols = ['C', 'I', 'CD', 'CDI', 'CDN', 'EQI', 'EQN', 'X', 'M', 'Y']
mex_qnar_plusb = pd.DataFrame(index=mex_qnaq.index, columns=cols)

mex_qnar_plusb['C'] = (mex_qnaq_sa['PC']-mex_qnaq_sa['DC']+ mex_qnaq_sa['X']                    - mex_qnaq_sa['M'])/mex_qnap_sa['NDC']*100.
mex_qnar_plusb['I'] = (mex_qnaq_sa['I']+mex_qnaq_sa['DC']-mex_qnaq_sa['GI'])                     / mex_qnap_sa['NDC']*100.
mex_qnar_plusb['CD'] = mex_qnaq_sa['DC'] / mex_qnap_sa['NDC']*100.
mex_qnar_plusb['CDI'] = mex_qnaq_sa['DCI']/mex_qnap_sa['NDC']*100.
mex_qnar_plusb['CDN'] = mex_qnaq_sa['DCN']/mex_qnap_sa['NDC']*100.
mex_qnar_plusb['EQI'] = mex_qnaq_sa['EQI']/mex_qnap_sa['NDC']*100.
mex_qnar_plusb['EQN'] = mex_qnaq_sa['EQN']/mex_qnap_sa['NDC']*100.
mex_qnar_plusb['X'] = mex_qnaq_sa['X']/mex_qnap_sa['NDC']*100.
mex_qnar_plusb['M'] = mex_qnaq_sa['M']/mex_qnap_sa['NDC']*100.
mex_qnar_plusb['Y'] = mex_qnar_plusb['C'] + mex_qnar_plusb['I']
mex_qnar_plusb['PDC'] = mex_qnap_sa['DC']
mex_qnar_plusb['PNDC'] = mex_qnap_sa['NDC']

# Vamos también a considerar únicamente el empleo privado
mex_trab['EMPP'] = (mex_trab['EMP15'] - mex_trab['EMPG'])*1000.

mex_qnar_plusb = pd.merge(
    mex_qnar_plusb,
    mex_trab[['POP15', 'EMPP']],
    left_index=True,
    right_index=True,
    how='outer'
)


# Después con Estados Unidos

# In[15]:


cols = ['C', 'I', 'CD', 'Y']
usa_qnar = pd.DataFrame(index=usa_qnaq.index, columns=cols)

# Vamos a considerar que la balanza comercial es inversión para una economía
# cerrada
usa_qnar['C'] = (usa_qnaq_sa['PC']-usa_qnaq_sa['CD'])/usa_qnap_sa['PNDC']*100.
usa_qnar['I'] = (usa_qnaq_sa['I']+usa_qnaq_sa['CD']-usa_qnaq_sa['IG']               + usa_qnaq_sa['X']-usa_qnaq_sa['M']) / usa_qnap_sa['PNDC']*100.
usa_qnar['CD'] = usa_qnaq_sa['CD'] / usa_qnap_sa['PNDC']*100.
usa_qnar['Y'] = usa_qnar['C'] + usa_qnar['I']
usa_qnar['PDC'] = usa_qnap_sa['PDC']
usa_qnar['PNDC'] = usa_qnap_sa['PNDC']

# Vamos también a considerar únicamente el empleo privado
usa_trab['EMPP'] = usa_trab['EMP15']*1000.

usa_qnar = pd.merge(
    usa_qnar,
    usa_trab[['POP15', 'EMPP']],
    left_index=True,
    right_index=True,
    how='outer'
)

cols = ['C', 'I', 'CD', 'CDI', 'EQI', 'X', 'M', 'Y']
usa_qnar_plus = pd.DataFrame(index=usa_qnaq.index, columns=cols)

# Vamos a considerar que la balanza comercial es INVERSIÓN para una economía
# cerrada
usa_qnar_plus['C'] = (usa_qnaq_sa['PC']-usa_qnaq_sa['CD'])/usa_qnap_sa['PNDC']*100.
usa_qnar_plus['I'] = (usa_qnaq_sa['I']+usa_qnaq_sa['CD']-usa_qnaq_sa['IG']               + usa_qnaq_sa['X']-usa_qnaq_sa['M']) / usa_qnap_sa['PNDC']*100.
usa_qnar_plus['CD'] = usa_qnaq_sa['CD']/usa_qnap_sa['PNDC']*100.
usa_qnar_plus['CDI'] = usa_qnaq_sa['DCI']/usa_qnap_sa['PNDC']*100.
usa_qnar_plus['EQI'] = usa_qnaq_sa['EQI']/usa_qnap_sa['PNDC']*100.
usa_qnar_plus['X'] = usa_qnaq_sa['X']/usa_qnap_sa['PNDC']*100.
usa_qnar_plus['M'] = usa_qnaq_sa['M']/usa_qnap_sa['PNDC']*100.
usa_qnar_plus['Y'] = usa_qnar_plus['C'] + usa_qnar_plus['I']
usa_qnar_plus['PDC'] = usa_qnap_sa['PDC']
usa_qnar_plus['PNDC'] = usa_qnap_sa['PNDC']

# Vamos también a considerar únicamente el empleo privado
usa_trab['EMPP'] = usa_trab['EMP15']*1000.

usa_qnar_plus = pd.merge(
    usa_qnar_plus,
    usa_trab[['POP15', 'EMPP']],
    left_index=True,
    right_index=True,
    how='outer'
)

cols = ['C', 'I', 'CD', 'CDI', 'EQI', 'X', 'M', 'Y']
usa_qnar_plusb = pd.DataFrame(index=usa_qnaq.index, columns=cols)

# Vamos a considerar que la balanza comercial es CONSUMO para una economía
# cerrada
usa_qnar_plusb['C'] = (usa_qnaq_sa['PC']-usa_qnaq_sa['CD']+ usa_qnaq_sa['X']                     - usa_qnaq_sa['M'])/usa_qnap_sa['PNDC']*100.
usa_qnar_plusb['I'] = (usa_qnaq_sa['I']+usa_qnaq_sa['CD']-usa_qnaq_sa['IG'])                     / usa_qnap_sa['PNDC']*100.
usa_qnar_plusb['CD'] = usa_qnaq_sa['CD']/usa_qnap_sa['PNDC']*100.
usa_qnar_plusb['CDI'] = usa_qnaq_sa['DCI']/usa_qnap_sa['PNDC']*100.
usa_qnar_plusb['EQI'] = usa_qnaq_sa['EQI']/usa_qnap_sa['PNDC']*100.
usa_qnar_plusb['X'] = usa_qnaq_sa['X']/usa_qnap_sa['PNDC']*100.
usa_qnar_plusb['M'] = usa_qnaq_sa['M']/usa_qnap_sa['PNDC']*100.
usa_qnar_plusb['Y'] = usa_qnar_plusb['C'] + usa_qnar_plusb['I']
usa_qnar_plusb['PDC'] = usa_qnap_sa['PDC']
usa_qnar_plusb['PNDC'] = usa_qnap_sa['PNDC']

# Vamos también a considerar únicamente el empleo privado
usa_trab['EMPP'] = usa_trab['EMP15']*1000.

usa_qnar_plusb = pd.merge(
    usa_qnar_plusb,
    usa_trab[['POP15', 'EMPP']],
    left_index=True,
    right_index=True,
    how='outer'
)


# Y ya tenemos lo que necesitamos para hacer varios análisis que nos permiten comparar el comportamiento cíclico de la economía de México relativo a Estados Unidos, aunque no sea exáctamente lo que se les pide en la tarea.
# 
# Salvamos los datos.

# In[16]:


mex_qnar.to_excel('mexico.xlsx') 
mex_qnar_plus.to_excel('mexico_plus.xlsx')
mex_qnar_plusb.to_excel('mexico_plusb.xlsx')
usa_qnar.to_excel('usa.xlsx')
usa_qnar_plus.to_excel('usa_plus.xlsx')
usa_qnar_plusb.to_excel('usa_plusb.xlsx')


# In[ ]:





# In[ ]:




