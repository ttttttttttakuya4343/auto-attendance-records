#!/usr/bin/env python3
"""
勤怠表自動作成ツール
CSVファイルから勤怠データを読み込み、Excelテンプレートに自動入力するWebアプリケーション
"""

import sys
import os

# モジュールパスを追加
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'apps'))

# Webアプリケーションを起動
try:
    from apps.web_app import start_server
    start_server()
except KeyboardInterrupt:
    print("\nアプリケーションを終了しました")