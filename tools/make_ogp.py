# -*- coding: utf-8 -*-
"""
SNS用のOGP画像（ogp.png）を生成する。

    python tools/make_ogp.py

右側のグラフは飾りではなく、本体と同じ計算式で出した実際の資産推移
（40歳・夫婦・子1人・持ち家・63歳まで就労のケース）。数値は tools/ogp_band.json に
書き出してある。作り直す場合は本体の simulate() から再出力する。

Pillow と Windows 標準の BIZ UD フォントを使う。出力は 1200x630。
"""
from PIL import Image, ImageDraw, ImageFont
import json, os

W, H = 1200, 630
BG    = (26, 32, 54)
WHITE = (255, 255, 255)
SUB   = (222, 228, 238)
MUTE  = (150, 159, 180)
CASH  = (140, 96, 40)     # 現金
PRIN  = (52, 68, 140)     # 投資元本
GAIN  = (22, 110, 78)     # 運用益
EDGE  = (150, 155, 175)   # 層の境目

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
F = "C:/Windows/Fonts/"

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# ---- 右側：実データの三層エリアチャート（右端と下端は断ち切り）----
band = json.load(open(os.path.join(HERE, "ogp_band.json"), encoding="utf-8"))
n = len(band)
X0, X1 = 520, W + 30          # 右へはみ出させる
Y0, Y1 = 270, H + 20          # 下へはみ出させる
top = max(b[0] + b[1] + b[2] for b in band)

def px(i):  return X0 + (X1 - X0) * i / (n - 1)
def py(v):  return Y1 - (Y1 - Y0) * v / top

base = [0.0] * n
for layer, color in ((0, CASH), (1, PRIN), (2, GAIN)):
    upper = [base[i] + band[i][layer] for i in range(n)]
    poly  = [(px(i), py(upper[i])) for i in range(n)] + \
            [(px(i), py(base[i]))  for i in range(n - 1, -1, -1)]
    d.polygon(poly, fill=color)
    d.line([(px(i), py(upper[i])) for i in range(n)], fill=EDGE, width=3, joint="curve")
    base = upper

# ---- 左側：文字 ----
mincho = ImageFont.truetype(F + "BIZ-UDMinchoM.ttc", 118)
goth_b = ImageFont.truetype(F + "BIZ-UDGothicB.ttc", 37)
goth_r = ImageFont.truetype(F + "BIZ-UDGothicR.ttc", 27)

d.text((52, 62),  "家計の50年", font=mincho, fill=WHITE)
d.text((56, 292), "年齢と手取り年収を入れるだけの", font=goth_b, fill=SUB)
d.text((56, 348), "家計シミュレーション", font=goth_b, fill=SUB)
d.text((56, 466), "教育費・年金・介護費は",           font=goth_r, fill=MUTE)
d.text((56, 508), "公的統計にもとづく標準値入り",     font=goth_r, fill=MUTE)
d.text((56, 550), "登録不要・入力はブラウザ内だけ",   font=goth_r, fill=MUTE)

out = os.path.join(ROOT, "ogp.png")
img.save(out, "PNG", optimize=True)
print("saved:", out, img.size)
