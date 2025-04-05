import time
from inky.auto import auto
from PIL import Image, ImageDraw, ImageFont  # ImageDrawとImageFontを追加

display = auto()  # Inkyディスプレイの自動検出
print(display.colour, display.resolution)
WIDTH, HEIGHT = display.resolution

display.set_border(display.WHITE)  # ボーダーは白で設定

# 白背景のキャンバスを作成
img = Image.new("P", (WIDTH, HEIGHT), color=display.WHITE)
draw = ImageDraw.Draw(img)

# フォント読み込み（パスは環境に合わせて調整してください）
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
except IOError:
    font = ImageFont.load_default()  # フォントが無い場合はデフォルトフォントを利用

# 表示するメッセージ
message = "Hello World"

# テキストのバウンディングボックスを取得し、中央に配置
bbox = draw.textbbox((0, 0), message, font=font)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]

x = (WIDTH - text_width) // 2  # 中央配置のX座標
y = (HEIGHT - text_height) // 2  # 中央配置のY座標

# テキスト描画（文字色はディスプレイで定義されたBLACKを利用）
draw.text((x, y), message, fill=display.BLACK, font=font)

display.set_image(img)  # 画像をディスプレイにセット
print("Displaying image...")
display.show()  # 画像の表示を更新

# time.sleep(10)