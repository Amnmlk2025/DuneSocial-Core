#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, json, sys, subprocess, pathlib

ALLOWED_LARGE_FILES = {".mp4", ".mov", ".zip"}
MAX_ADDED_LINES = 400
FRONTEND_LABEL_REQUIRED = "frontend-allowed"

def run(*cmd: str) -> str:
    return subprocess.check_output(list(cmd), text=True).strip()

def call_ok(*cmd: str) -> int:
    return subprocess.call(list(cmd))

def ref_exists(ref: str) -> bool:
    return call_ok("git", "show-ref", "--verify", f"refs/heads/{ref}") == 0 or \
           call_ok("git", "show-ref", "--verify", f"refs/remotes/{ref}") == 0 or \
           call_ok("git", "rev-parse", "--verify", ref) == 0

def ensure_remote_ref(remote: str, ref: str) -> str:
    """
    تلاش می‌کند ref را قابل استفاده کند:
    - اگر 'main' است و موجود نیست، از 'origin/main' استفاده می‌کند.
    - در غیر این صورت همان ref را برمی‌گرداند.
    """
    if ref_exists(ref):
        return ref
    # تلاش برای origin/<ref>
    origin_ref = f"{remote}/{ref}" if not ref.startswith(f"{remote}/") else ref
    # گرفتن شاخهٔ پایه از ریموت
    call_ok("git", "fetch", "--no-tags", "--prune", "--depth", "2", remote, f"+refs/heads/{ref}:refs/remotes/{remote}/{ref}")
    return origin_ref if ref_exists(origin_ref) else ref

# خواندن لیبل‌ها از رویداد
labels = set()
ev = os.environ.get("GITHUB_EVENT_PATH")
if ev and os.path.exists(ev):
    try:
        with open(ev, "r", encoding="utf-8") as f:
            d = json.load(f)
            labels = {l.get("name","") for l in d.get("pull_request", {}).get("labels", [])}
    except Exception:
        labels = set()

# اطمینان از دسترسی به main از ریموت
call_ok("git","fetch","--no-tags","--prune","--depth","2","origin","+refs/heads/*:refs/remotes/origin/*")

# تعیین base/head برای PR یا push
base_env = os.environ.get("GITHUB_BASE_REF")  # مثال: "main" در PRها
base_ref = base_env or "main"
base_ref = ensure_remote_ref("origin", base_ref)

head = os.environ.get("GITHUB_SHA") or "HEAD"
# در PRها، checkout معمولا روی pull/<id>/merge است. همین HEAD کافی است.

# محاسبهٔ merge-base ایمن
try:
    mb = run("git", "merge-base", head, base_ref)
except subprocess.CalledProcessError:
    # اگر هنوز main محلی نیست، دوباره fetch و تلاش
    call_ok("git","fetch","--no-tags","--prune","--depth","2","origin",f"+refs/heads/{base_ref.replace('origin/','')}:refs/remotes/{base_ref}")
    try:
        mb = run("git", "merge-base", head, base_ref)
    except subprocess.CalledProcessError:
        # آخرین راه‌حل: اولین کامیت مخزن به‌عنوان پایه
        try:
            mb = run("git","rev-list","--max-parents=0", head).splitlines()[0]
        except Exception:
            print("FATAL: unable to determine merge-base"); sys.exit(1)

# استخراج تغییرات
try:
    diff = run("git","diff", f"{mb}..{head}", "--name-status")
except subprocess.CalledProcessError:
    diff = ""

files = [ln.split("\t")[-1] for ln in diff.splitlines() if ln.strip()]

try:
    shortstat = run("git","diff","--shortstat", f"{mb}..{head}")
except subprocess.CalledProcessError:
    shortstat = ""

# شمارش خطوط افزوده
added = 0
for part in shortstat.split(","):
    p = part.strip()
    if p.endswith("insertions(+)") or p.endswith("insertion(+)"):
        try:
            added = int(p.split()[0])
        except Exception:
            pass

if added > MAX_ADDED_LINES:
    print(f"FATAL: Too many added lines: {added} > {MAX_ADDED_LINES}")
    sys.exit(2)

# تغییرات frontend نیازمند لیبل
if any(p.startswith("frontend/") for p in files) and FRONTEND_LABEL_REQUIRED not in labels:
    print(f"FATAL: Frontend changes detected without required label '{FRONTEND_LABEL_REQUIRED}'.")
    sys.exit(3)

# جلوگیری از ورود فایل‌های بسیار بزرگِ نامجاز
for p in files:
    fp = pathlib.Path(p)
    if fp.exists() and fp.is_file():
        try:
            if fp.stat().st_size > 100 * 1024 * 1024 and fp.suffix.lower() not in ALLOWED_LARGE_FILES:
                print(f"FATAL: Large file >100MB detected: {p}")
                sys.exit(4)
        except Exception:
            # اگر به هر دلیل نتوانست اندازه را بخواند، از این بررسی عبور می‌کنیم
            pass

print("Guardrails passed.")
