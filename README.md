# oshimane-lp（推しマネ LP・公開サイト）

推しマネの GitHub Pages 公開サイト。**このリポジトリが LP の唯一の正典（単一正典）**。

- リモート: `sodemane/sodemane.github.io`（origin）。旧 `oshimane/oshimane.github.io` は転送専用（remote 名 `oshimane-legacy`・中身は `tools/make_legacy_redirect.py` の出力だけ）
- 本番URL: **https://sodemane.github.io/**（2026-10-15 移行。旧 https://oshimane.github.io/ は同じパスへ転送）
- 現況（2026-07-17時点）: **公開中・`noindex`（検索エンジン非索引・直リンクでは閲覧可能）**。本ローンチ時に `noindex` を解除して索引を許可する。

## 単一正典ルール（重要）

LP（`index.html` 等）の編集は**必ずこのリポジトリで行い、commit/push して本番へ反映**する。これだけが「本物の LP」。

- LLMWiki vault（`output/oshikatsu-app/`）に置かれている LP は**閲覧用スナップショットが1本だけ**（`lp-live-snapshot_<YYYYMMDD_HHmmss>.html`）。**手編集禁止**。vault 側を直しても本番には反映されない。
- vault 側スナップショットを更新したいときは、このリポジトリの最新 `index.html` をコピーして作り直す（このリポジトリ → vault の一方向）。
- `privacy.html` / `terms.html` はこのリポジトリと vault の両方に置き、編集時は両方を同期する（安定ドキュメントのため複製可）。

## ファイル構成

- `index.html` … LP 本体（推しマネ）
- `privacy.html` … プライバシーポリシー
- `terms.html` … 利用規約
- `features/` … 機能詳細ページ（calendar / lottery / money）
- `assets/` … favicon / apple-touch-icon / OG画像 / スクリーンショット
- `screens/` … アプリ実機スクリーンショット素材
- `robots.txt` … クロール許可（`Allow: /`）。索引可否は各ページの `<meta name="robots">` が別途制御
- `sitemap.xml` … 公開6URL（index / calendar / lottery / money / privacy / terms）

## CONFIG.MODE（3局面の切替）

`index.html` 内 `<script>` 冒頭の `CONFIG` オブジェクトで、LP の局面を1点で切り替える。

```js
var CONFIG = {
  MODE: "prereg",     // "prereg" | "beta" | "launch"
  BETA_URL: "",         // TestFlight パブリックリンク（MODE="beta" のとき設定）
  STORE_URL: "",        // App Store / Google Play のURL（MODE="launch" のとき設定）
  ENDPOINT: "...",      // Google Apps Script の WebアプリURL（事前登録の送信先）
  REGISTERED_COUNT: 0,  // 事前登録の表示人数（★実数のみ。架空の数字は入れない）
  COUNT_MIN_SHOW: 50,   // この人数に達するまでは「受付中」表示のみ
  TRACK_EVENTS: true
};
```

| MODE | 用途 | 必須設定 | 挙動 |
|---|---|---|---|
| `prereg`（現行） | 事前登録受付 | `ENDPOINT` | フォームからメール登録を受け付け、GAS経由でスプレッドシートへ記録 |
| `beta` | TestFlight ベータ募集 | `BETA_URL` | 「無料で事前登録」ボタンが「ベータ版に参加する」に変わり、TestFlightリンクへ誘導 |
| `launch` | 公開後（ストア誘導） | `STORE_URL` | 「無料で事前登録」ボタンが「無料でダウンロード」に変わり、ストアURLへ遷移 |

切替手順: `MODE` を書き換え、対応する `BETA_URL` / `STORE_URL` を設定 → commit/push のみ（他のコード変更は不要）。

## 事前登録フォームの運用

- 送信先は `CONFIG.ENDPOINT`（Google Apps Script Webアプリ）。POSTボディ方式・PII(メール)はURLに乗せない。
- スパム対策（クライアント側）: honeypot フィールド（`#regHp`・視覚的に非表示）と、ページ読み込みからの経過秒数（`elapsed`）を送信payloadに含める。**判定（弾く/通す）はGAS側で行う**（このリポジトリのJSは検知データを送るだけで送信自体はブロックしない）。
- `REGISTERED_COUNT` はスプレッドシートの実登録数を手動で反映する運用（架空の数字を入れない）。

## 公開前ゲート（未クローズ）

- 独自ドメイン（未設定・任意）
- 本ローンチ時: 全ページの `noindex` を解除、`MODE` を `launch` に切替、`STORE_URL` を設定

## デプロイ

`main` ブランチへの push が GitHub Pages に自動反映される（Pages設定: `source[branch]=main`, `source[path]=/`）。
