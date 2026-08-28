# -*- coding: utf-8 -*-
"""
Instagram用のカルーセル画像を生成する。

    python tools/make_instagram.py

1080x1350（4:5）を5枚。draft/instagram/ に出力する。
文言やレイアウトを変えたいときは、このファイルを直して実行するだけ。
"""
from PIL import Image, ImageDraw, ImageFont
import json, os

W, H = 1080, 1350
BG    = (26, 32, 54)
WHITE = (255, 255, 255)
SUB   = (222, 228, 238)
MUTE  = (150, 159, 180)
DIM   = (110, 119, 140)
LINE  = (60, 68, 92)
CASH  = (178, 122, 24)
PRIN  = (74, 92, 171)
GAIN  = (24, 136, 90)

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT  = os.path.join(ROOT, "draft", "instagram")
os.makedirs(OUT, exist_ok=True)
F = "C:/Windows/Fonts/"

def font(name, size):
    return ImageFont.truetype(F + name, size)

MIN_XL = font("BIZ-UDMinchoM.ttc", 108)
MIN_L  = font("BIZ-UDMinchoM.ttc", 76)
GO_B   = font("BIZ-UDGothicB.ttc", 46)
GO_M   = font("BIZ-UDGothicB.ttc", 38)
GO_R   = font("BIZ-UDGothicR.ttc", 33)
GO_S   = font("BIZ-UDGothicR.ttc", 27)
MONO   = font("consola.ttf", 30)
NUM    = font("BIZ-UDGothicB.ttc", 64)

def base(page):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    for i, c in enumerate([CASH, PRIN, GAIN]):
        d.rectangle([i * W // 3, 0, (i + 1) * W // 3, 9], fill=c)
    d.text((W - 96, H - 74), "{}/5".format(page), font=GO_S, fill=DIM)
    return img, d

def wrap(d, lines, f, x, y, lh, fill):
    """lines は文字列のリスト。最後に描いた行の下端 y を返す。"""
    for line in lines:
        d.text((x, y), line, font=f, fill=fill)
        y += lh
    return y

# ---------- 1枚目：表紙 ----------
img1, d1 = base(1)
band = json.load(open(os.path.join(HERE, "ogp_band.json"), encoding="utf-8"))
n = len(band)
X0, X1, Y0, Y1 = -40, W + 40, 780, H + 40
top = max(sum(b) for b in band)
px = lambda i: X0 + (X1 - X0) * i / (n - 1)
py = lambda v: Y1 - (Y1 - Y0) * v / top
b0 = [0.0] * n
for layer, col in ((0, CASH), (1, PRIN), (2, GAIN)):
    up = [b0[i] + band[i][layer] for i in range(n)]
    d1.polygon([(px(i), py(up[i])) for i in range(n)] +
               [(px(i), py(b0[i])) for i in range(n - 1, -1, -1)], fill=col)
    d1.line([(px(i), py(up[i])) for i in range(n)], fill=(150, 155, 175), width=3)
    b0 = up
d1.text((72, 150), "家計の50年", font=MIN_XL, fill=WHITE)
wrap(d1, ["年齢と手取り年収を", "入れるだけの", "家計シミュレーション"], GO_B, 76, 330, 68, SUB)
d1.text((76, 590), "無料・登録不要", font=GO_R, fill=MUTE)

# ---------- 2枚目：出典 ----------
img2, d2 = base(2)
wrap(d2, ["数字は全部", "公的統計から"], MIN_L, 72, 130, 96, WHITE)
y = 400
for name, src in [
    ("教育費（幼〜高）", "文部科学省 子供の学習費調査"),
    ("教育費（大学）",   "日本政策金融公庫 教育費負担の実態調査"),
    ("生活費",           "総務省 家計調査 2025年平均"),
    ("年金",             "日本年金機構 令和8年度"),
    ("介護費",           "生命保険文化センター 2024年度"),
]:
    d2.rectangle([72, y + 8, 78, y + 44], fill=GAIN)
    d2.text((98, y), name, font=GO_M, fill=SUB)
    d2.text((98, y + 50), src, font=GO_S, fill=MUTE)
    y += 128
d2.rectangle([72, 1190, W - 72, 1193], fill=LINE)
d2.text((72, 1226), "塾代も、下宿の仕送りも、出典のある数字だけ", font=GO_S, fill=DIM)

# ---------- 3枚目：忘れる支出 ----------
img3, d3 = base(3)
wrap(d3, ["生活費を聞かれて", "答え忘れるもの"], MIN_L, 72, 130, 100, WHITE)
y = 420
for t in ["固定資産税", "住宅の修繕費", "火災保険", "車の買替", "80歳からの介護費"]:
    d3.text((84, y), "・" + t, font=GO_B, fill=SUB)
    y += 104
y = wrap(d3, ["毎月きっかり出ていくお金ではないので、",
              "家計簿を思い浮かべながら答えると、",
              "まるごと抜ける。"], GO_R, 76, y + 46, 54, MUTE)
d3.text((76, y + 34), "最初から全部入れてあります。", font=GO_M, fill=SUB)

# ---------- 4枚目：実質で見せる ----------
img4, d4 = base(4)
wrap(d4, ["「2075年に1億円」は", "今の3700万円"], MIN_L, 72, 130, 100, WHITE)
d4.text((76, 430), "インフレ2%で50年たつと", font=GO_R, fill=MUTE)
d4.text((76, 508), "物価は", font=GO_M, fill=MUTE)
d4.text((214, 486), "2.7倍", font=NUM, fill=CASH)
wrap(d4, ["額面の数字を大きく出すと", "気持ちはいい。",
          "でも、それで判断はできない。"], GO_M, 76, 690, 68, SUB)
wrap(d4, ["このツールが大きく出すのは", "今のお金に直した額です。",
          "額面は括弧の中に小さく置きました。"], GO_R, 76, 960, 56, MUTE)
d4.rectangle([76, 1190, W - 76, 1193], fill=LINE)
d4.text((76, 1226), "甘い数字で安心するのが、いちばんあぶない", font=GO_S, fill=DIM)

# ---------- 5枚目：使い方 ----------
img5, d5 = base(5)
wrap(d5, ["入れるのは", "2つだけ"], MIN_L, 72, 150, 96, WHITE)
y = 430
for t in ["年齢", "手取り年収"]:
    d5.rounded_rectangle([72, y, 640, y + 96], radius=10,
                         outline=PRIN, width=3, fill=(32, 39, 62))
    d5.text((104, y + 24), t, font=GO_B, fill=SUB)
    y += 124
wrap(d5, ["教育費も年金も介護費も", "標準値が入っているので",
          "調べなくて大丈夫。"], GO_R, 76, 700, 52, MUTE)
wrap(d5, ["入力はブラウザの中だけ。", "どこにも送信されません。"], GO_S, 76, 890, 44, DIM)
d5.rectangle([72, 1150, W - 72, 1153], fill=LINE)
d5.text((72, 1186), "winnow-00.github.io/kakei50", font=MONO, fill=SUB)
d5.text((72, 1240), "プロフィールのリンクから", font=GO_S, fill=DIM)

for i, im in enumerate([img1, img2, img3, img4, img5], 1):
    p = os.path.join(OUT, "insta_{}.png".format(i))
    im.save(p, "PNG", optimize=True)
    print("saved:", os.path.basename(p))
