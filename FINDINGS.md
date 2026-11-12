# GSMG.IO 5 BTC Puzzle — Cryptanalysis of the SalPhaseIon / Cosmic Duality endgame

This document records a rigorous, falsification-driven analysis of the **unsolved final
phase** of the GSMG.IO puzzle (SalPhaseIon → Cosmic Duality). Every hypothesis below was
tested empirically; negative results are reported honestly because they *narrow* the
problem. Tools live in [`_work/`](./_work) and are reusable.

> TL;DR: The endgame reduces to decoding two strings, **`dbbi`** (91 symbols) and
> **`faed`** (570 symbols), both over the 9-symbol alphabet `a–i`. We establish that
> `dbbi` is a **structured, decodable key** and `faed` is a **high-entropy encrypted
> payload**; that the cipher family is a **VIC / straddling-checkerboard** (validated by
> reproducing the already-solved phase 3.2.2); that the two escape digits are almost
> certainly **1,4**; and — crucially — that the puzzle is blocked by a **verification
> problem** that makes blind search/cryptanalysis provably unable to converge. The
> missing piece is a single *interpretive* leap, not more compute.

> **Update 2026-11-12:** see [Session 2](#session-2-2026-11-12--further-falsification) at the
> end: live-page verification, a validated AES oracle, and seven more negative results
> (clue corpus, prime zeroing, repeated keys, substring search, checkerboard +
> transposition).

## The two unsolved strings

```
dbbi (91 = 7×13): dbbibfbhccbegbihabebeihbeggegebebbgehhebhhfbabfdhbeffcdbbfcccgbfbeeggecbedcibfbffgigbeeeabe
faed (570 = 15×38): faedggeedfcbdabhhggcadcfeddgfdgbgig...iihic   (see _work/, full string in scripts)
```

Both decoded from the SalPhaseIon page text. The page also contains:
- `matrixsumlist` / `enter` (the two "abba" binary blobs) — **paired with `dbbi`**
- `lastwordsbeforearchichoice` / `thispassword` (two "z"-segments) — **paired with `faed`**
- `shabef our first hint is your last command` and `shabef ans too` (`shabef` = **sha256**)
- An 80-byte AES blob (`_work/salphaseion_blob.txt`)
- The **Cosmic Duality** AES blob (1328 B, `ChatExport/files/cd.b64.txt`)

## Hard structural facts (the foundation)

| Fact | Evidence |
|---|---|
| **`dbbi` is a structured/decodable key** | Index of Coincidence = **0.151** (uniform-9 = 0.111). 'b'=27%, 'e'=20% dominate. |
| **`faed` is an encrypted payload** | IoC = **0.118 ≈ uniform**, flat across all periods; ~no repeated n-grams = max entropy. |
| **Cipher = VIC / straddling checkerboard** | Phase 3.2.2 used exactly this (`dcode.fr/vic-cipher`). Decoder validated in `_work/cb2.py` reproduces `INCASEYOUMANAGE...` perfectly. Top community solver "RB": straddling checkerboard is the "hottest candidate since 2021"; `matrixsumlist` = the **mod-9 over-encryption** step. |
| **Escape digits ≈ 1,4** | In a checkerboard, escape digits are the most frequent. `dbbi`'s two most frequent symbols are `b,e`; with mapping `a=0..i=8`, `b=1, e=4` = **identical to the 3.2.2 escapes**. |
| **Key-length ↔ grid match** | `len("matrixsumlist")=13` ↔ `dbbi=13×7`; `len("lastwordsbeforearchichoice"+"thispassword")=38` ↔ `faed=15×38`. The decoded words are transposition-key-length. |
| **Endgame pipeline** | `sha256(first hint)` → decode key for `dbbi/faed` → **ANSWER** → `sha256(ANSWER)` = AES key → Cosmic Duality. (RB's reading of `shabef ... ans too`.) |

## The byte-boundary colour layer (verified, but redundant)

The first image (`puzzle.png`) is a 14×14 binary matrix read CCW-spiral → `gsmg.io/theseedisplanted`.
It has **15 blue + 9 yellow** special squares. Verified finding: in spiral order **all 24
special squares sit at exact multiples of 8** — i.e. the last bit of each of the 24 URL
characters. Intentional (impossible by chance). **However** blue=1/yellow=0 simply equals
the parity of each character → it *confirms* the byte structure but encodes **no new key**.
"Roses are White but often Red, Yellow has a number and so does Blue" mirrors Lewis Carroll's
*Game of Logic* counters (RED=1 occupied, GREY=0 empty), confirming the binary-counter theme.

## The verification problem (why the puzzle resists, provably)

Two independent reasons make one-candidate-at-a-time search unable to converge:

1. **Each guessed key fixes only ONE of ≥4 unknowns.** A full VIC decode of `dbbi` needs:
   checkerboard *alphabet* **+** `a–i→digit` *mapping* **+** *transposition* key **+**
   *over-encryption* keystream. Testing a phrase as "the alphabet" leaves three unknowns,
   so even the *correct* alphabet yields gibberish.
2. **No verification signal until the very end.** `dbbi` → ~60 letters. Hill-climbing
   (`_work/hillclimb.py`) reaches English-level trigram fitness from **any** starting
   alphabet (overfit on 60 chars). So even a fully-correct decode can't be recognised from
   `dbbi` alone. The only true verifier is the closed loop `decode → sha256(answer) →
   opens the AES blob` — which requires all 4 parameters correct *simultaneously*.

⇒ The block is **interpretive/structural, not computational**. Matches the creator's
"good puzzles don't need hints" / "it's in front of your eyes but you're not seeing it".

## Hypotheses tested and FALSIFIED (with evidence)

- **"matrixsumlist triangle"** (dbbi fills upper-triangle of 14×14, row-sums XOR faed):
  produced fragments `SENDTHE`/`BLUENET` — but a **null-model test** (38k random strings)
  shows max score identical → **apophenia**, not signal. Disproven.
- **Image hidden layers / steganography**: no trailing data after IEND, no text chunks in
  any PNG; only `puzzle.png` + `theseedisplanted.png` use special colours; no alternative
  matrix reading (rotations/flips/clockwise all gibberish; 4 leftover spiral bits = `0000`).
- **Book cipher**: searched OCR of both reference books for 27 solved-phase answers —
  Cosmic Duality **0/27**, Game of Logic **1/27**. `causality`, `heisenberg`, `Safenet`,
  `Luna`, `Merovingian`, `architect`, etc. **absent from both** ⇒ books are *thematic name*
  only, **not** a key source.
- **"first hint" candidates** (all → checkerboard alphabet + AES key + keystream, 0 hits):
  blue/yellow layer; the chronological first hash `5ac40783…` = sha256(phase-2 flower
  password); the white rabbit (drawing sits on white/0 centre cells); the phase-3 chess
  position; the Decentraland spectrogram (→ `HASHTHETEXT`); "The Warning" by Logic lyrics;
  yellow-blue-prime; the Roses poem. **None crack it** (and per the verification problem,
  the correct one wouldn't be recognisable anyway).

## Tools (`_work/`)

- `cb2.py` — **validated** straddling-checkerboard decoder (reproduces phase 3.2.2).
- `hillclimb.py` — trigram hill-climber for the checkerboard alphabet (demonstrates overfit).
- `parse_chat.py` — Telegram HTML export → plain transcript.
- `vic_full.py`, `cb9.py`, `blueyellow_attack.py`, `columnar.py`, `triangle_zero.py`,
  `matrixtri.py`, `dbbi_*.py`, `faed_base9.py`, `prime_theory.py` — individual attack scripts.
- `decrypt*.py` — OpenSSL-compatible AES-256-CBC (sha256 KDF) for the blobs.
- Data: `salphaseion_blob.txt`, `salph_raw.txt`, `creator_jrk.txt` (all creator messages),
  `gameoflogic_ocr.txt` (public-domain OCR), analysis outputs `*_out.txt`.

## The joint 4-parameter attack (`_work/joint_attack.py`)

The structurally-correct computational attack: instead of trusting the (unreliable)
English score, enumerate {alphabet × `a–i` mapping × escapes × transposition ×
over-encryption} jointly and verify **only** via the real oracle —
`decode(dbbi) → sha256(answer) → does it open the SalPhaseIon or Cosmic blob`.

- Bounded candidate space: ~16 keyword/seed alphabets (incl. the 3.2.2 alphabet),
  2 mappings, 3 escape pairs, 3 transpositions, 3 over-encryption keystreams, 6 answer
  normalisations, both `sha256(answer)` and raw-answer as the openssl pass.
- **4904 decode-forms AES-tested → 0 hits.**

What this proves: the attack is feasible and correct, but it can only win if the
checkerboard **alphabet** is one of the natural keyword candidates — it isn't. The
alphabet is a 26! space and the AES oracle is **binary with no gradient**, so it cannot
be searched efficiently. ⇒ Without the correct *interpretation* that fixes the alphabet
(the "first hint"), the endgame is **computationally unbreakable from our position**.
This is the formal endpoint of the campaign.

## What would actually move this

1. A **new official hint** from the creator (he stated he'd release one more if unsolved).
2. A **joint 4-parameter attack** that solves alphabet + mapping + transposition +
   over-encryption *together*, verifying only via the end-of-chain AES loop (expensive,
   low-probability, but the only computational path that respects the real structure).
3. The single correct **interpretation of "the first hint"** that closes the loop at once.

---

## Session 2 (2026-11-12) — further falsification

Same method as above: every hypothesis tested against a validated oracle, negatives
reported. Scripts are in [`_work/session2/`](./_work/session2) (they use absolute Windows
paths and, for `ckb.py`, a corpus of Project Gutenberg books in `corpus/pg*.txt`).

### 1. The live page, verified

`https://gsmg.io/89727c59…` was re-downloaded (HTTP 200, `Last-Modified` 2026-08-15). Its two
textareas are **byte-identical** to the 2021 data used in this repo (895 chars + the 1328 B
Cosmic Duality blob); only the file timestamp changed. The HTML has no comments, scripts,
images or hidden text. Real order of the content:

| # | Content | Meaning |
|---|---|---|
| 1 | `dbbi…` (91) | undecoded |
| 2 | a/b blob (104 bits) | `matrixsumlist` |
| 3 | `faed…` (570) | undecoded |
| 4 | `z` + segment | `lastwordsbeforearchichoice` |
| 5 | `z` + segment | `thispassword` |
| 6 | `z` + `shabef` + `ourfirsthintisyourlastcommand` | "sha256 our first hint is your last command" |
| 7 | AES blob #1 (80 B ct), split in two 64-char halves with an a/b blob between them | that blob = `enter` |
| 8 | `shabef` + `anstoo` | "sha256 ans too" |
| 9 | Cosmic Duality textarea (`Salted__`, 1328 B ct) | final blob |

- **`enter` is the line break.** Each half of blob #1 is exactly 64 chars (openssl `-a` line
  width); `enter` sits where the newline would be. It is not an independent clue.
- Reading order suggests `blob #1 = AES(sha256(first hint))`, then
  `Cosmic Duality = AES(sha256(ans))` with `ans` the output of blob #1 (same pipeline as above).
- `faed` begins at raw offset 195 (91 + 104), right after the a/b blob.
- `π(570) = 104` = bit length of the `matrixsumlist` blob. Probably chance; it produced nothing.

### 2. Oracle validation

`evp(sha256)` + AES-256-CBC + PKCS#7 reimplemented and checked against **solved** blobs from
upstream: Phase 3 (key `sha256hex(causality…FEN)`) and Phase 3.2 (key `sha256hex(jacquefresco…)`)
both decrypt to the expected plaintext. A "0 hits" below therefore means a real miss.

### 3. Corrections to earlier assumptions

- The 2026-01-01 message decodes to *"…here's a "tiny hint" <3."* (a first transcription
  without "tiny" was wrong; redone with the right text).
- `faed_base9.py` treated `faed` as base 9 (`a=0..i=8`). The SalPhaseIon notebook decodes the
  `z`-segments as **decimal** digits (`abcdefghio -> 1234567890`) → int → hex → ASCII. That
  reading of `faed`/`dbbi` was untested here until now (see 5.).

### 4. Clue corpus as key — 0 hits

Official hints and admin quotes 2020–2026 (transcribed from the upstream `hints/` images),
~150 phrases incl. the three 2026 hints, with variants (raw/lower/upper/stripped, pairs).

| Run | Base strings | Tests |
|---|---|---|
| 2026 hints + EO11110 / fefefe / 5binary themes | 917 | 14,672 |
| All hints 2020–2026 | 32,132 | 642,640 |

Forms: raw, sha256 hex (lower/upper), double sha256, md5; KDF sha256 and md5; both blobs.

### 5. Structural attacks on `dbbi` / `faed` — all negative

- **Prime "zeroing"** ("some characters need to be zeroed out", "prime part", 2021): zero /
  delete / keep-only at prime positions (0- and 1-indexed, complement, squares) and at digit
  *values* in every subset of {2,3,5,7}; `a1`/`a0` maps; decimal→hex→bytes and 2/3-digit ASCII;
  on `dbbi`, `faed`, both concatenations, and the raw page; forward and reversed. ~1,080
  variants, each also fed to the AES oracle. Pipeline sanity-checked: it recovers
  `lastwordsbeforearchichoice` from the known segment. No structure, no hits.
- **Row/column sums** of `dbbi` as 7×13 and 13×7 (the `matrixsumlist` idea), `a0`/`a1`, mod
  9/10/26/27: nothing readable.
- **Pairs/triples**: `faed` is indistinguishable from a shuffle of its own letters at unit
  sizes 2, 3, 4 (z between −0.7 and +1.0 against 300 shuffles). No simple substitution over
  digraphs/trigraphs. (`dbbi` k=4 offset 3 gave z=3.1 once in 12 tests; not significant.)
- **Repeated `dbbi` as key** over `faed` (±, mod 9/10, both digit offsets, forward/reversed,
  all 91 shifts; 1,456 variants): best IoC 0.1143, inside the random-key null (p99 0.1136,
  max 0.1148).
- **All substrings of the Phase 3.2 plaintext** (the creator's modified Architect speech) as
  key, raw and sha256 hex, lengths 3..1539: **2,361,664** tests, 0 hits.
- **Ordered combinations of the page's own words** (`matrixsumlist`, `lastwordsbefore…`,
  `thispassword`, `sha256`/`shabef`, `ourfirsthint…`, `enter`, `anstoo`/`ans`/`answer`; 1–7
  pieces; plus `yinyang`, `yellowblueprimes`, `primes` up to 4 pieces), with separators, case,
  raw / sha256 / double sha256 / hash chains: **4,721,184** tests, 0 hits.

### 6. `dbbi` as a straddling checkerboard — calibrated, negative

Previous hill-climbing was inconclusive (trigram model from the README only; 6 restarts).
Redone properly:

- Model: with 9 symbols and 2 escapes the board has 7+9+9 = 25 cells = a 25-letter alphabet
  (I=J). Given the escape pair, decoding is deterministic, leaving a monoalphabetic
  substitution over ~25 token types. All 36 escape pairs tried, no assumption on the
  `a–i → digit` order (absorbed by the alphabet).
- English model: quadgrams from 2.6 M letters of 5 Gutenberg books. Solver: simulated
  annealing with restarts, **calibrated** on known 60-token messages (it recovers them at
  fit ≈ −4.1…−4.2, readable text).

| | fit (mean log10 quadgram) |
|---|---|
| real English, 60 tokens | −4.1 … −4.2 |
| `dbbi`, best of 36 escape pairs | −4.57 |
| shuffled `dbbi`, best of 36 pairs (3 controls) | −4.43 … −4.54 |
| `dbbi` + 33 grid readings (7×13 / 13×7 rows, cols, snake, spiral, diagonals, each reversed) × 36 pairs | best −4.34, unreadable |

Result: `dbbi` is **not** a plain 9-symbol straddling checkerboard of English, with or without a
simple grid transposition. Not covered: keyed columnar transposition (7! / 13! orders),
mod-9/10 over-encryption with a keystream, 3-escape boards, non-English plaintext.

### 7. What the page and hints add (no new key, but useful context)

- Admin messages not listed above: *"Breaking salphation should be giving the feeling of the
  phase's name"* (2021-05); *"You are at the prime part already"* (2021-03); *"some characters
  need to be 'zeroed out'"* + primes required (2021-12); *"Once you hit a 'ying yang', you'll
  be able to solve it the same day"* (2024-04); *"Partly."* to a question about the
  "salvation part" (2024-04); 2026-07-12: *"My close friends have the best chance of solving
  it… they don't have the skills some of you do. NOTE: that is a hint"* and *"The 5 btc was
  never the actual prize."* — all consistent with an **interpretive** last step.
- The Phase 3.2 plaintext itself says the end involves *"twenty three ciphers, sixteen
  encryptions and/or seven intertwined passwords"*, *"return to the source code"* and
  *"reinserting the prime basics"*; the 2023-02-23 hint gives the step order
  yellow/blue → primes → matrix sumlist → last words before archichoice → yin yang.
- Upstream (Naddiseo, 2026) fixed the truncated Phase 3 password (it ends with the full FEN
  `…/3N1N2 b - - 0 1`) and added `unverified/`. Make sure any script that hashes it uses
  the complete string. This fork has **not** been synced with upstream.
- Upstream README now warns that a decryption without verifiable output structure is
  indistinguishable from failure, and quotes the creator saying the remaining steps are
  easier than those already solved. This argues against any path that needs all four
  parameters of the joint attack at once.

### Updated "what would move this"

1. A new official hint (none since 2026-07-12).
2. The correct interpretation of "our first hint is your last command" (all literal readings
   above are exhausted).
3. A cheap scoring function for **keyed** transposition / over-encryption of `dbbi`, which is
   the only family of the structural model left open.
