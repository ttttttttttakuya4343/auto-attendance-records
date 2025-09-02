#!/usr/bin/env python3
"""
全テストを実行するスクリプト
"""

import unittest
import sys

# パスを追加
sys.path.append(".")
sys.path.append("src")


def run_all_tests():
    """全テストを実行"""
    # テストディスカバリー
    loader = unittest.TestLoader()
    start_dir = "tests"
    suite = loader.discover(start_dir, pattern="test_*.py")

    # テスト実行
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # 結果の表示
    print(f"\n{'='*50}")
    print("テスト結果:")
    print(f"実行テスト数: {result.testsRun}")
    print(f"失敗: {len(result.failures)}")
    print(f"エラー: {len(result.errors)}")

    if result.failures:
        print("\n失敗したテスト:")
        for test, traceback in result.failures:
            print(f"- {test}")

    if result.errors:
        print("\nエラーが発生したテスト:")
        for test, traceback in result.errors:
            print(f"- {test}")

    # 成功判定
    success = len(result.failures) == 0 and len(result.errors) == 0
    print(f"\n全体結果: {'成功' if success else '失敗'}")
    print(f"{'='*50}")

    return success


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
