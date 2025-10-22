#!/usr/bin/env python3
import os, json, sys, subprocess, pathlib

ALLOWED_LARGE_FILES = {".mp4", ".mov", ".zip"}
MAX_ADDED_LINES = 400
FRONTEND_LABEL_REQUIRED = "frontend-allowed"

def run(*cmd):
    return subprocess.check_output(list(cmd), text=True).strip()

# برچسب‌های PR از رویداد
labels = set()
ev = os.environ.get("GITHUB_EVENT_PATH")
if ev and os.path.exists(ev):
    with open(ev, "r", encoding="utf-8") as f:
        d = json.load(f)
        labels = {l.get("name","") for l in d.get("pull_request", {}).get("labels", [])}

# اطمینان از وجود main محلی و ریموت
subprocess.call([
    "git","fetch","--no-tags","--prune","--depth","50","origin",
    "+refs/heads/main:refs/heads/main",
    "+refs/heads/main:refs/remotes/origin/main"
])

base_ref = os.environ.get("GITHUB_BASE_REF") or "origin/main"
if base_ref == "main":
    base_ref = "origin/main"

head = os.environ.get("GITHUB_SHA") or "HEAD"

<<<<<<< HEAD
import subprocess
def safe(cmd):
    try: return subprocess.check_output(cmd, text=True).strip()
    except subprocess.CalledProcessError: return ""
# normalize base to remote ref and ensure it exists
if base == "main": base = "origin/main"
subprocess.call(["git","fetch","--no-tags","origin","+refs/heads/main:refs/remotes/origin/main"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
mb = safe(["git","merge-base","HEAD","origin/main"]) or "HEAD"
diff = run(["git","diff",f"{mb}..{head}","--name-status"])
files = [line.split("\t")[-1] for line in diff.splitlines() if line]
shortstat = run(["git","diff","--shortstat",f"{mb}..{head}"])
=======
# محاسبه merge-base ایمن
try:
    mb = run("git","merge-base", head, base_ref)
except subprocess.CalledProcessError:
    mb = run("git","rev-parse", base_ref)
>>>>>>> origin/main

# Diff بین merge-base و HEAD
diff = run("git","diff", f"{mb}..{head}", "--name-status")
files = [ln.split("\t")[-1] for ln in diff.splitlines() if ln]
shortstat = run("git","diff","--shortstat", f"{mb}..{head}")

# خطوط افزوده
added = 0
for part in shortstat.split(","):
    p = part.strip()
    if p.endswith("insertions(+)") or p.endswith("insertion(+)"):
        try:
            added = int(p.split()[0])
        except:
            pass

if added > MAX_ADDED_LINES:
    print(f"FATAL: Too many added lines: {added} > {MAX_ADDED_LINES}")
    sys.exit(2)

# نیاز به لیبل برای تغییرات frontend/
if any(p.startswith("frontend/") for p in files) and FRONTEND_LABEL_REQUIRED not in labels:
    print("FATAL: Frontend changes detected without required label 'frontend-allowed'.")
    sys.exit(3)

# ممنوعیت فایل‌های خیلی بزرگ غیرمجاز
for p in files:
    fp = pathlib.Path(p)
    if fp.exists() and fp.is_file():
        if fp.stat().st_size > 100*1024*1024 and fp.suffix.lower() not in ALLOWED_LARGE_FILES:
            print(f"FATAL: Large file >100MB detected: {p}")
            sys.exit(4)

print("Guardrails passed.")

