#!/usr/bin/env python3
"""
勤怠表自動作成ツール - 簡単実行スクリプト
"""

import subprocess
import sys

def main():
    print("=== 勤怠表自動作成ツール ===")
    
    try:
        subprocess.run([sys.executable, "main.py"])
    except KeyboardInterrupt:
        print("\nアプリケーションを終了しました")
    except Exception as e:
        print(f"エラー: {e}")
        print("\n環境セットアップを実行してください:")
        print(f"   {sys.executable} setup.py")

if __name__ == "__main__":
    main()