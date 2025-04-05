"""Digital clock implementation using Pimoroni Inky PHAT.

Inky PHATを使用したデジタル時計の実装。
Raspberry Pi Zero 2とPIMORONI Inky PHATを使用してデジタル時計を表示します。

必要な外部パッケージ:
    python3-inkyphat, Pillow

動作環境:
    Raspberry Pi Zero 2, PIMORONI Inky PHAT
"""

import time  # 時間制御用ライブラリ
from datetime import datetime  # 時刻取得用ライブラリ
from inky import InkyPHAT  # Inky PHATライブラリ
from inky.auto import auto  # Inkyディスプレイの自動検出
from PIL import Image, ImageDraw, ImageFont  # 画像描画用ライブラリ


def main():
    """単純なデジタル時計を表示するメイン関数."""
    # 自動検出を使用してディスプレイを初期化
    display = auto()
    # ボーダーを白に設定して、見やすい表示に
    display.set_border(display.WHITE)
    WIDTH, HEIGHT = display.resolution

    # フォントの読み込み（指定されたパスが存在しない場合はデフォルトフォントを使用）
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 35)  # フォントサイズを48に変更
    except IOError:
        font = ImageFont.load_default()

    now = ""
    # 無限ループで時刻を更新して表示
    while True:
        # 現在時刻とnowが不一致であれば、時刻を更新
        if datetime.now().strftime("%Y/%m/%d\n%A\n%H:%M") == now:
            time.sleep(1)
            continue

        # 現在時刻を取得し、"年月日曜日\n時:分"形式にフォーマット
        now = datetime.now().strftime("%Y/%m/%d\n%A\n%H:%M")
        # 白背景のキャンバスを生成（Pモード：パレットモードはInkyディスプレイに適合）
        img = Image.new("P", (WIDTH, HEIGHT), color=display.WHITE)
        draw = ImageDraw.Draw(img)
        # 時刻文字のバウンディングボックスを取得して中央配置用の幅と高さを計算
        bbox = draw.textbbox((0, 0), now, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        x = (WIDTH - w) // 2  # X座標：中央配置
        y = (HEIGHT - h) // 2  # Y座標：中央配置

        # 黒色で時刻テキストを描画
        draw.text((x, y), now, font=font, fill=display.BLACK)

        # 画像を180度回転させる（時計回り）
        img = img.rotate(180, expand=True)  # 回転処理追加

        # 生成した画像をディスプレイへ設定し、表示を更新
        display.set_image(img)
        display.show()

        # 次の分境界まで待機するように修正
        now_dt = datetime.now()  # 現在時刻を再取得
        sleep_duration = 60 - now_dt.second - now_dt.microsecond / 1e6  # 次の分境界までの秒数
        time.sleep(sleep_duration)  # 待機


if __name__ == "__main__":
    main()
