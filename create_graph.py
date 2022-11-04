# -*- coding: utf-8
import numpy as np
import matplotlib.pyplot as plt

def main():
    # CSVのロード
    data = np.genfromtxt(
        "./data.csv", delimiter=",", dtype='float')

    # 2次元配列を分割（経過時間t, x座標, y座標の1次元配列)
    t = data[:,0]
    x = data[:,1]
    y = data[:,2]

    # グラフにプロット
    plt.rcParams["font.family"] = "Times New Roman" # フォントの種類
    plt.plot(x, y, "r-", label="coordinate")
    plt.xlabel("x軸", fontsize=16)     # x軸ラベル
    plt.ylabel("y軸", fontsize=16)    # y軸ラベル
    plt.grid()         # グリッド表示
    plt.legend(loc=1, fontsize=16)       # 凡例表示
    plt.show()


if __name__ == "__main__":
    main()