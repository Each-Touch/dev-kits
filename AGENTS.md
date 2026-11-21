# Each-Touch Dev Kits — Autonomous Operating Manual (`AGENTS.md`)

> Scope: `/Users/zhaozixu/.gemini/antigravity/scratch/dev-kits`
> Schedule: Tue/Fri 17:00 Asia/Shanghai
> Positioning: High-Margin Zero-Dependency Commercial Source Kits, Canvas Engines & Creator Toolkits (Higher-Ticket Tier `$4.99–$7.99` + Interactive Web Playground + Free Lite Demo — ZERO Generative AI).

## Strict Red Lines
1. **Zero Collision**: NEVER touch `运营总台/`, `game-studio-ops/`, `each-touch-arcade/`, `forge-tools/`, `asset-lab/`, `print-play-lab/`, or existing personal `ego-browser` spaces (`2, 3, 27, 31, 50, 51, 54, 61, 77`).
2. **Paywall Protection**: Paid Full Commercial Kits MUST match `releases/*/*-full-*` or `releases/*/paid_*` so `.gitignore` blocks them from public GitHub repos! Only public playgrounds, docs, and Lite demos go to GitHub Pages; full source kits upload ONLY to `itch.io` behind the Paid paywall.
3. **Automated Tests Required**: Every kit MUST include automated `node --test` unit tests covering all public modules, and tests MUST pass 100% before packaging or deploying.
4. **Zero External CDNs / Zero Generative AI**: 100% zero-dependency ES Modules + TypeScript `.d.ts` declarations; `Generative AI disclosure` on itch.io MUST be `No`.
5. **Browser & Visual Audit Gate**: Fresh temporary `taskSpace(...)`, close with `await task.finish({ keep: [] })`; never `read_file` PNGs in main conversation (`research` `Model: "pro"` only). Never submit personal tax/bank forms.

## 5-Stage Autonomous Production Loop
1. Run `python3 scripts/fetch_metrics.py` & inspect `https://itch.io/dashboard` (read-only); pick next `TODO` from `ops/01_高客单开发者套件排期池.md` (`IN_PROGRESS`).
2. Implement zero-dependency source kit + TypeScript `.d.ts` + `node --test` unit tests + live browser interactive playground in `docs/<slug>/` + `630x500` cover; run `package_kit.py` & `build_showcase.py`.
3. Run temporary HTTP QA (`1280x800` & `390x844`, interactive playground clicks + zero errors/overflow) and `research` (`Model: "pro"`) visual audit until `VERDICT: PASS`.
4. Verify `git status` excludes Paid Full ZIPs, push `Each-Touch/dev-kits` `main`, verify `https://each-touch.github.io/dev-kits/` `HTTP 200`; publish to `itch.io` (`Classification: Tools`, `Kind: Downloadable`, `Paid` `$4.99–$7.99`, Lite Demo checked Demo, `Generative AI: No`), publish `Public`, verify live Buy/Demo CTAs.
5. Update `kits-catalog.json` with live `itchUrl`, rebuild showcase, mark `DONE`, log metrics & lessons in `ops/00..02`, commit & push.
