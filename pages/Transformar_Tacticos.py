import streamlit as st
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_icon = "💯"
)

st.markdown("<h1 style='text-align: center;color:#ccd6f6'>TÁCTICOS</h1>", unsafe_allow_html=True)

st.markdown("<h4 style='color: #a5a5a6;text-align: center;'>Subir Tacticos</h4>", unsafe_allow_html=True)
with st.expander("Recuerda que el archivo Excel debe contar con los siguientes campos..."):
    st.write("FECHA DE INICIO | FECHA FIN | SKU | DESCRIPCIÓN | TOP DESPLIEGUE MEDIOS 'X'")
archivo = st.file_uploader("Sube tu archivo Excel", type=["xlsx","xls"])

if archivo:
    if st.button("Transformar data"):
        df_y_total = []
        df_tactico = pd.read_excel(archivo)
        df_tactico = df_tactico.dropna(subset='SKU')
        df_y_total = []
        SKUS = df_tactico['SKU'].unique()
        
        for x in SKUS:
            df = df_tactico[df_tactico['SKU'] == x]
            SKU = x
            SKU_DESC = df['DESCRIPCIÓN'].iloc[0]
            CAMPAÑA = df['CAMPAÑA'].iloc[0]
            
            dfs = []
            
            for index, row in df.iterrows():
                df_x = pd.DataFrame({'Fecha': pd.date_range(row['FECHA INICIO'], row['FECHA FIN'])})
                TOP_DEALS_COD = row['TOP DESPLIEGUE MEDIOS "X"']
                
                df_x[f'TOP_DEALS_{index}'] = TOP_DEALS_COD
                
                dfs.append(df_x.set_index('Fecha'))
                
            df_y = pd.concat(dfs , axis = 1)
            df_y.reset_index(inplace=True)
            df_y['T'] = df_y.filter(like="TOP").mode(axis=1).get(0, default='')
            
            df_y.drop(columns=df_y.filter(like="TOP").columns, inplace=True)
            df_y['CAMPAÑA'] = CAMPAÑA
            df_y['SKU'] = SKU
            df_y['SKU_DESC'] = SKU_DESC
            df_y['Año'] = df_y["Fecha"].dt.year
            df_y['Mes'] = df_y["Fecha"].dt.month
            df_y_total.append(df_y)
            
        df_final = pd.concat(df_y_total, ignore_index=True)
        df_final['SKU'] = df_final['SKU'].astype('str')
        
        st.dataframe(df_final)