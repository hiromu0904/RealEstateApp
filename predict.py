import streamlit as st
import pandas as pd
import numpy as np

st.title('家賃予測')

area_select = st.sidebar.selectbox(
    'エリア(23区)',
    list(('選択してください', '足立区', '荒川区', '板橋区', '江戸川区', '大田区', '葛飾区', '北区', '江東区', '品川区', '渋谷区', '新宿区', '杉並区', '墨田区', '世田谷区', '台東区', '千代田区', '中央区', '豊島区', '中野区', '練馬区', '文京区', '港区', '目黒区'))
)


square = st.sidebar.text_input('平米数(m^2)', )

price = st.sidebar.text_input('家賃(万円)')

if st.sidebar.button('相場検索'):
    letter = st.write("""
    ### この物件は相場よりも、割高です。

    ### お探しの条件での推定家賃：14.8万円

    """)
else:
    st.write("""
    ## サイドバーから値を入力してください。
    """)

    #アプリデザイン