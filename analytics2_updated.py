import pandas as pd
import numpy as np
from matplotlib import pyplot as plt 
from sklearn.linear_model import LinearRegression as LR
from sklearn import preprocessing
import seaborn as sns
from sklearn.linear_model import LinearRegression

#データの前処理----------------------------------------------------
data = pd.read_excel("SUUMO(データ分割版）.xlsx")

data_complete = data

#データの前処理----------------------------------------------------

#重回帰分析-------------------------------------------------------

df = data_complete

df.to_excel("all-data.xlsx")

train = pd.read_excel("train-suumo.xlsx")
test = pd.read_excel("test-suumo.xlsx")

mm = preprocessing.MinMaxScaler()

train_test = train[["築年数", "面積", "徒歩"]]

train_nm = mm.fit_transform(train_test)

df_train = pd.DataFrame(train_nm)

df = df_train
df_train = df.rename(columns={0: "築年数", 1: "面積", 2: "徒歩"})

test = test[["築年数", "面積", "徒歩"]]

test_nm = mm.fit_transform(test)

df_test = pd.DataFrame(test_nm)

df2 = df_train
df_test = df2.rename(columns={0: "築年数", 1: "面積", 2: "徒歩"})

model = LR()

target_data = pd.DataFrame(train["家賃"])
model.fit(target_data, df_train)

model.coef_

model.intercept_

model.score(target_data, df_train)

#重回帰分析-------------------------------------------------------

#ユーザーのインプットを受け取り、散布図で表示---------------------------

#後で確認
plt.scatter(data_complete["家賃"], data_complete["面積"])


user_input_m2 = input("平米数を書いてね（数字だけでいいよ）：")
user_input_m2 = int(user_input_m2)

user_input_yachin = int(input("家賃を書いてね(数字だけでいいよ)："))
user_input_yachin = int(user_input_yachin)

new_input_data = pd.DataFrame(
    data={'家賃': user_input_yachin, 
        '面積': user_input_m2},
    index=[0]
)

origin_data = data_complete[["家賃", "面積"]]
merged_data= origin_data.append(new_input_data)

#散布図の作成

plt.title('家賃と平米数の相関図',
                    fontsize=20) # タイトル
plt.xlabel("平米数（m2）", fontsize=20) # x軸ラベル
plt.ylabel("家賃（万円）", fontsize=20) # y軸ラベル
plt.grid(True) # 目盛線の表示
plt.tick_params(labelsize = 12) # 目盛線のラベルサイズ

plt.scatter(merged_data["家賃"], merged_data["面積"], c="b", label="世の中の平均")

#散布図の関数化
plot_data = plt.scatter(merged_data["家賃"], merged_data["面積"], c="b", label="世の中の平均")

plt.scatter(merged_data["家賃"], merged_data["面積"], c="b", label="世の中の平均")
plt.scatter(user_input_yachin, user_input_m2, c="r", label="あなたのデータ") 


#ユーザーのインプットを受け取り、散布図で表示---------------------------
#単回帰分析 -------------------------------------------------------
dfdf = pd.DataFrame(train["家賃"])
dfdf2 = pd.DataFrame(train["面積"])

x = dfdf2
y = dfdf

plt.plot(x, y, 'o')
plt.show()

model_lr = LinearRegression()

model_lr.fit(x, y)

plt.plot(x, y, 'o')
plt.plot(x, model_lr.predict(x), linestyle="solid")
plt.show()

print('モデル関数の回帰変数 w1: %.3f' %model_lr.coef_)
print('モデル関数の切片 w2: %.3f' %model_lr.intercept_)
print('y= %.3fx + %.3f' % (model_lr.coef_ , model_lr.intercept_))
print('決定係数 R^2： ', model_lr.score(x, y))

##予測

dfdf3 = pd.DataFrame(test["面積"])
pred = model_lr.predict(dfdf3)
pred2 = pd.DataFrame(pred)
pred2

##インプットから推論

user_input_m2 = int(input("平米数を書いてね"))
user_input_m22 = pd.DataFrame(
                 {'列名1':[user_input_m2]},
                 index = ['１']
                  )

input_pred = model_lr.predict(user_input_m22)
input_pred2 = pd.DataFrame(input_pred)
input_pred2

#単回帰分析-------------------------------------------------------




