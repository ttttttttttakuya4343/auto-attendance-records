#!/usr/bin/env python3
"""
勤怠表自動作成ツール（コマンドライン版）
"""

import argparse
import os
from attendance_processor import AttendanceProcessor


def main():
    parser = argparse.ArgumentParser(description="勤怠表自動作成ツール")
    parser.add_argument("--csv", required=True, help="CSVファイルのパス")
    parser.add_argument("--template", required=True, help="Excelテンプレートのパス")
    parser.add_argument("--output", required=True, help="出力ファイルのパス")
    parser.add_argument("--name", required=True, help="作業者名")

    args = parser.parse_args()

    # ファイル存在チェック
    if not os.path.exists(args.csv):
        print(f"エラー: CSVファイルが見つかりません: {args.csv}")
        return 1
    if not os.path.exists(args.template):
        print(f"エラー: Excelテンプレートが見つかりません: {args.template}")
        return 1

    try:
        print("勤怠表作成を開始します...")

        processor = AttendanceProcessor()
        processor.load_csv(args.csv)
        processor.load_excel_template(args.template)
        processor.process_attendance(args.name, args.output)

        print(f"完了: {args.output}")
        return 0

    except Exception as e:
        print(f"エラー: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
