#!/usr/bin/env python3
"""Run JuiceBox 2D unit tests and package Paid Full Commercial ZIP + Free Lite Demo ZIP."""

from __future__ import annotations

import shutil
import subprocess
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PKG = ROOT / "packages" / "juicebox-2d"
REL = ROOT / "releases" / "juicebox-2d"
DOCS_JB = ROOT / "docs" / "juicebox-2d"

LITE_JS = """/**
 * JuiceBox 2D — Free Lite Demo (2 of 12 Modules: CameraShake + Hitstop)
 * Upgrade to Full Commercial Kit ($5.99) for all 12 ES modules, TypeScript .d.ts,
 * 3 standalone HTML5 demos, unit tests, and commercial royalty-free license:
 * https://each-touch.itch.io/juicebox-2d-game-feel-kit
 */

export class CameraShake {
  constructor(opts = {}) {
    this.maxOffsetX = opts.maxOffsetX ?? 18;
    this.maxOffsetY = opts.maxOffsetY ?? 18;
    this.decayPerSec = opts.decayPerSec ?? 2.2;
    this.trauma = 0;
  }
  addTrauma(amount) { this.trauma = Math.min(1, Math.max(0, this.trauma + amount)); }
  update(dt) {
    this.trauma = Math.max(0, this.trauma - this.decayPerSec * dt);
    const s = this.trauma * this.trauma;
    return { x: (Math.random() * 2 - 1) * this.maxOffsetX * s, y: (Math.random() * 2 - 1) * this.maxOffsetY * s };
  }
}

export class Hitstop {
  constructor() { this.remaining = 0; }
  trigger(seconds) { this.remaining = Math.max(this.remaining, Math.max(0, seconds)); }
  step(dt) {
    if (this.remaining <= 0) return false;
    this.remaining = Math.max(0, this.remaining - dt);
    return true;
  }
}
"""

LITE_README = """JuiceBox 2D — Free Lite Demo (2 of 12 Modules)

Included in this Free Lite Demo:
- juicebox2d-lite.mjs (CameraShake + Hitstop preview)

Upgrade to the Full Commercial Kit ($5.99 USD) to unlock all 12 Modules + TypeScript .d.ts:
1. CameraShake   2. Hitstop       3. SpringValue      4. ParticlePool
5. FloatingText  6. SquashStretch 7. HitFlash         8. MotionTrail
9. TimeScale    10. ImpactAudio  11. InputAssist     12. FpsMonitor
+ 3 Standalone Playable HTML5 Demos + Full node --test Unit Test Suite + Commercial License

Get the Full Kit: https://each-touch.itch.io/juicebox-2d-game-feel-kit
Try Live Interactive Playground: https://each-touch.github.io/dev-kits/juicebox-2d/
"""


def main() -> int:
    # 1. Run unit tests — hard fail if any test fails
    res = subprocess.run(["node", "--test", str(PKG / "tests" / "juicebox.test.mjs")], capture_output=True, text=True)
    print(res.stdout)
    if res.returncode != 0:
        print(res.stderr)
        raise RuntimeError("JuiceBox 2D unit tests failed!")

    REL.mkdir(parents=True, exist_ok=True)
    DOCS_JB.mkdir(parents=True, exist_ok=True)

    # 2. Build Paid Full Commercial Kit ZIP (gitignored!)
    full_zip = REL / "juicebox-2d-full-commercial-kit-v1.0.zip"
    with zipfile.ZipFile(full_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for fp in sorted(PKG.rglob("*")):
            if fp.is_dir():
                continue
            rel = fp.relative_to(PKG).as_posix()
            zf.write(fp, arcname=f"juicebox-2d/{rel}")

    # 3. Build Free Lite Demo ZIP (2 modules + upgrade guide)
    lite_zip = REL / "juicebox-2d-free-lite-demo.zip"
    with zipfile.ZipFile(lite_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("juicebox2d-lite.mjs", LITE_JS.encode("utf-8"))
        zf.writestr("README-UPGRADE.txt", LITE_README.encode("utf-8"))

    # Also copy lite demo zip into docs/demos/ for GitHub Pages download
    docs_demo = ROOT / "docs" / "demos" / "juicebox-2d-free-lite-demo.zip"
    docs_demo.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(lite_zip, docs_demo)

    for zp in (full_zip, lite_zip):
        with zipfile.ZipFile(zp, "r") as zf:
            assert zf.testzip() is None
            print(f"Verified ZIP {zp.name}: {len(zf.namelist())} files, {zp.stat().st_size} bytes")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
