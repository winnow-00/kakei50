# -*- coding: utf-8 -*-
"""
SNS用のOGP画像（ogp.png）を生成する。

    python tools/make_ogp.py

Pillow と Windows 標準の BIZ UD フォントを使う。
ブラウザを経由しないので、文言を変えたいときはここを直して実行するだけ。
出力は 1200x630。SNSのカードはこの比率が標準。
"""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1200, 630
BG    = (26, 32, 54)      # 濃紺（faviconと同じ）
WHITE = (255, 255, 255)
SUB   = (201, 208, 222)
MUTE  = (139, 147, 168)
DIM   = (110, 119, 140)
CASH  = (178, 122, 24)    # 現金
PRIN  = (74, 92, 171)     # 投資元本
GAIN  = (24, 136, 90)     # 運用益

F = "C:/Windows/Fonts/"
img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

mincho = ImageFont.truetype(F + "BIZ-UDMinchoM.ttc", 96)
goth_b = ImageFont.truetype(F + "BIZ-UDGothicB.ttc", 34)
goth_r = ImageFont.truetype(F + "BIZ-UDGothicR.ttc", 27)
mono   = ImageFont.truetype(F + "consola.ttf", 25)

# 下端の3色帯（本体グラフの3層と同じ色）
for i, c in enumerate([CASH, PRIN, GAIN]):
    d.rectangle([i * W // 3, H - 10, (i + 1) * W // 3, H], fill=c)

# 右側：資産が積み上がる棒。上端は 380px までに抑える（切れないように）
x = 806
for h, c in [(130, CASH), (215, PRIN), (300, GAIN), (380, PRIN)]:
    d.rounded_rectangle([x, H - 150 - h, x + 66, H - 150], radius=8, fill=c)
    x += 90

d.text((80, 96),  "家計の50年", font=mincho, fill=WHITE)
d.text((84, 250), "年齢と手取り年収を入れるだけの", font=goth_b, fill=SUB)
d.text((84, 300), "家計シミュレーション", font=goth_b, fill=SUB)
d.text((84, 376), "教育費・年金・介護費は公的統計にもとづく標準値入り", font=goth_r, fill=MUTE)
d.text((84, 418), "登録不要・入力はブラウザ内だけ", font=goth_r, fill=MUTE)
d.text((84, 508), "winnow-00.github.io/kakei50", font=mono, fill=DIM)

out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ogp.png")
img.save(out, "PNG", optimize=True)
print("saved:", out, img.size)
