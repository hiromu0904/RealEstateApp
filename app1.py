import pandas as pd
import matplotlib.pyplot as plt 
import streamlit as st
import matplotlib.font_manager
import math

# スクレイピングデータの取得
@st.cache
def get_data():
    df = pd.read_excel("SUUMO(データ分割版）.xlsx", index_col=0)
    arr = df[["家賃", "面積"]]
    return arr
arr = get_data()

# 家賃、面積の最大値/最小値の取得
xmin_value=arr['家賃'].min()
xmax_value=math.ceil(arr['家賃'].max())+5
ymin_value=arr['面積'].min()
ymax_value=math.ceil(arr['面積'].max())+10

# サイドバーの設定
st.sidebar.write("""
## グラフの範囲設定
""")
xmin, xmax=st.sidebar.slider("家賃(万円):", 0, xmax_value,(0, xmax_value), 1)
ymin, ymax=st.sidebar.slider("平米数(㎡):", 0, ymax_value,(0, ymax_value), 1)
st.sidebar.write("""
## あなたの物件情報
""")
xuser=st.sidebar.number_input('あなたの家賃(万円):',value=10.0, step=0.1)
yuser=st.sidebar.number_input('あなたの平米数(㎡):', value=40, step=1)

# プロット図の表示
fig, ax = plt.subplots()
ax.scatter(xuser, yuser, s=70, linewidths=2, c='b', edgecolors='b', label='あなたの物件')
ax.scatter(arr["家賃"],arr["面積"],s=15, alpha=0.5, linewidths=2, c='#FFaaaa', edgecolors='r',label='地域の物件')
ax.set_xlabel('家賃',fontfamily='Meiryo')
ax.set_ylabel('平米数',fontfamily='Meiryo')
ax.set_xlim(left=xmin, right=xmax)
ax.set_ylim(bottom=ymin, top=ymax)
ax.set_title('家賃プロット図',fontfamily='Meiryo', fontdict={'fontsize':15}, y=1.1)
ax.legend(prop={"family":"Meiryo"})
st.pyplot(fig)