import streamlit as st
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_icon = "📊"
)

st.markdown("<h1 style='text-align: center;color:#ccd6f6'>HS</h1>", unsafe_allow_html=True)

st.markdown("<h4 style='color: #a5a5a6;text-align: center;'>Subir HS</h4>", unsafe_allow_html=True)
with st.expander("Recuerda que el archivo Excel debe contar con los siguientes campos..."):
    st.write("FECHA DE INICIO | FECHA DE FIN | PROMOCION | SKU | Descripcion | EAN | Division | ARRIENDO | Tipo Promocion | TOP DEALS")
archivo = st.file_uploader("Sube tu archivo Excel", type=["xlsx","xls"])

if archivo:
    if st.button("Transformar data"):  
        df_total = pd.read_excel(archivo, engine="openpyxl")
        df_y_total = []
        SKUS = df_total['SKU'].unique()
        for x in SKUS:
            df = df_total[df_total['SKU']==x]
            df = df.dropna(subset=['Division'])
            SKU = x
            SKU_DESC = df['Descripcion'].iloc[0]
            EAN = df['EAN'].iloc[0]
            DIVISION = df['Division'].iloc[0]
            PROMOCION = df['PROMOCION'].iloc[0]
            
            dfs = []
            
            for index, row in df.iterrows():
                df_x = pd.DataFrame({'Fecha': pd.date_range(row['FECHA DE INICIO'], row['FECHA DE FIN'])})
                CMR_COD = 1 if row['Tipo Promocion'] == 'CON CMR' else 0
                ARRIENDO_COD = 1 if row['ARRIENDO'] == 'SI' else 0
                TOP_DEALS_COD = row['TOP DEALS']
                
                df_x[f'ARRIENDO_{index}'] = ARRIENDO_COD
                df_x[f'CMR_{index}'] = CMR_COD
                df_x[f'TOP_DEALS_{index}'] = TOP_DEALS_COD
                
                dfs.append(df_x.set_index('Fecha'))
            
            df_y = pd.concat(dfs, axis=1)
            df_y.reset_index(inplace=True)
            df_y['C'] = df_y.filter(like="CMR").max(axis=1).astype(int)
            df_y['A'] = df_y.filter(like="ARRIENDO").max(axis=1).astype(int)
            df_y['T'] = df_y.filter(like="TOP").mode(axis=1).get(0, default='')
            
            df_y.drop(columns=df_y.filter(like="CMR").columns, inplace=True)
            df_y.drop(columns=df_y.filter(like="ARRIENDO").columns, inplace=True)
            df_y.drop(columns=df_y.filter(like="TOP").columns, inplace=True)
            
            df_y['Promocion'] = PROMOCION
            df_y['División'] = DIVISION
            df_y['SKU'] = SKU
            df_y['EAN'] = EAN
            df_y['SKU_DESC'] = SKU_DESC
            df_y['Año'] = df_y["Fecha"].dt.year
            df_y['Mes'] = df_y["Fecha"].dt.month
            df_y_total.append(df_y)
            
        df_final = pd.concat(df_y_total, ignore_index=True)
        df_final['SKU'] = df_final['SKU'].astype('str')
        
        st.dataframe(df_final)