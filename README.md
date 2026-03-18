# Screen Translator

画面上のテキストをドラッグで選択し、OCR と OpenAI でその場で翻訳する Windows 向けデスクトップアプリです。

**「コピペして翻訳サイトに持っていく手間」を減らす**ことを目的にした、実用寄りの小さなツールです。

- 任意の画面領域を選択して翻訳
- ライブ翻訳ポップアップ
- 翻訳結果のコピーと簡易履歴
- システムトレイ常駐

## こんな場面向け

- 海外アプリや英語 UI をすぐ読みたい
- ゲーム画面や動画プレイヤー上の文字をざっくり理解したい
- ブラウザやデスクトップアプリの一部だけを素早く訳したい
- OCR と翻訳を行き来する手間を減らしたい

## 技術スタック

- Python 3.11
- Tkinter
- Tesseract OCR
- OpenAI API
- PyInstaller

## クイックスタート

### 1. リポジトリを取得

```powershell
git clone https://github.com/kzya/ScreenTranslator.git
cd ScreenTranslator
```

### 2. 依存パッケージをインストール

```powershell
py -3.11 -m pip install -r requirements.txt
```

### 3. Tesseract OCR を用意

- [UB Mannheim 版 Tesseract](https://github.com/UB-Mannheim/tesseract/wiki) の利用を推奨します
- 既定のインストール先は `C:\Program Files\Tesseract-OCR\tesseract.exe` です
- 日本語を使う場合は `Japanese script` と `Japanese vertical` の言語データも入れてください

### 4. OpenAI API キーを設定

次のどちらかで設定できます。

1. 環境変数 `OPENAI_API_KEY` を使う
2. アプリ起動後に設定画面から入力する

PowerShell 例:

```powershell
$env:OPENAI_API_KEY = "sk-..."
```

### 5. 起動

```powershell
py -3.11 main.py
```

## 使い方

1. 「画面を選択して翻訳」を押します
2. 翻訳したい範囲をドラッグで選択します
3. OCR と翻訳が完了すると結果が表示されます
4. 必要に応じて「ライブ」や「コピー」を使います

## 設定ファイル

- 設定は `%LOCALAPPDATA%\ScreenTranslator\settings.json` に保存されます
- 旧バージョンの `settings.json` がアプリフォルダにある場合は、新しい保存先へ 1 回だけ移行します
- `OPENAI_API_KEY` が設定されている場合は、保存済みキーより環境変数が優先されます
- リポジトリには実運用の `settings.json` を含めません。形式が必要な場合は `settings.example.json` を参照してください

## テスト

```powershell
py -3.11 -m unittest discover -s tests -v
```

## 配布用 exe のビルド

最短なら付属スクリプトを使えます。

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\build_release.ps1
```

手動で行う場合:

```powershell
Remove-Item build, dist, release -Recurse -Force -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Path release -Force | Out-Null
py -3.11 -m PyInstaller build.spec --clean --noconfirm
Compress-Archive -Path dist\ScreenTranslator\* -DestinationPath release\ScreenTranslator-win-x64.zip -Force
```

- `tesseract` フォルダが存在する場合はビルドに同梱されます
- `settings.json` はビルド成果物に含めないでください

## 公開前チェック

- `settings.json` や API キーがリポジトリに含まれていないこと
- `dist` と `build` をコミットしていないこと
- Release 用 zip に個人設定ファイルが含まれていないこと
- 現行の OpenAI API キーを失効し、新しいキーを各ユーザーが設定する運用にしていること

## 発信用素材

公開時にそのまま使える文面や台本を `docs/LAUNCH_KIT.md` にまとめています。

- X 投稿案
- Shorts / TikTok 用の短い台本
- note 記事の構成案
- デモ撮影チェックリスト

## リポジトリ構成

```text
core/     OCR・翻訳・設定管理などのコア処理
ui/       Tkinter ベースの UI
tests/    単体テスト
docs/     発信用素材や補足ドキュメント
scripts/  ビルド補助スクリプト
```

## ライセンス

Based on Screen-Translate (MIT License)
