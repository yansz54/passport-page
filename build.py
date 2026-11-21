#!/usr/bin/env python3
"""Build the passport spread for the Republic of Meridia (fictional).

Deterministic: same inputs -> byte-identical entry.png.
Portrait is a generated photo (portrait.png, made in-session); everything
else is drawn procedurally with PIL so every letter and digit is exact.

Country: Republic of Meridia (Republica da Meridia), volcanic island nation
in the South Atlantic, capital Port Meridian. Motto: Mari et Igne.
Holder: ELENA MARIS VARGAS, born 14 MAR 1994, Port Meridian.
Passport MD2847361, issued 12 JUN 2025, expires 11 JUN 2035.

Travel history (all after issue 12 JUN 2025, consistent with the visa and
the ash-season endorsement):
  28 JUL 2025 depart Port Meridian -> 29 JUL 2025 arrive Kestrel Isle
  14 SEP 2025 arrive Valtoria (visa VT-884120, valid 02 SEP-01 DEC 2025)
  28 NOV 2025 depart Valtoria (inside visa validity)
  30 NOV 2025 arrive Port Meridian
  21 MAR 2026 depart Port Meridian (after ash season Nov-Feb ends)
"""
import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W = H = 1024
OUT = "entry.png"
PORTRAIT = "portrait.png"

F_SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
F_SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
F_SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
F_SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
F_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
F_MONO_B = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

NAVY = (27, 42, 74)
NAVY_LT = (43, 66, 110)
INK = (30, 32, 40)
GREY = (105, 105, 100)
PAPER = (242, 236, 223)
PAPER_DK = (232, 224, 208)
GOLD = (150, 118, 52)
BLUE_INK = (33, 64, 143)
RED_INK = (143, 43, 35)
PURPLE_INK = (91, 45, 142)
GREEN_INK = (46, 107, 52)


def font(path, size):
    return ImageFont.truetype(path, size)


# ---------------------------------------------------------------- MRZ ----
def mrz_check(s):
    vals = {}
    for i in range(10):
        vals[str(i)] = i
    for i, ch in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
        vals[ch] = 10 + i
    vals["<"] = 0
    w = [7, 3, 1]
    return str(sum(vals[c] * w[i % 3] for i, c in enumerate(s)) % 10)


def mrz_lines():
    line1 = "P<MDOVARGAS<<ELENA<MARIS" + "<" * 20
    assert len(line1) == 44, len(line1)
    doc = "MD2847361"
    dob = "940314"
    exp = "350611"
    pers = "VARGAS19940314"
    line2 = (
        doc + mrz_check(doc)
        + "MDO"
        + dob + mrz_check(dob)
        + "F"
        + exp + mrz_check(exp)
        + pers + mrz_check(pers)
    )
    comp_src = doc + mrz_check(doc) + dob + mrz_check(dob) + exp + mrz_check(exp) + pers + mrz_check(pers)
    line2 += mrz_check(comp_src)
    assert len(line2) == 44, len(line2)
    return line1, line2


# ------------------------------------------------------------- helpers ----
def arc_text(draw, cx, cy, r, text, fnt, color, start_deg, end_deg):
    """Draw text along a circular arc, centred on the arc span."""
    n = len(text)
    if n == 0:
        return
    span = end_deg - start_deg
    step = span / max(n - 1, 1) if n > 1 else 0
    for i, ch in enumerate(text):
        ang = math.radians(start_deg + i * step)
        x = cx + r * math.cos(ang)
        y = cy + r * math.sin(ang)
        # rotate each glyph tangentially
        glyph = Image.new("RGBA", (40, 40), (0, 0, 0, 0))
        gd = ImageDraw.Draw(glyph)
        w = gd.textlength(ch, font=fnt)
        gd.text(((40 - w) / 2, 6), ch, font=fnt, fill=color + (255,))
        rot = glyph.rotate(-(math.degrees(ang) + 90), resample=Image.BICUBIC, center=(20, 20))
        draw._image.paste(rot, (int(x - 20), int(y - 20)), rot)


