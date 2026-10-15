# -*- coding: utf-8 -*-
"""旧 URL（oshimane.github.io）に置く「転送専用」サイトを生成する（2026-10-15 移行）。

GitHub Pages はサーバー側の 301 を出せないので、各ページを次の 3 段で転送する:
  1. <link rel="canonical"> で新 URL を正と宣言（検索エンジンの評価を新 URL へ寄せる）
  2. <meta http-equiv="refresh" content="0"> で即転送（JS が無効でも動く）
  3. location.replace() でクエリと #アンカーも引き継いで転送（履歴に旧 URL を残さない）
さらに 404.html で「存在しないパス」も同じパスの新 URL へ送る（古い共有リンクの取りこぼし防止）。
旧サイトは noindex にして、検索結果から徐々に新 URL へ置き換わるようにする。

    python3 tools/make_legacy_redirect.py <出力先ディレクトリ>

出力先は旧リポジトリ（oshimane/oshimane.github.io）の作業ツリー。LP 本体（このリポジトリ）の
HTML のパス一覧から、同じパスの転送ページを作る。
"""
import sys
from html import escape
from pathlib import Path

NEW = 'https://sodemane.github.io'
ROOT = Path(__file__).resolve().parents[1]

PAGE = '''<!doctype html>
<html lang="ja"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex">
<title>ソデマネ（移転しました）</title>
<link rel="canonical" href="{url}">
<meta http-equiv="refresh" content="0; url={url}">
<script>location.replace({js_base} + location.search + location.hash);</script>
<style>body{{font-family:-apple-system,"Hiragino Sans",sans-serif;background:#fff7fb;color:#2b1b26;margin:0;padding:48px 16px;text-align:center;line-height:1.8}}a{{color:#d61f69}}</style>
</head><body>
<p>「推しマネ」は「ソデマネ」に名前が変わり、サイトも移転しました。</p>
<p><a href="{url}">{url}</a></p>
</body></html>
'''

NOT_FOUND = '''<!doctype html>
<html lang="ja"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex">
<title>ソデマネ（移転しました）</title>
<script>location.replace("{new}" + location.pathname + location.search + location.hash);</script>
</head><body style="font-family:sans-serif;text-align:center;padding:48px 16px">
<p>サイトは移転しました: <a href="{new}/">{new}/</a></p>
</body></html>
'''


def main(out: Path) -> None:
    pages = sorted(p.relative_to(ROOT) for p in ROOT.rglob('*.html')
                   if not any(part.startswith('.') or part in ('tools', 'node_modules') for part in p.parts))
    for rel in pages:
        path = '/' if rel.as_posix() == 'index.html' else '/' + rel.as_posix()
        url = NEW + path
        js_base = '"' + url.replace('"', '') + '"'
        dst = out / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(PAGE.format(url=escape(url), js_base=js_base), encoding='utf-8')
        print('redirect', rel, '->', url)
    (out / '404.html').write_text(NOT_FOUND.format(new=NEW), encoding='utf-8')
    (out / 'robots.txt').write_text('User-agent: *\nAllow: /\n', encoding='utf-8')
    (out / 'README.md').write_text(
        '# oshimane.github.io（転送専用）\n\n'
        '2026-10-15 に「推しマネ」は「ソデマネ」へ改名し、LP は https://sodemane.github.io/ に移転した。\n'
        'このリポジトリは旧 URL を他者に取られないよう**確保しておくため**と、古いリンクを同じパスへ\n'
        '転送するためだけに残している。中身は LP repo の `tools/make_legacy_redirect.py` が生成する。\n'
        '**ここを直接編集しない。**\n', encoding='utf-8')
    print('404.html / robots.txt / README.md')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit('usage: make_legacy_redirect.py <出力先>')
    main(Path(sys.argv[1]).resolve())
