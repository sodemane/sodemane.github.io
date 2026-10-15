# oshimane-lp — 編集ガードレール（必読）

本repoはソデマネLPの**単一正典**（本番 https://sodemane.github.io/ ・push=即本番反映。旧 https://oshimane.github.io/ は転送専用＝2026-10-15 移行・`tools/make_legacy_redirect.py`）。
コピーの正本ルール = `~/dev/oshikatsu-app/.gtm-loop/gtm-brand-charter.md`（GTM Brand Charter）。**LPを編集する前に必ずcharterを読むこと。**

## 誠実コピー（絶対・違反はpush禁止）

- 実装にない動作（**予約/購入/手配/支払い/自動収集/代行/送金**）を匂わせない。実機能=監視・通知・記録・可視化・シミュのみ。
- 実装に存在しない機能を訴求しない（例: 「レポートでふり返り」は未実装のため2026-07-17に削除済み。復活させる前に実装の存在を `~/dev/oshikatsu-app/.feature-audit/feature-stories.json` で確認）。
- 架空実績・捏造レビュー・実在しないユーザー数の禁止。登録者数は実数のみ（50未満は「受付中」表示）。

## C2ルール（裁定 2026-07-17・無料/有料の境界）

- 無料=コア機能全部＋**推し1人**＋プリセット色着せ替え。有料（検証中）=系スキン・自由色・写真背景・**複数推しの管理**。
- **「ぜんぶ無料」「全機能無料」と書くときは必ず「推し1人」の限定を併記**する（無限定の全機能無料表現は禁止）。

## C11ルール（裁定 2026-07-17・系スキンの段階公開）

- 公開ビルドは**STARのみ**。NOIR/NEON/DREAM/SPLASHは「近日公開」表記必須＝今すぐ選べるかのような見せ方禁止（各系の解禁時に解除）。

## 運用

- `noindex` の解除・`CONFIG.MODE`（prereg/beta/launch）切替・`BETA_URL`/`STORE_URL`/`ENDPOINT` の変更は**T-dayランブック**（vault `output/oshikatsu-app/launch-runbook_*.html`）に従う。勝手に切り替えない。
- 価格のA/B variant（`PRICING`）と価格の「仮・検証中」留保文言を消さない（有利誤認回避）。
- 特商法11条表示は有料化（G7）時に整備（暫定解釈=注文手段のないリードジェネLPは対象外。**G3前にlegal-reviewで正式確定**・charter §tokushoho参照）。
- 編集後は `~/dev/oshikatsu-app/.gtm-loop/scripts/gtm_copy_lint.py --charter` を index.html に対して回すか、gtm-content-check（LLM審査）を通す。**リンタ通過≠C2準拠**（共起ルールはLLM審査のみが検査できる）。
- vault側 `output/oshikatsu-app/lp-live-snapshot_*.html` は閲覧用スナップショット＝手編集禁止。privacy.html/terms.htmlはrepoとvault両方を同期。
