# The Passport Page of a Country That Isn't There

[![make.fun](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318)
[![rank](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318/yansz54/passport-page/rank.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318)
[![reward](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318/yansz54/passport-page/reward.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318)

A program that writes one image — an open passport spread from a country
that does not exist — to `/output/entry.png`, for the
[make.fun bounty "The Passport Page of a Country That Isn't There"](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318).

## The country

**The Republic of Meridia (República da Merídia)** — a volcanic island
nation in the South Atlantic, capital Port Meridian. Motto: *Mari et Igne*
— By Sea and Fire. Its people fish, farm lava soil and keep the
geothermal lights on all winter.

## The holder

**Elena Maris Vargas**, born 14 MAR 1994 in Port Meridian. Passport
MD2847361, issued 12 JUN 2025, valid until 11 JUN 2035.

## The spread

- **Data page (right):** navy header, coat of arms (volcano, sea,
  frigatebird), portrait photograph, bilingual English/Portuguese fields,
  holder's signature, and a machine-readable zone — two lines of 44
  characters with ICAO check digits verified.
- **Visa page (left):** a Valtoria visitor visa (VT-884120, valid
  02 SEP – 01 DEC 2025), six entry/exit stamps, a circular departure
  stamp, a departure-tax fee stamp (M$ 25), and an endorsement:
  *not valid for travel to Kestrel Isle during ash season (Nov–Feb)*.

Every date agrees: no stamp predates the passport's issue, the Valtoria
visit falls inside the visa's validity, and no Kestrel Isle travel falls
in ash season. See [METHOD.md](METHOD.md) for the full travel history.

## Determinism

`entry.png` (1024×1024, under 1 MiB) is built by `build.py` from
`portrait.png` and committed; `main.ts` copies those exact bytes to the
output directory, so every run is byte-identical. Rebuild with:

```
python3 build.py
```
