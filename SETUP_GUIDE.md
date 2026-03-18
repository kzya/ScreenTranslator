# セットアップガイド

## 1. Python を確認する

```powershell
py -3.11 --version
```

`py` が使えない場合は Python 3.11 をインストールしてから再度確認してください。

## 2. 依存パッケージを入れる

```powershell
cd C:\Users\nagat\Antigravity\screen_translate\screen_translator_mvp
py -3.11 -m pip install -r requirements.txt
```

## 3. Tesseract OCR を入れる

1. [UB Mannheim 版 Tesseract](https://github.com/UB-Mannheim/tesseract/wiki) をダウンロード
2. 既定のインストール先のままセットアップ
3. 日本語を使う場合は `Japanese script` と `Japanese vertical` を選択

## 4. OpenAI API キーを設定する

### 方法 A: 環境変数を使う

```powershell
$env:OPENAI_API_KEY = "sk-your-api-key-here"
```

### 方法 B: アプリ内設定を使う

1. アプリを起動
2. 「設定」を開く
3. API キーを保存

保存先:

```text
%LOCALAPPDATA%\ScreenTranslator\settings.json
```

環境変数 `OPENAI_API_KEY` がある場合は、保存済みのキーより優先されます。

## 5. アプリを起動する

```powershell
py -3.11 main.py
```

## 6. 配布用 exe を作る

```powershell
Remove-Item build, dist, release -Recurse -Force -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Path release -Force | Out-Null
py -3.11 -m PyInstaller build.spec --clean --noconfirm
Compress-Archive -Path dist\ScreenTranslator\* -DestinationPath release\ScreenTranslator-win-x64.zip -Force
```

## よくある確認ポイント

- `settings.json` を Git に含めない
- `dist` と `build` を Git に含めない
- Release 用 zip に個人の API キーが入っていない
- 公開前に古い OpenAI API キーを失効する
