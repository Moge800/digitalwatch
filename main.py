"""Digital clock implementation using Pimoroni Inky PHAT.

Inky PHATを使用したデジタル時計の実装。
Raspberry Pi Zero 2とPIMORONI Inky PHATを使用してデジタル時計を表示します。

必要な外部パッケージ:
    python3-inkyphat, Pillow

動作環境:
    Raspberry Pi Zero 2, PIMORONI Inky PHAT
"""

import time
from datetime import datetime
from inky import InkyPHAT
from inky.auto import auto
from PIL import Image, ImageDraw, ImageFont

# 定数定義
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_SIZE = 35
UPDATE_INTERVAL = 1  # 画面更新チェック間隔（秒）
ROTATION_DEGREE = 180  # 画面回転角度


def get_formatted_time() -> str:
    """現在時刻を整形された文字列で取得。

    Returns:
        str: 年月日、曜日、時分を含む整形された時刻文字列
    """
    return datetime.now().strftime("%Y/%m/%d\n%A\n%H:%M")


def load_font(font_path: str, font_size: int) -> ImageFont.ImageFont:
    """指定されたパスからフォントを読み込み。

    Args:
        font_path: フォントファイルのパス
        font_size: フォントサイズ

    Returns:
        ImageFont: 読み込まれたフォントオブジェクト
    """
    try:
        return ImageFont.truetype(font_path, font_size)
    except IOError:
        # フォントファイルが見つからない場合はデフォルトフォントを使用
        return ImageFont.load_default()


def update_display(display, font: ImageFont.ImageFont, time_text: str) -> None:
    """ディスプレイに時刻を表示。

    Args:
        display: Inkyディスプレイオブジェクト
        font: 使用するフォント
        time_text: 表示する時刻文字列
    """
    width, height = display.resolution

    # 白背景のキャンバスを生成
    img = Image.new("P", (width, height), color=display.WHITE)
    draw = ImageDraw.Draw(img)

    # テキストの配置位置を計算（中央揃え）
    bbox = draw.textbbox((0, 0), time_text, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x, y = (width - w) // 2, (height - h) // 2

    # 時刻テキストを描画
    draw.text((x, y), time_text, font=font, fill=display.BLACK)

    # 画像を回転
    img = img.rotate(ROTATION_DEGREE, expand=True)

    # ディスプレイを更新
    display.set_image(img)
    display.show()


def calculate_sleep_time() -> float:
    """次の分境界までの待機時間を秒単位で計算。

    Returns:
        float: 次の分境界までの待機時間（秒）
    """
    now = datetime.now()
    return 60 - now.second - now.microsecond / 1e6


def main():
    """単純なデジタル時計を表示するメイン関数。"""
    try:
        # ディスプレイの初期化
        display = auto()
        display.set_border(display.WHITE)

        # フォントの読み込み
        font = load_font(FONT_PATH, FONT_SIZE)

        # 前回の表示時刻を空に初期化
        last_time = ""

        # メインループ
        while True:
            # 現在時刻を取得
            current_time = get_formatted_time()

            # 時刻が変化した場合のみディスプレイを更新
            if current_time != last_time:
                update_display(display, font, current_time)
                last_time = current_time
                # 次の分境界まで待機
                time.sleep(calculate_sleep_time())
            else:
                # 変化がなければ短い間隔で再チェック
                time.sleep(UPDATE_INTERVAL)

    except KeyboardInterrupt:
        # Ctrl+Cでの終了処理
        print("プログラムを終了します")
    except Exception as e:
        # 予期せぬエラーの処理
        print(f"エラーが発生しました: {e}")


if __name__ == "__main__":
    main()
