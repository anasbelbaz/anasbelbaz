#!/usr/bin/env python3
"""Generate an animated 'binary garden' SVG: a garden scene drawn entirely from
0/1 glyphs, colored by region so the lake, koi, trees and grass read clearly."""

W, H = 92, 29          # grid: columns, rows
CW, CH = 9, 17         # cell advance in px (monospace)
PAD = 14
FS = 15

BG = "#0a0e1a"

# region -> color
COL = {
    "sky":    "#20406e",
    "sun":    "#ffd84a",
    "sunglow":"#c9a12e",
    "cloud":  "#c2d2e2",
    "hill":   "#1c6a35",
    "grass":  "#2f9e3e",
    "grass2": "#43c455",
    "trunk":  "#a3703f",
    "canopy": "#2ea043",
    "canopy2":"#37c24a",
    "water":  "#1f8fc0",
    "water2": "#4fd6f2",
    "refl":   "#ffe488",
    "koiO":   "#ff8a3d",
    "koiR":   "#f8544f",
    "koiG":   "#ffd24a",
    "pad":    "#2ea043",
    "reed":   "#3f9a4a",
    "flowerP":"#ff7ab8",
    "flowerY":"#ffd24a",
}

def ell(c, r, cx, cy, rx, ry):
    dx = (c - cx) / rx
    dy = (r - cy) / ry
    return dx * dx + dy * dy <= 1.0

HORIZON = 16

def region(c, r):
    # --- foreground: flowers, reeds ---
    for (fc, fr, col) in [(6,26,"flowerP"),(15,27,"flowerY"),(83,26,"flowerP"),(89,27,"flowerY")]:
        if abs(c-fc) <= 1 and fr-1 <= r <= fr:
            return col
    # reeds by the lake edges (vertical strokes)
    if c in (13,14) and 20 <= r <= 25: return "reed"
    if c in (78,79) and 20 <= r <= 25: return "reed"

    # --- lake region (ellipse) ---
    in_lake = ell(c, r, 46, 23, 31, 5.2)
    if in_lake:
        # koi fish inside the lake
        if ell(c, r, 32, 24, 4.0, 1.8): return "koiO"
        if ell(c, r, 58, 25, 3.6, 1.6): return "koiR"
        if ell(c, r, 49, 22, 3.0, 1.4): return "koiG"
        # lily pads
        if ell(c, r, 40, 25, 2.0, 1.0): return "pad"
        if ell(c, r, 62, 24, 2.0, 1.0): return "pad"
        # shimmering sun reflection on the water
        if ell(c, r, 46, 21, 9, 1.2): return "refl"
        # brighter water toward the center
        if ell(c, r, 46, 22.5, 20, 3.1): return "water2"
        return "water"

    # --- trees (canopy + trunk), sitting on the ground ---
    trees = [
        dict(tc=11, cy=11, rx=5.0, ry=3.6, th=20, extra=[(7,12,3.2,2.4),(15,12,3.4,2.5),(11,8.5,3.0,2.4)]),
        dict(tc=24, cy=12, rx=3.4, ry=2.6, th=18, extra=[(21,12.5,2.2,1.8),(27,12.5,2.3,1.9)]),
        dict(tc=84, cy=11, rx=5.2, ry=3.8, th=21, extra=[(80,12,3.4,2.6),(88,12,3.5,2.6),(84,8,3.0,2.4)]),
        dict(tc=71, cy=12, rx=3.2, ry=2.5, th=18, extra=[(68,12.5,2.1,1.7),(74,12.5,2.2,1.8)]),
    ]
    for t in trees:
        if r >= HORIZON and (c == t["tc"] or c == t["tc"]+1) and r <= t["th"]:
            return "trunk"
        if ell(c, r, t["tc"]+0.5, t["cy"], t["rx"], t["ry"]):
            return "canopy" if (c + r) % 2 else "canopy2"
        for (ec, er, erx, ery) in t["extra"]:
            if ell(c, r, ec, er, erx, ery):
                return "canopy2" if (c + r) % 2 else "canopy"

    # --- sun + glow (top right) ---
    if ell(c, r, 76, 4, 5.5, 3.4): return "sun"
    if ell(c, r, 76, 4, 9.5, 6.0): return "sunglow"

    # --- clouds ---
    if ell(c, r, 20, 4, 7.0, 2.4) or ell(c, r, 45, 3, 5.5, 2.0): return "cloud"

    # --- ground vs sky ---
    if r >= HORIZON:
        if r == HORIZON or r == HORIZON+1:
            return "hill"
        return "grass2" if (c + r) % 3 == 0 else "grass"
    return "sky"


def bit(c, r):
    return (c * 31 + r * 17 + c * r * 3) % 7 % 2  # deterministic 0/1


def main():
    width = W * CW + 2 * PAD
    height = H * CH + 2 * PAD
    out = []
    out.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="{width}" height="{height}" role="img" '
        f'aria-label="A garden scene — lake, koi, trees and grass — drawn from binary digits">'
    )
    out.append("<title>Binary garden</title>")
    # styles: gentle matrix shimmer via a few staggered flicker classes
    out.append("<style>")
    out.append("text{font-family:'SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace;"
               f"font-size:{FS}px;font-weight:600;}}")
    for i in range(6):
        delay = round(i * 0.5, 2)
        out.append(f".f{i}{{animation:flick 3.4s ease-in-out {delay}s infinite;}}")
    out.append("@keyframes flick{0%,100%{opacity:1}50%{opacity:.55}}")
    out.append(".dim{opacity:.5}")
    out.append("</style>")
    out.append(f'<rect width="{width}" height="{height}" fill="{BG}"/>')

    # subtle vignette-free background grid of very dim digits already covered by sky/grass
    for r in range(H):
        y = PAD + r * CH + FS
        row_cells = []
        for c in range(W):
            x = PAD + c * CW
            reg = region(c, r)
            # thin the sky so it reads as open air, not noise
            if reg == "sky" and (c * 13 + r * 7) % 5 < 2:
                continue
            color = COL[reg]
            cls = f"f{(c * 5 + r * 3) % 6}"
            extra = ' class="%s dim"' % cls if reg == "sky" else ' class="%s"' % cls
            row_cells.append(f'<text x="{x}" y="{y}" fill="{color}"{extra}>{bit(c,r)}</text>')
        out.append("".join(row_cells))

    # a few brighter "rain" streaks falling through the sky
    streaks = [(9, "#8affc0"), (34, "#8affc0"), (58, "#a8e6ff"), (67, "#8affc0")]
    for (col, color) in streaks:
        x = PAD + col * CW
        dur = 4 + (col % 5)
        out.append(
            f'<text x="{x}" y="0" fill="{color}" opacity="0.9">'
            f'<animate attributeName="y" values="-10;{PAD + (HORIZON-1)*CH}" '
            f'dur="{dur}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;0.95;0" dur="{dur}s" repeatCount="indefinite"/>'
            f'{(col) % 2}</text>'
        )

    out.append("</svg>")
    with open("assets/garden.svg", "w") as f:
        f.write("\n".join(out))
    print(f"wrote assets/garden.svg  ({width}x{height}px, {W*H} digits)")


if __name__ == "__main__":
    main()
