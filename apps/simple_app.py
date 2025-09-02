#!/usr/bin/env python3
"""
勤怠表自動作成ツール（シンプル版）
"""

import sys
import os
import re
import traceback

sys.path.append("src")

from attendance_processor import AttendanceProcessor  # noqa: E402


def main():
    print("=== 勤怠表自動作成ツール ===")

    # 作業者名入力
    employee_name = input("作業者名を入力してください: ").strip()
    if not employee_name:
        print("❌ 作業者名が入力されていません")
        return

    # CSVファイルパス入力
    csv_path = input("CSVファイルのパスを入力してください: ").strip()
    if not csv_path or not os.path.exists(csv_path):
        print(f"❌ CSVファイルが見つかりません: {csv_path}")
        return

    # Excelテンプレートパス入力
    template_path = input("Excelテンプレートのパスを入力してください: ").strip()
    if not template_path or not os.path.exists(template_path):
        print(f"❌ Excelテンプレートが見つかりません: {template_path}")
        return

    try:
        processor = AttendanceProcessor()

        print("📄 CSVファイル読み込み中...")
        processor.load_csv(csv_path)

        print("📊 Excelテンプレート読み込み中...")
        processor.load_excel_template(template_path)

        print("⚙️  勤怠データ処理中...")
        # 出力ディレクトリを作成
        os.makedirs("data/output", exist_ok=True)
        # テンプレートファイル名から出力ファイル名を生成

        filename = re.sub(
            r"Quco_[^_]+_", f"Quco_{employee_name}_", processor.template_filename
        )
        output_path = f"data/output/{filename}"
        processor.process_attendance(employee_name, output_path)

        print(f"✅ 完了！出力ファイル: {output_path}")

    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    main()
