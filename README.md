# Screen Translator

画面上のテキストを選択し、OCR と OpenAI を使って翻訳する Windows 向けデスクトップアプリです。

## 主な機能

- 任意の画面領域を選択して翻訳
- ライブ翻訳ポップアップ
- 翻訳結果のコピーと簡易履歴
- システムトレイ常駐

## 動作環境

- Windows
- Python 3.11 以上
- OpenAI API キー
- Tesseract OCR

## インストール

### 1. Python パッケージを入れる

```powershell
py -3.11 -m pip install -r requirements.txt
```

### 2. Tesseract OCR を用意する

- 通常利用では [UB Mannheim 版 Tesseract](https://github.com/UB-Mannheim/tesseract/wiki) のインストールを推奨します。
- 既定のインストール先は `C:\Program Files\Tesseract-OCR\tesseract.exe` です。
- 日本語を扱う場合は `Japanese script` と `Japanese vertical` の言語データも入れてください。

### 3. OpenAI API キーを設定する

次のどちらかで設定できます。

1. 環境変数 `OPENAI_API_KEY` を設定する
2. アプリ起動後に設定画面から入力する

PowerShell 例:

```powershell
$env:OPENAI_API_KEY = "sk-..."
```

## 設定ファイル

- 設定は `%LOCALAPPDATA%\ScreenTranslator\settings.json` に保存されます。
- 旧バージョンの `settings.json` がアプリフォルダにある場合は、新しい保存先へ 1 回だけ移行します。
- `OPENAI_API_KEY` が設定されている場合は、保存済みキーより環境変数が優先されます。
- リポジトリには実運用の `settings.json` を含めません。形式が必要な場合は `settings.example.json` を参照してください。

## 使い方

```powershell
py -3.11 main.py
```

1. 「画面を選択して翻訳」を押します。
2. 翻訳したい範囲をドラッグで選択します。
3. OCR と翻訳が完了すると結果が表示されます。
4. 必要に応じて「ライブ」や「コピー」を使います。

## 配布用 exe のビルド

```powershell
Remove-Item build, dist -Recurse -Force -ErrorAction SilentlyContinue
py -3.11 -m PyInstaller build.spec --clean --noconfirm
Compress-Archive -Path dist\ScreenTranslator\* -DestinationPath release\ScreenTranslator-win-x64.zip -Force
```

- `tesseract` フォルダが存在する場合はビルドに同梱されます。
- `settings.json` はビルド成果物に含めないでください。

## 公開前チェック

- `settings.json` や API キーがリポジトリに含まれていないこと
- `dist` と `build` をコミットしていないこと
- Release 用 zip に個人設定ファイルが含まれていないこと
- 現行の OpenAI API キーを失効し、新しいキーを各ユーザーが設定する運用にしていること

## ライセンス

Based on Screen-Translate (MIT License)
