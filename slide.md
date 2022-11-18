---
marp: true
---

# オブジェクトトラッキングと軌跡の出力

---

# 使用した言語, ライブラリ

- Python (3 系)

### オブジェクトトラッキング

- OpenCV
- numpy

### 軌跡の出力

- matplotlib
- numpy

---

# 要件

- 赤いゴルフボールの軌跡をグラフで出力すること

# 仕様

- OpenCV を用いて、最大の赤色領域の座標を取得して追跡（オブジェクトトラッキング）
- 座標の変化をグラフに出力

---

# 1. オブジェクトトラッキング

1. マスク処理で赤色の領域を抽出
2. ラベリング処理と Blob 解析で最大領域の座標を取得
3. 上記をカメラ入力のフレーム毎に適用することで、最大の赤色領域の座標の座標を追跡
4. CSV として出力する

---

## 1-1. マスク処理

1. 入力を HSV 色空間に変換する
2. 検出する色の範囲を指定
   a. 赤色の色相は正の値を用いると 0~30, 150~179 の 2 領域になる

##### マスク処理とは

特定の領域のみを表示し、それ以外を表示しない(黒色にする)ようにする処理。ここでは、`cv2.inRange`を用いて、HSV 色空間の中で特定の HSV 色範囲に含まれる部分のみを抽出している。

---

```python: object_tracking.py

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

hsv_min = np.array([0,127,0])
hsv_max = np.array([30,255,255])
mask1 = cv2.inRange(hsv, hsv_min, hsv_max)

hsv_min = np.array([150,127,0])
hsv_max = np.array([179,255,255])
mask2 = cv2.inRange(hsv, hsv_min, hsv_max)

```

<!--
参考:
- `https://algorithm.joho.info/image-processing/hsv-color-space/`
- `https://pystyle.info/opencv-mask-image/`
-->

---

## 1-2. ラベリング処理・Blob 解析

1. 2 値化画像を`cv2.connectedComponentsWithStats`でラベリング処理し、領域毎にデータを取得できるようにする
2. 領域の面積と中心座標を取得するために必要なデータを抽出(Blob を加工)
3. 面積最大の領域のラベルを特定
4. 面積最大の領域のステータスを取得

##### ラベリング処理とは

画像中に含まれるオブジェクト(領域)にラベルを振る処理。例えば、2 値化画像の False の領域(背景)は 0, True の領域は 1,2,3,...n のように、領域に番号をつけて、その後に処理できるようにする。

---

```python: object_tracking.py

label = cv2.connectedComponentsWithStats(binary_img)

n = label[0] - 1
data = np.delete(label[2], 0, 0)
center = np.delete(label[3], 0, 0)

max_index = np.argmax(data[:, 4])

maxblob = {}
maxblob["upper_left"] = (data[:, 0][max_index], data[:, 1][max_index]) # 左上座標
maxblob["width"] = data[:, 2][max_index]  # 幅
maxblob["height"] = data[:, 3][max_index]  # 高さ
maxblob["area"] = data[:, 4][max_index]   # 面積
maxblob["center"] = center[max_index]  # 中心座標

```

<!--
参考:
- `https://algorithm.joho.info/programming/python/blob-max-moment/`
- `https://axa.biopapyrus.jp/ia/opencv/object-detection.html`
-->

---

## 1-3. 動画のフレーム毎に座標を CSV で出力

1. 経過時間, 最大の赤色領域の座標(x, y)を 配列に格納
2. 一連の処理が終了したら CSV に出力

---

# 2. 軌跡の出力

- matplotlib を用いて、xy 座標系に軌跡を出力する
