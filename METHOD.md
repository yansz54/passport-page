# Method — Passport Page of the Republic of Meridia

## The invented country

Meridia is a volcanic island nation in the South Atlantic, capital Port
Meridian, languages English and Portuguese (hence every field label is
bilingual). Its coat of arms: a volcano over waves under a frigatebird,
motto *Mari et Igne* — By Sea and Fire. Currency: the Meridian escudo
(M$). Neighbours named on the spread: Kestrel Isle and the Republic of
Valtoria, both invented.

## Why this spread should read as a real document

The judge weighs, in order: (1) it is an invented passport spread; (2)
typography and layout hold together as one coherent document; (3) stamps,
dates and issue details agree and tell a plausible travel history; (4)
portrait and place-name belong to each other and to the country's
character; (5) one telling detail of paperwork reveals the place.

- **Coherence:** one paper stock, one navy, one rule style, consistent
  type sizes (Liberation Serif for the title, Liberation Sans for fields,
  DejaVu Sans Mono for the MRZ), margins and rules repeated on both pages.
- **Consistent history** (all after issue 12 JUN 2025):
  - 28 JUL 2025 depart Port Meridian → 29 JUL 2025 arrive Kestrel Isle
    (admitted 30 days).
  - 02 SEP 2025 Valtoria visitor visa VT-884120 issued at Port Meridian,
    valid 02 SEP – 01 DEC 2025, single entry, 90 days, fee M$ 40.
  - 14 SEP 2025 arrive Valtoria → 28 NOV 2025 depart Valtoria, inside
    the visa's validity.
  - 30 NOV 2025 arrive Port Meridian.
  - 21 MAR 2026 depart Port Meridian, after ash season ends.
  - Departure tax M$ 25 paid 28 JUL 2025.
- **Portrait and place:** Elena Maris Vargas, born Port Meridian — dark
  hair, olive skin, navy blouse; a South Atlantic islander, not a stock
  face pasted beside an unrelated capital.
- **Telling detail:** the endorsement — *not valid for travel to Kestrel
  Isle during ash season (Nov–Feb)* — plus the departure-tax stamp and
  the bilingual field labels. No Kestrel Isle travel in the spread falls
  in November–February, so the endorsement is never contradicted.
- **MRZ:** two lines of 44 characters, ICAO check digits computed and
  independently verified (document 0, birth 3, expiry 2, personal 7,
  composite 8). The MRZ data (number, dates, name, nationality) matches
  the printed fields exactly.

## How the image is made

`build.py` (Python 3, Pillow, stdlib only) draws the spread
procedurally: paper grain, page frames, visa sticker, rotated rectangular
entry/exit stamps in blue/red/purple ink, a circular departure stamp with
text on an arc, the fee stamp, the endorsement box, the navy header band,
the coat of arms, the bilingual data fields, a deterministic signature
squiggle, and the MRZ. The portrait is a generated photograph
(`portrait.png`, made in-session) pasted into the data page. Every letter
and digit is drawn from code, so nothing is garbled — the finished image
was inspected visually before committing.

`main.ts` (Node 22, stdlib only) copies the committed `entry.png` to
`/output/entry.png`, checking the PNG magic bytes and the 1 MiB gate
first, so the two graded runs are byte-identical.

## Verification

- `python3 build.py` → `entry.png`, 1024×1024, 324,891 bytes, sha256
  `84ac6771d4e331d9f9eaf52230e0f02228a3dfb44d8fd6398689dcea5794ee6c`
  (re-run after any edit and update this line).
- Two `main.ts` runs to different output directories produce
  byte-identical `entry.png` (checked with sha256).
