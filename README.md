# 勤怠表自動作成ツール

CSVファイルから勤怠データを読み込み、Excelテンプレートに自動入力するツールです。

## 機能
- CSVファイルから出勤時刻、退勤時刻、休憩時間を抽出
- Excelテンプレートに自動入力
- Web版とコマンドライン版を提供

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

#### Web版
```bash
python main.py
```

#### コマンドライン版
```bash
python apps/simple_app.py
```

#### 詳細コマンドライン版
```bash
python src/cli_app.py --csv CSVファイルパス --template Excelテンプレートパス --output 出力ファイルパス --name 作業者名
```

## ファイル構成
```
auto-attendance-records/
├── apps/                    # アプリケーション
│   ├── web_app.py          # Webアプリケーション
│   └── simple_app.py       # シンプルコマンドライン版
├── src/                     # コアモジュール
│   ├── attendance_processor.py  # メイン処理
│   └── cli_app.py          # 詳細コマンドライン版
├── main.py                 # エントリーポイント
├── run.py                  # 簡単実行スクリプト
├── setup.py               # 環境セットアップ
└── requirements.txt       # 依存関係
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