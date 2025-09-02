#!/usr/bin/env python3
"""
ファイル名生成のテストコード
"""

import unittest
import re


class TestFilenameGeneration(unittest.TestCase):

    def test_filename_replacement(self):
        """ファイル名置換テスト"""
        test_cases = [
            {
                "template": "Quco_〇〇_2025年8月度勤務表・立替経費精算書.xlsx",
                "employee": "山田太郎",
                "expected": "Quco_山田太郎_2025年8月度勤務表・立替経費精算書.xlsx",
            },
            {
                "template": "Quco_テスト_2025年9月度勤務表・立替経費精算書.xlsx",
                "employee": "田中花子",
                "expected": "Quco_田中花子_2025年9月度勤務表・立替経費精算書.xlsx",
            },
            {
                "template": "Quco_サンプル_2024年12月度勤務表・立替経費精算書.xlsx",
                "employee": "佐藤次郎",
                "expected": "Quco_佐藤次郎_2024年12月度勤務表・立替経費精算書.xlsx",
            },
        ]

        for case in test_cases:
            with self.subTest(case=case):
                result = re.sub(
                    r"Quco_[^_]+_", f'Quco_{case["employee"]}_', case["template"]
                )
                self.assertEqual(result, case["expected"])

    def test_filename_pattern_matching(self):
        """ファイル名パターンマッチングテスト"""
        # 正規表現がマッチするパターン
        valid_patterns = [
            "Quco_〇〇_2025年8月度勤務表・立替経費精算書.xlsx",
            "Quco_テスト_勤務表・立替経費精算書.xlsx",
            "Quco_ABC_何かのファイル.xlsx",
        ]

        for pattern in valid_patterns:
            with self.subTest(pattern=pattern):
                match = re.search(r"Quco_[^_]+_", pattern)
                self.assertIsNotNone(match)

    def test_filename_no_match(self):
        """マッチしないファイル名のテスト"""
        invalid_patterns = [
            "勤務表・立替経費精算書.xlsx",
            "Quco勤務表.xlsx",
            "Quco_.xlsx",
        ]

        for pattern in invalid_patterns:
            with self.subTest(pattern=pattern):
                # マッチしない場合は元のファイル名がそのまま返される
                result = re.sub(r"Quco_[^_]+_", "Quco_テスト_", pattern)
                if "Quco_" not in pattern:
                    self.assertEqual(result, pattern)


if __name__ == "__main__":
    unittest.main()