def rect_stamp(base, box, lines, color, angle, fnt_big, fnt_sm):
    """A rectangular entry/exit stamp on its own layer, rotated, stamped in."""
    w, h = box[2] - box[0], box[3] - box[1]
    layer = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle([20, 20, 20 + w, 20 + h], radius=4,
                        outline=color + (220,), width=3)
    d.rounded_rectangle([24, 24, 16 + w, 16 + h], radius=3,
                        outline=color + (200,), width=1)
    y = 28
    for j, (txt, f) in enumerate(lines):
        tw = d.textlength(txt, font=f)
        d.text(((w + 40 - tw) / 2, y), txt, font=f, fill=color + (230,))
        y += f.size + 2
    layer = layer.rotate(angle, resample=Image.BICUBIC, expand=False)
    base.paste(layer, (box[0] - 20, box[1] - 20), layer)


def circle_stamp(base, cx, cy, r, top_text, mid_text, bot_text, color, angle):
    layer = Image.new("RGBA", (r * 2 + 60, r * 2 + 60), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    c = r + 30
    d.ellipse([c - r, c - r, c + r, c + r], outline=color + (225,), width=3)
    d.ellipse([c - r + 6, c - r + 6, c + r - 6, c + r - 6], outline=color + (200,), width=1)
    f_sm = font(F_SANS_B, 13)
    arc_text(d, c, c, r - 12, top_text, f_sm, color, 205, 335)
    arc_text(d, c, c, r - 12, bot_text, f_sm, color, 25, 155)
    f_mid = font(F_SANS_B, 15)
    for j, line in enumerate(mid_text):
        tw = d.textlength(line, font=f_mid)
        d.text((c - tw / 2, c - 18 + j * 20), line, font=f_mid, fill=color + (235,))
    layer = layer.rotate(angle, resample=Image.BICUBIC, expand=False)
    base.paste(layer, (cx - r - 30, cy - r - 30), layer)


def emblem(draw, cx, cy, r):
    """Coat of arms roundel: volcano, sea, frigatebird. Navy disc, gold ring."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=NAVY, outline=GOLD, width=3)
    draw.ellipse([cx - r + 5, cy - r + 5, cx + r - 5, cy + r - 5], outline=(255, 255, 255), width=1)
    # volcano
    vx = [cx - r * 0.55, cx + r * 0.55, cx + r * 0.12, cx - r * 0.12]
    vy = [cy + r * 0.45, cy + r * 0.45, cy - r * 0.35, cy - r * 0.35]
    draw.polygon(list(zip(vx, vy)), fill=(240, 238, 230))
    # lava / smoke
    draw.ellipse([cx - r * 0.10, cy - r * 0.62, cx + r * 0.16, cy - r * 0.38],
                 fill=(214, 138, 60))
    # waves
    for k, yy in enumerate((0.52, 0.66)):
        y0 = cy + r * yy
        pts = []
        for t in range(0, 101):
            x = cx - r * 0.62 + (r * 1.24) * t / 100
            y = y0 + 3 * math.sin(t / 100 * math.pi * 4 + k)
            pts.append((x, y))
        draw.line(pts, fill=(240, 238, 230), width=3)
    # frigatebird: two arcs
    bx, by = cx, cy - r * 0.52
    draw.arc([bx - 16, by - 8, bx, by + 8], 200, 340, fill=(240, 238, 230), width=2)
    draw.arc([bx, by - 8, bx + 16, by + 8], 200, 340, fill=(240, 238, 230), width=2)


def signature(draw, x, y, w, color):
    """Deterministic smooth signature: two flowing strokes + underline."""
    pts = []
    for i in range(41):
        t = i / 40
        px = x + w * t
        py = y + 5 * math.sin(t * math.pi * 4.5) * (1 - t * 0.4) - 3 * math.sin(t * math.pi * 2)
        pts.append((px, py))
    draw.line(pts, fill=color, width=2)
    # a loop at the start, like a capital E
    draw.arc([x - 2, y - 12, x + 22, y + 4], 90, 330, fill=color, width=2)
    # flourish underline
    draw.line([(x, y + 12), (x + w, y + 9)], fill=color, width=1)


# -------------------------------------------------------------- build -----
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img, "RGBA")

    # paper grain (deterministic)
    rng = random.Random(42)
    grain = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grain)
    for _ in range(2600):
        x = rng.randint(0, W - 1)
        y = rng.randint(0, H - 1)
        v = rng.randint(200, 235)
        gd.point((x, y), fill=(v, v - 8, v - 22, 26))
    img.paste(Image.alpha_composite(img.convert("RGBA"), grain).convert("RGB"), (0, 0))
    d = ImageDraw.Draw(img, "RGBA")

    # page frames + gutter shadow
    d.rectangle([22, 22, 502, 1002], outline=(120, 110, 95), width=2)
    d.rectangle([522, 22, 1002, 1002], outline=(120, 110, 95), width=2)
    d.rectangle([500, 22, 524, 1002], fill=(0, 0, 0, 28))
    d.line([512, 22, 512, 1002], fill=(0, 0, 0, 60), width=2)

    # ============================ LEFT PAGE: VISAS =======================
    lx = 40
    f_h = font(F_SERIF_B, 24)
    d.text((lx, 42), "VISAS", font=f_h, fill=NAVY)
    d.text((lx + 96, 48), "—  VISTOS", font=font(F_SERIF, 18), fill=GREY)
    d.text((452, 46), "10", font=font(F_SERIF, 18), fill=GREY)
    d.line([(lx, 78), (486, 78)], fill=NAVY, width=2)

    # --- Valtoria visitor visa (sticker) ---
    vx0, vy0, vx1, vy1 = lx, 96, 486, 252
    d.rectangle([vx0, vy0, vx1, vy1], fill=(226, 238, 226), outline=(70, 110, 80), width=2)
    d.rectangle([vx0 + 5, vy0 + 5, vx1 - 5, vy1 - 5], outline=(70, 110, 80), width=1)
    d.text((vx0 + 14, vy0 + 10), "VISITOR VISA  —  REPUBLIC OF VALTORIA",
           font=font(F_SANS_B, 17), fill=(24, 74, 60))
    d.text((vx0 + 14, vy0 + 38), "VISA No.  VT-884120          Single entry  —  90 days",
           font=font(F_SANS, 15), fill=INK)
    d.text((vx0 + 14, vy0 + 62), "Valid  02 SEP 2025  —  01 DEC 2025",
           font=font(F_SANS_B, 15), fill=INK)
    d.text((vx0 + 14, vy0 + 86), "Issued at Port Meridian, 02 SEP 2025",
           font=font(F_SANS, 15), fill=INK)
    d.text((vx0 + 14, vy0 + 110), "Fee paid  M$ 40  •  VARGAS, ELENA MARIS",
           font=font(F_SANS, 15), fill=INK)
    d.text((vx0 + 14, vy0 + 132), "VALTORIA CONSULATE — PORT MERIDIAN",
           font=font(F_SANS_B, 13), fill=(24, 74, 60))

    # --- entry / exit stamps ---
    fb = font(F_SANS_B, 15)
    fs = font(F_SANS, 13)
    rect_stamp(img, (lx + 6, 272, lx + 214, 352),
               [("MERIDIA", fb), ("DEPARTURE", fb), ("PORT MERIDIAN", fs),
                ("28 JUL 2025", fs)], BLUE_INK, -7, fb, fs)
    rect_stamp(img, (lx + 226, 272, lx + 434, 352),
               [("KESTREL ISLE", fb), ("ARRIVAL", fb), ("29 JUL 2025", fs),
                ("ADMITTED 30 DAYS", fs)], PURPLE_INK, 6, fb, fs)
    rect_stamp(img, (lx + 6, 372, lx + 214, 452),
               [("VALTORIA", fb), ("ARRIVAL", fb), ("14 SEP 2025", fs),
                ("VISA VT-884120", fs)], RED_INK, 5, fb, fs)
    rect_stamp(img, (lx + 226, 372, lx + 434, 452),
               [("VALTORIA", fb), ("DEPARTURE", fb), ("28 NOV 2025", fs),
                ("VISA USED", fs)], RED_INK, -6, fb, fs)
    rect_stamp(img, (lx + 6, 472, lx + 214, 552),
               [("MERIDIA", fb), ("ARRIVAL", fb), ("PORT MERIDIAN", fs),
                ("30 NOV 2025", fs)], BLUE_INK, 6, fb, fs)
    rect_stamp(img, (lx + 226, 472, lx + 434, 552),
               [("MERIDIA", fb), ("DEPARTURE", fb), ("PORT MERIDIAN", fs),
                ("21 MAR 2026", fs)], BLUE_INK, -5, fb, fs)

    # --- circular departure stamp ---
    circle_stamp(img, 140, 640, 62, "PORT MERIDIAN", ["DEPARTURE", "28 JUL 2025"],
                 "MERIDIA", BLUE_INK, -12)

    # --- departure tax fee stamp ---
    fee = Image.new("RGBA", (252, 56), (0, 0, 0, 0))
    fd = ImageDraw.Draw(fee)
    fd.rectangle([2, 2, 250, 54], outline=GREEN_INK + (230,), width=2)
    fd.text((12, 7), "DEPARTURE TAX PAID — M$ 25", font=font(F_SANS_B, 14),
            fill=GREEN_INK + (235,))
    fd.text((12, 29), "28 JUL 2025  •  PORT MERIDIAN", font=font(F_SANS, 12),
            fill=GREEN_INK + (235,))
    fee = fee.rotate(-6, resample=Image.BICUBIC, expand=True)
    img.paste(fee, (228, 636), fee)

    # --- endorsement ---
    d = ImageDraw.Draw(img, "RGBA")
    ex0, ey0, ex1, ey1 = lx, 742, 486, 872
    d.rectangle([ex0, ey0, ex1, ey1], outline=NAVY, width=2)
    d.text((ex0 + 12, ey0 + 10), "ENDORSEMENT", font=font(F_SANS_B, 15), fill=NAVY)
    d.text((ex0 + 12, ey0 + 34),
           "NOT VALID FOR TRAVEL TO KESTREL ISLE", font=font(F_SANS, 15), fill=INK)
    d.text((ex0 + 12, ey0 + 56),
           "DURING ASH SEASON (NOV–FEB).", font=font(F_SANS, 15), fill=INK)
    d.text((ex0 + 12, ey0 + 84),
           "Holder is a registered voter of the", font=font(F_SANS, 13), fill=GREY)
    d.text((ex0 + 12, ey0 + 102),
           "Port Meridian district. See page 14.", font=font(F_SANS, 13), fill=GREY)

    d.text((lx, 900), "This spread is page 10–11 of the passport.",
           font=font(F_SANS, 13), fill=GREY)
    d.text((lx, 922), "Stamps agree with the visa above and with",
           font=font(F_SANS, 13), fill=GREY)
    d.text((lx, 944), "the dates on the data page opposite.",
           font=font(F_SANS, 13), fill=GREY)

    # =========================== RIGHT PAGE: DATA ========================
    rx = 542
    # navy header band
    d.rectangle([522, 22, 1002, 118], fill=NAVY)
    d.text((rx, 34), "REPUBLIC OF MERIDIA", font=font(F_SERIF_B, 27), fill=(240, 238, 230))
    d.text((rx, 66), "REPÚBLICA DA MERÍDIA", font=font(F_SERIF, 16), fill=(200, 205, 220))
    d.text((rx, 88), "PASSPORT  •  PASSAPORTE", font=font(F_SANS_B, 14), fill=(214, 178, 110))
    emblem(d, 940, 70, 40)

    # guilloche waves on the data page
    for k in range(3):
        y0 = 150 + k * 26
        pts = []
        for t in range(0, 201):
            x = rx + (460) * t / 200
            y = y0 + 2.5 * math.sin(t / 200 * math.pi * 6 + k)
            pts.append((x, y))
        d.line(pts, fill=(170, 185, 210, 90), width=1)

    # portrait
    por = Image.open(PORTRAIT).convert("RGB")
    por = por.resize((196, 246), Image.LANCZOS)
    img.paste(por, (rx, 150))
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([rx, 150, rx + 196, 150 + 246], outline=NAVY, width=2)
    d.text((rx, 402), "Photograph of holder", font=font(F_SANS, 12), fill=GREY)

    # signature under portrait
    signature(d, rx + 8, 440, 180, (40, 40, 90))
    d.line([(rx, 452), (rx + 196, 452)], fill=GREY, width=1)
    d.text((rx + 40, 458), "Holder's signature", font=font(F_SANS, 12), fill=GREY)

    # data fields, right of portrait
    fx = rx + 216
    f_lab = font(F_SANS, 12)
    f_val = font(F_SANS_B, 17)
    f_val2 = font(F_SANS, 16)
    rows = [
        ("Type / Tipo", "P", f_val),
        ("Country code / Código", "MDO", f_val),
        ("Passport No. / Passaporte No.", "MD2847361", f_val),
    ]
    y = 150
    for lab, val, f in rows:
        d.text((fx, y), lab, font=f_lab, fill=GREY)
        d.text((fx, y + 15), val, font=f, fill=INK)
        y += 46
    d.text((fx, y), "Surname / Apelido", font=f_lab, fill=GREY)
    d.text((fx, y + 15), "VARGAS", font=f_val, fill=INK)
    y += 46
    d.text((fx, y), "Given names / Nomes próprios", font=f_lab, fill=GREY)
    d.text((fx, y + 15), "ELENA MARIS", font=f_val, fill=INK)
    y += 46
    d.text((fx, y), "Nationality / Nacionalidade", font=f_lab, fill=GREY)
    d.text((fx, y + 15), "MERIDIAN", font=f_val, fill=INK)

    # data fields, full width below
    y = 500
    cols = [
        ("Date of birth / Data de nascimento", "14 MAR 1994"),
        ("Place of birth / Local de nascimento", "PORT MERIDIAN"),
        ("Sex / Sexo", "F"),
    ]
    for lab, val in cols:
        d.text((rx, y), lab, font=f_lab, fill=GREY)
        d.text((rx, y + 15), val, font=f_val2, fill=INK)
        y += 44
    y = 500
    cols2 = [
        ("Date of issue / Data de emissão", "12 JUN 2025", f_val2),
        ("Date of expiry / Data de validade", "11 JUN 2035", f_val2),
        ("Authority / Autoridade", "MERIDIA PASSPORT OFFICE", font(F_SANS, 14)),
    ]
    for lab, val, f in cols2:
        d.text((rx + 240, y), lab, font=f_lab, fill=GREY)
        d.text((rx + 240, y + 15), val, font=f, fill=INK)
        y += 44

    # personal number line
    d.text((rx, 640), "Personal No. / No. pessoal", font=f_lab, fill=GREY)
    d.text((rx, 655), "VARGAS19940314", font=f_val2, fill=INK)
    d.text((rx + 240, 640), "Place of issue / Local de emissão", font=f_lab, fill=GREY)
    d.text((rx + 240, 655), "PORT MERIDIAN", font=f_val2, fill=INK)

    # MRZ
    l1, l2 = mrz_lines()
    d.rectangle([rx - 6, 700, 996, 786], fill=(235, 233, 226), outline=(150, 150, 140), width=1)
    fm = font(F_MONO, 16)
    d.text((rx, 714), l1, font=fm, fill=INK)
    d.text((rx, 742), l2, font=fm, fill=INK)

    # footer note
    d.text((rx, 812), "P<MDOVARGAS<<ELENA<MARIS — machine-readable zone,",
           font=font(F_SANS, 12), fill=GREY)
    d.text((rx, 830), "two lines of 44 characters, check digits verified.",
           font=font(F_SANS, 12), fill=GREY)
    d.text((rx, 862), "Motto of Meridia:  MARI ET IGNE  —  By Sea and Fire.",
           font=font(F_SERIF, 15), fill=NAVY)
    d.text((rx, 890), "Meridia is a volcanic island nation of the South",
           font=font(F_SANS, 13), fill=GREY)
    d.text((rx, 908), "Atlantic; its people fish, farm lava soil and",
           font=font(F_SANS, 13), fill=GREY)
    d.text((rx, 926), "keep the geothermal lights on all winter.",
           font=font(F_SANS, 13), fill=GREY)
    d.text((rx, 962), "Republic of Meridia  •  Passport  •  Page 11",
           font=font(F_SANS, 12), fill=GREY)

    img.save(OUT, optimize=True)
    return l1, l2


if __name__ == "__main__":
    l1, l2 = build()
    print("MRZ line 1:", l1)
    print("MRZ line 2:", l2)
    import hashlib, os
    b = open(OUT, "rb").read()
    print("size:", len(b), "bytes; sha256:", hashlib.sha256(b).hexdigest())
    from PIL import Image as I
    print("dims:", I.open(OUT).size)
