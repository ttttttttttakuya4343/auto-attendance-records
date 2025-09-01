#!/usr/bin/env python3
"""
勤怠表自動作成ツール（シンプル版）
"""

import sys
import os
sys.path.append('src')

from attendance_processor import AttendanceProcessor

def main():
    print("=== 勤怠表自動作成ツール ===")
    
    # 作業者名入力
    employee_name = input("作業者名を入力してください: ").strip()
    if not employee_name:
        print("❌ 作業者名が入力されていません")
        return
    
    # CSVファイルパス
    csv_path = "data/csv/attendance-record-summary-20250901094168b4ebbfb1bc2.csv"
    if not os.path.exists(csv_path):
        print(f"❌ CSVファイルが見つかりません: {csv_path}")
        return
    
    # Excelテンプレートパス
    template_path = "data/template/Quco_山村拓也_2025年8月度勤務表・立替経費精算書.xlsx"
    if not os.path.exists(template_path):
        print(f"❌ Excelテンプレートが見つかりません: {template_path}")
        return
    
    try:
        processor = AttendanceProcessor()
        
        print("📄 CSVファイル読み込み中...")
        processor.load_csv(csv_path)
        
        print("📊 Excelテンプレート読み込み中...")
        processor.load_excel_template(template_path)
        
        print("⚙️  勤怠データ処理中...")
        output_path = f"Quco_{employee_name}_勤務表・立替経費精算書.xlsx"
        processor.process_attendance(employee_name, output_path)
        
        print(f"✅ 完了！出力ファイル: {output_path}")
        
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()