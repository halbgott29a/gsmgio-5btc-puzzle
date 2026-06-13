#!/usr/bin/env python3
"""Parse Telegram HTML export into a single plain-text transcript."""
import re, html, glob, os, sys

CHATDIR = r"D:\tmp\gsmgio-5btc-puzzle\ChatExport"
OUT = r"D:\tmp\gsmgio-5btc-puzzle\_work\chat_transcript.txt"

files = sorted(glob.glob(os.path.join(CHATDIR, "messages*.html")),
               key=lambda p: int(re.search(r"messages(\d*)", p).group(1) or "0"))

msg_re = re.compile(r'<div class="message (default|service)[^"]*"[^>]*>(.*?)(?=<div class="message |</div>\s*</div>\s*</body>|$)', re.S)
from_re = re.compile(r'<div class="from_name">\s*(.*?)\s*</div>', re.S)
date_re = re.compile(r'<div class="(?:pull_right )?date[^"]*"[^>]*title="([^"]*)"')
text_re = re.compile(r'<div class="text">\s*(.*?)\s*</div>', re.S)

def clean(t):
    t = re.sub(r'<br\s*/?>', '\n', t)
    t = re.sub(r'<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>',
               lambda m: m.group(2) if m.group(2).strip()==m.group(1).strip() else f"{m.group(2)} [{m.group(1)}]", t, flags=re.S)
    t = re.sub(r'<[^>]+>', '', t)
    return html.unescape(t).strip()

last_sender = "?"
total = 0
with open(OUT, "w", encoding="utf-8") as out:
    for f in files:
        raw = open(f, encoding="utf-8").read()
        # split per message div
        blocks = re.split(r'(?=<div class="message )', raw)
        for b in blocks:
            if not b.startswith('<div class="message'):
                continue
            fn = from_re.search(b)
            sender = clean(fn.group(1)) if fn else last_sender
            last_sender = sender
            dm = date_re.search(b)
            date = dm.group(1) if dm else ""
            tm = text_re.search(b)
            if not tm:
                continue
            text = clean(tm.group(1))
            if not text:
                continue
            total += 1
            out.write(f"=== [{date}] {sender}\n{text}\n\n")
print(f"parsed {total} messages -> {OUT}")
