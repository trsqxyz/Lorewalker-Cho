# Lorewalker-Cho
Hearthstone's Deck Code Translator
Thanks python-hearthstone and https://gist.github.com/Tenchi2xh/68f20ed6531b4200a16b1cdcc0e84130

# 使い方
`python -m lorewalker_cho decode CODE NAME`

- CODE はハースストーンのデッキコードに対応しています。
- NAME は好きに名付けてください。(デフォルトは 'Great Deck!' です。)

# 必要なもの

- Python3

## from pip
- request
- click
- python-hearthstone

最初の使用でフォルダに `db.json` が作成されます。