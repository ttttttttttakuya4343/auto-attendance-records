# 勤怠表自動作成ツール

CSVファイルから勤怠データを読み込み、Excelテンプレートに自動入力するツールです。

## 前提条件
- **Python**: Python 3.6 以上
- **CSVファイル**: ジョブカンからダウンロードした勤怠データを使用してください
- **Excelテンプレート**: 自社から提供される勤務表テンプレートを使用してください

## 機能
- CSVファイルから出勤時刻、退勤時刻、休憩時間を抽出
- Excelテンプレートに自動入力
- テンプレートファイル名から月情報を保持した出力ファイル名を自動生成
- Web版（GUI）とコマンドライン版を提供

## セットアップ

### 1. リポジトリをクローン
```bash
git clone <repository-url>
cd auto-attendance-records
```

### 2. 環境セットアップ
```bash
python setup.py
```

## 使用方法

### 簡単実行（推奨）
```bash
python run.py
```

### 手動実行

#### Web版（GUI）
```bash
python main.py
```

ブラウザが自動で開き、以下のようなシンプルなWebインターフェースが表示されます：

![GUIスクリーンショット](images/スクリーンショット%202025-09-02%20午前9.40.34.png)

**GUIイメージ:**
- タイトル: 「勤怠表自動作成ツール」
- 作業者名入力フィールド
- CSVファイルアップロードボタン
- Excelテンプレートアップロードボタン
- 「勤怠表を作成」実行ボタン

**操作手順:**
1. 作業者名を入力
2. CSVファイルをアップロード（ジョブカンからダウンロードしたファイル）
3. Excelテンプレートをアップロード（自社提供のテンプレート）
4. 「勤怠表を作成」ボタンをクリック
5. 作成されたファイルが自動でダウンロードされます

#### コンソール版（対話形式）
```bash
python apps/simple_app.py
```

実行後、以下の順番で入力してください：
1. 作業者名を入力
2. CSVファイルのパスを入力（例：`data/csv/attendance-record.csv`）
3. Excelテンプレートのパスを入力（例：`data/template/Quco_〇〇_2025年8月度勤務表・立替経費精算書.xlsx`）

作成されたファイルは `data/output/` ディレクトリに保存されます。

#### 詳細コマンドライン版
```bash
python src/cli_app.py --csv CSVファイルパス --template Excelテンプレートパス --output 出力ファイルパス --name 作業者名
```

## ファイル構成
```
auto-attendance-records/
├── apps/                    # アプリケーション
│   ├── __init__.py         # パッケージ初期化
│   ├── web_app.py          # Webアプリケーション
│   └── simple_app.py       # シンプルコマンドライン版
├── src/                     # コアモジュール
│   ├── __init__.py         # パッケージ初期化
│   ├── attendance_processor.py  # メイン処理
│   └── cli_app.py          # 詳細コマンドライン版
├── tests/                   # テストコード
│   ├── __init__.py         # パッケージ初期化
│   ├── test_*.py           # 各機能のテスト
│   ├── run_all_tests.py    # 全テスト実行
│   └── test_data/          # テスト用データ
├── images/                  # スクリーンショット等
│   └── スクリーンショット 2025-09-02 午前9.40.34.png  # GUIスクリーンショット
├── data/                    # データフォルダ
│   ├── csv/                # CSVファイル置き場
│   ├── template/           # テンプレート置き場
│   └── output/             # 出力ファイル保存先
├── .flake8                  # Flake8設定
├── .gitignore               # Git除外ファイル
├── CHANGELOG.md             # 変更履歴
├── LICENSE                  # ライセンス
├── Makefile                 # 開発用コマンド
├── README.md                # プロジェクト説明
├── main.py                 # エントリーポイント
├── pyproject.toml           # プロジェクト設定
├── requirements.txt         # 依存関係
├── run.py                  # 簡単実行スクリプト
└── setup.py               # 環境セットアップ
```

## 注意事項

通常勤務、有給休暇以外の考慮はしていないため、勤務状況の変更を行なった日によっては正しくExcelに反映されてない場合があります。（例えば、慶弔休暇など）

通常勤務、有給休暇以外の申請を出してる場合、対象の日付の入力値を確認してください。

## テスト

### 全テスト実行
```bash
python tests/run_all_tests.py
```

### 個別テスト実行
```bash
# コア機能テスト
python -m unittest tests.test_attendance_processor

# CLIアプリテスト
python -m unittest tests.test_cli_app

# コンソールアプリテスト
python -m unittest tests.test_simple_app

# ファイル名生成テスト
python -m unittest tests.test_filename_generation
```

## トラブルシューティング

### 依存関係エラーが発生する場合
```bash
python setup.py
```

### 手動インストール
```bash
pip install -r requirements.txt
```

### ファイルが見つからないエラー
- CSVファイルのパスが正しいか確認してください
- Excelテンプレートファイルのパスが正しいか確認してください
- ファイル名に特殊文字が含まれていないか確認してください

### Excelファイルのエラー
- テンプレートファイルに「業務報告書（現場業務用）」シートが存在するか確認してください
- Excelファイルが破損していないか確認してください