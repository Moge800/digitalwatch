#!/bin/bash

# プロジェクトディレクトリに移動（現在のスクリプトがあるディレクトリへ）
cd "$(dirname "$0")" || exit 1
# 環境を設定
source .venv/bin/activate
pip install inky  # 追加: inkyライブラリをインストールして不足モジュールに対応
# Pythonスクリプトを実行（Python3のパスを正しく記述）
exec python main.py
