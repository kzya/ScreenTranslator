# セットアップガイド

このガイドは、**リポジトリを clone した直後の状態**から Screen Translator を動かすための最短手順です。

## 1. リポジトリのルートへ移動

```powershell
git clone https://github.com/kzya/ScreenTranslator.git
cd ScreenTranslator
```

すでに clone 済みなら、このリポジトリのルートで作業してください。

## 2. Python を確認

```powershell
py -3.11 --version
```

`py` が使えない場合は Python 3.11 をインストールしてから再度確認してください。

## 3. 依存パッケージをインストール

```powershell
py -3.11 -m pip install -r requirements.txt
```

## 4. Tesseract OCR をインストール

1. [UB Mannheim 版 Tesseract](https://github.com/UB-Mannheim/tesseract/wiki) をダウンロード
2. 既定のインストール先のままセットアップ
3. 日本語を使う場合は `Japanese script` と `Japanese vertical` を選択

既定のパス:

```text
C:\Program Files\Tesseract-OCR\tesseract.exe
```

## 5. OpenAI API キーを設定

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

## 6. アプリを起動

```powershell
py -3.11 main.py
```

## 7. テストを実行

```powershell
py -3.11 -m unittest discover -s tests -v
```

## 8. 配布用 exe を作成

### いちばん簡単な方法

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\build_release.ps1
```

### 手動で行う場合

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
- 発信時は `docs/LAUNCH_KIT.md` をそのまま叩き台に使う
