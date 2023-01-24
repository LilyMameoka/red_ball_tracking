import numpy as np
from matplotlib import pyplot as plt

# CSVのロード
data = np.genfromtxt("./data.csv", delimiter=",", dtype='float')

# 2次元配列を分割（経過時間t, x座標, y座標の1次元配列)
t = data[:,0]
x = data[:,1]
y = data[:,2]
x=x-200



# 近似パラメータakを算出
coe = np.polyfit(x, y, 2)
print(coe)

# 得られたパラメータakからカーブフィット後の波形を作成
y_fit = coe[0] * x ** 2 + coe[1] * x ** 1 + coe[2]

# 相関係数と決定係数を計算する
r = np.corrcoef(y, y_fit)[0,1] # 相関係数R
r2 = r ** 2 # 決定係数R^2
print(r, r2)

coe[0]=round(coe[0],5)
coe[1]=round(coe[1],5)
coe[2]=round(coe[2],5)

# ここからグラフ描画
# フォントの種類とサイズを設定する。
plt.rcParams['font.size'] = 14
plt.rcParams['font.family'] = 'Times New Roman'

# 目盛を内側にする。
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'

# グラフの上下左右に目盛線を付ける。
fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.yaxis.set_ticks_position('both')
ax1.xaxis.set_ticks_position('both')

# 軸のラベルを設定する。
ax1.set_xlabel('x')
ax1.set_ylabel('y')

# データプロットの準備。
ax1.scatter(x, y, label='sample', lw=1, marker="o")
ax1.plot(x, y_fit, label='fitted curve', lw=1)

# グラフを表示する。
fig.tight_layout()


plt.text(0,0,rf'$y={coe[0]}x^2+{coe[1]}x+{coe[2]}$',fontsize=15)
plt.show()
plt.close()