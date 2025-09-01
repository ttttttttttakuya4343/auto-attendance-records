#!/usr/bin/env python3
"""
環境セットアップスクリプト
"""

import subprocess
import sys
import os

def check_python_version():
    """Python バージョンチェック"""
    if sys.version_info < (3, 7):
        print("Python 3.7以上が必要です")
        sys.exit(1)
    print(f"Python {sys.version} 検出")

def install_requirements():
    """依存関係をインストール"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("依存関係のインストール完了")
    except subprocess.CalledProcessError:
        print("依存関係のインストールに失敗しました")
        sys.exit(1)

def check_dependencies():
    """依存関係の動作確認"""
    try:
        import pandas
        import openpyxl
        print("依存関係の動作確認: OK")
        return True
    except ImportError as e:
        print(f"依存関係が利用できません: {e}")
        return False

def main():
    print("=== 勤怠表自動作成ツール セットアップ ===")
    
    check_python_version()
    install_requirements()
    
    if not check_dependencies():
        print("\n【重要】依存関係が不足しています")
        print("以下のコマンドで再インストールしてください:")
        print("pip install -r requirements.txt")
    else:
        print("\n✅ セットアップ完了!")
        print("Web版: python main.py")
        print("CLI版: python src/cli_app.py --help")

if __name__ == "__main__":
    main()