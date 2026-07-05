#!/usr/bin/env python3
"""Generate a simple, kid-style black & white 'binary garden' SVG.

A big smiley sun, two lollipop trees, an open pond with chunky fish, a cloud,
flowers and scattered grass — all drawn from 0/1 glyphs, white on black, with
lots of space so it stays light and playful."""

W, H = 72, 22
CW, CH = 11, 20
PAD = 18
FS = 18

BG = "#000000"
HI = "#f7f7f7"

FISH = set()


def ell(c, r, cx, cy, rx, ry):
    dx = (c - cx) / rx
    dy = (r - cy) / ry
    return dx * dx + dy * dy <= 1.0


def ring(c, r, cx, cy, rx, ry, t):
    return ell(c, r, cx, cy, rx, ry) and not ell(c, r, cx, cy, rx - t, ry - t)


def cell(c, r):
    # ---------- BIG SMILEY SUN (top-left) ----------
    sx, sy = 9, 5
    for (rc, rr) in [(9, 0), (9, 10), (3, 5), (15, 5), (4, 1), (14, 1), (4, 9), (14, 9)]:
        if (c, r) == (rc, rr):
            return "hi"
    if ell(c, r, sx, sy, 4.6, 4.2):
        if (c, r) in [(7, 4), (11, 4)]:            # eyes
            return None
        if (c, r) in [(7, 6), (8, 7), (9, 7), (10, 7), (11, 6)]:  # smile
            return None
        return "hi"

    # ---------- CLOUD (top middle) ----------
    if r <= 4 and (ell(c, r, 40, 3, 5.0, 1.8) or ell(c, r, 44, 4, 3.2, 1.4) or ell(c, r, 36, 4, 2.8, 1.3)):
        return "hi"

    # ---------- LOLLIPOP TREES ----------
    if c in (23, 24) and 13 <= r <= 18:            # big trunk
        return "hi"
    if ell(c, r, 23.5, 9, 4.6, 4.1):               # big canopy
        return "hi"
    if c in (60, 61) and 13 <= r <= 18:            # small trunk
        return "hi"
    if ell(c, r, 60.5, 10, 3.5, 3.1):              # small canopy
        return "hi"

    # ---------- OPEN POND with CHUNKY FISH ----------
    px, py, prx, pry = 40, 15, 11, 3.4
    if ell(c, r, px, py, prx, pry):
        fishes = [(34, 15), (44, 16)]              # (tail col, row)
        for (fx, fy) in fishes:
            if c == fx and r in (fy - 1, fy + 1):  # tail fork
                FISH.add((c, r)); return "hi"
            if r == fy and fx + 1 <= c <= fx + 4:  # body
                FISH.add((c, r)); return "hi"
        if ring(c, r, px, py, prx, pry, 1.5):      # bright rim, empty inside
            return "hi"
        return None

    # ---------- FLOWERS ----------
    for (fx, fy) in [(14, 17), (56, 16)]:
        if (c, r) in [(fx, fy - 1), (fx - 1, fy), (fx + 1, fy), (fx, fy)]:  # petals + center
            return "hi"
        if c == fx and fy < r <= 20:               # stem
            return "hi"

    # ---------- GRASS TUFTS ----------
    for tc in (4, 11, 20, 30, 40, 50, 62, 68):
        if (c, r) in [(tc, 19), (tc, 20), (tc - 1, 20), (tc + 1, 20)]:
            return "hi"

    return None


def bit(c, r):
    return (c * 31 + r * 17 + c * r * 3) % 7 % 2


def main():
    width = W * CW + 2 * PAD
    height = H * CH + 2 * PAD
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="{width}" height="{height}" role="img" '
        f'aria-label="A simple garden — smiley sun, trees, a pond with fish, a cloud and flowers — drawn from binary digits">',
        "<title>Binary garden</title>",
        "<style>",
        "text{font-family:'SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace;"
        f"font-size:{FS}px;font-weight:700;}}",
        ".tw0{animation:tw 3.6s ease-in-out 0s infinite;}",
        ".tw1{animation:tw 3.6s ease-in-out .7s infinite;}",
        ".tw2{animation:tw 3.6s ease-in-out 1.4s infinite;}",
        "@keyframes tw{0%,100%{opacity:1}50%{opacity:.72}}",
        ".swim{animation:swim 2.8s ease-in-out infinite alternate;}",
        "@keyframes swim{from{transform:translateX(-4px)}to{transform:translateX(4px)}}",
        "</style>",
        f'<rect width="{width}" height="{height}" fill="{BG}"/>',
    ]

    fish_cells = []
    for r in range(H):
        y = PAD + r * CH + FS
        row = []
        for c in range(W):
            if cell(c, r) is None:
                continue
            x = PAD + c * CW
            if (c, r) in FISH:
                fish_cells.append((x, y, bit(c, r)))
                continue
            cls = f"tw{(c + r) % 3}"
            row.append(f'<text x="{x}" y="{y}" fill="{HI}" class="{cls}">{bit(c,r)}</text>')
        if row:
            out.append("".join(row))

    out.append(f'<g class="swim" fill="{HI}">')
    for (x, y, b) in fish_cells:
        out.append(f'<text x="{x}" y="{y}">{b}</text>')
    out.append("</g>")

    out.append("</svg>")
    with open("assets/garden.svg", "w") as f:
        f.write("\n".join(out))
    print(f"wrote assets/garden.svg  ({width}x{height}px)")


if __name__ == "__main__":
    main()
