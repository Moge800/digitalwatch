#!/bin/bash
# digitalwatch.service を自動生成し、システムに登録するスクリプト

# サービスファイル名とシステムディレクトリの定義
SERVICE_FILE="digitalwatch.service"
TARGET_DIR="/etc/systemd/system"

# 追加: カレントディレクトリ、launch.shのパス、ユーザー名を自動取得
LAUNCH_PATH="$(pwd)/launch.sh"        # launch.sh のフルパスを生成
WORKING_DIR="$(pwd)"                # カレントディレクトリを取得
CURRENT_USER="$(whoami)"            # 現在のユーザー名を取得

# CURRENT_USER の存在チェック。存在しなければ代替ユーザーとして root を使用
if id "$CURRENT_USER" >/dev/null 2>&1; then
    USER_TO_USE="$CURRENT_USER"  # 指定ユーザーが存在する場合
else
    echo "指定ユーザー $CURRENT_USER は存在しません。代替ユーザー（root）を使用します。"
    USER_TO_USE="root"
fi

# USER_TO_USE に応じたホームディレクトリの設定
if [ "$USER_TO_USE" = "root" ]; then
    HOME_DIR="/root"  # root の場合は /root
else
    HOME_DIR="/home/${USER_TO_USE}"  # それ以外は /home/<ユーザー名>
fi

# サービスユニットファイルを自動生成（改修: 各行のコメントは別行に移動）
cat << EOF > "$SERVICE_FILE"
[Unit]
# サービスの説明
Description=Digital Watch Service
# ネットワーク起動後に開始
After=network.target

[Service]
# launch.sh を bash で実行
ExecStart=/bin/bash ${LAUNCH_PATH}
# 作業ディレクトリを自動取得
WorkingDirectory=${WORKING_DIR}
# 異常終了時に再起動
Restart=always
# 追加: 起動失敗後5秒待機を設定
RestartSec=5
# チェック済みのユーザーを使用
User=${USER_TO_USE}
# HOME を明示的に設定
Environment=HOME=${HOME_DIR}

[Install]
WantedBy=multi-user.target
EOF

# サービスファイルをシステムディレクトリへコピー
sudo cp "$SERVICE_FILE" "$TARGET_DIR/"

# systemd のデーモンを再読み込みし、サービスを有効化・起動
sudo systemctl daemon-reload
sudo systemctl enable digitalwatch.service
sudo systemctl start digitalwatch.service

echo "digitalwatch.service の登録が完了しました。"

# サービス状態を確認し、結果を表示する処理を改善
SERVICE_STATUS=$(sudo systemctl is-active digitalwatch.service)  # サービス状態を取得
if [ "$SERVICE_STATUS" = "active" ]; then
    echo "digitalwatch.service は正常に稼働中です。"
else
    echo "digitalwatch.service は稼働していません。"
    echo "詳細な状態を表示します:"  # 詳細なサービス状態を出力
    sudo systemctl status digitalwatch.service
    echo "直近5分間のサービスログを確認してください:"  # ログ出力
    sudo journalctl -u digitalwatch.service --since "5 minutes ago"
fi
