import streamlit as st
import pandas as pd
import numpy as np
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import pandas as pd
from google.oauth2.service_account import Credentials
from matplotlib import pyplot as plt
import seaborn
from sklearn.linear_model import LinearRegression as LR
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline


#スプレッドシートの読み込み--------------------------------------------------
#def read_spread():

scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

credentials = Credentials.from_service_account_file(
    'gspread-tech0-suumo-f3edd9717bb1.json',
    scopes=scopes
)

gc = gspread.authorize(credentials)

SP_SHEET_KEY = '1co7OezxBYraCGdCENmFvH41EG_HvspnUAOOQAGqkcc8'
sh = gc.open_by_key(SP_SHEET_KEY)

SP_SHEET = 'DB'
worksheet = sh.worksheet(SP_SHEET)
        
#スプレッドシートの選択
sh = gc.open_by_key(SP_SHEET_KEY)
#シートの選択
worksheet = sh.worksheet(SP_SHEET)
        
data = worksheet.get_all_values()
        
df = pd.DataFrame(data[1:], columns=data[0])


#平米数から算出する家賃(その平米数の予測家賃)-------------------------------
#def est():

x = df[['面積']]
y = df[['家賃']]

x['面積'] = x['面積'].astype(np.float64)
y['家賃'] = y['家賃'].astype(np.float64)

model = make_pipeline(StandardScaler(with_mean=False), LR())

model_lr = LR(normalize=True)
model_lr.fit(x, y)

w1 = '%.3f' %model_lr.coef_ #モデル関数の回帰変数
w2 = '%.3f' %model_lr.intercept_ #モデル関数の切片
estimate = 'y= %.3fx + %.3f' % (model_lr.coef_ , model_lr.intercept_)
# estimate = y = 0.341x + 0.405　(万円)


#初期画面-----------------------------------------------------------------
st.title('家賃予測')

#サイドバー---------------------------------------------------------------
area_select = st.sidebar.selectbox(
    'エリア(23区)',
    list(('選択してください', '世田谷区'))
    #list(('選択してください', '足立区', '荒川区', '板橋区', '江戸川区', '大田区', '葛飾区', '北区', '江東区', '品川区', '渋谷区', '新宿区', '杉並区', '墨田区', '世田谷区', '台東区', '千代田区', '中央区', '豊島区', '中野区', '練馬区', '文京区', '港区', '目黒区'))
)

square = st.sidebar.text_input('平米数(m^2)')

price = st.sidebar.text_input('家賃(万円)')

button = st.sidebar.button('相場検索')

#入力値のインプット--------------------------------------------------------
#square = input('平米数(m^2)')
#price = input('家賃(万円)')

if price and square:
    s = float(square)
    p = float(price)
    #浮動小数点数同士の計算　後で確認＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
    a = 0.341 * s + 0.405
    if button:
        #推定家賃の表示----------------------------------------------------
        st.write('お探しの条件での推定家賃', round(a, 4), '万円')
        #入力平米数での平均家賃と、入力家賃の比較　割高or割安表示-----------------
        if p < a:
            st.write('この物件は相場よりも、割安です。')
            st.write(df[:11])
        elif p == a:
            st.write('この物件は相場と同等価格です。')
            st.write(df[:11])
        else:
            st.write('この物件は相場よりも、割高です。')
            st.write(df[:11])


#表の表示----------------------------------------------------------------
##入力平米数における、家賃を低い方から10個
##上から10行を表示
##st.write(表)

#改善点：予測家賃計算、表表示、（他区）