#!/usr/bin/env python3
"""Render a small, kid-style ASCII-art garden as a transparent SVG.

Real ASCII symbols (not 0/1): a smiley sun, a cloud, two trees, a pond with
fish, grass and little flowers. Transparent background; the text color adapts
to light/dark themes. Regenerate with: python3 gen_garden.py"""

W, H = 46, 11
CHW = 8.43          # monospace advance at the font size below
LH = 17
FS = 14
PAD = 16


def build_grid():
    g = [[" "] * W for _ in range(H)]

    def put(r, c, s):
        for i, ch in enumerate(s):
            if 0 <= r < H and 0 <= c + i < W:
                g[r][c + i] = ch

    # sun (top-left) with a little face
    put(0, 6, "\\  |  /")
    put(1, 4, "--  (o)  --")
    put(2, 6, "/  |  \\")

    # cloud (top-right)
    put(1, 32, ".-~~~-.")
    put(2, 31, "(       )")
    put(3, 32, "`-~~~-'")

    # left tree
    put(4, 4, "####")
    put(5, 3, "######")
    put(6, 4, "####")
    put(7, 5, "||")
    put(8, 5, "||")

    # right tree
    put(4, 38, "####")
    put(5, 37, "######")
    put(6, 38, "####")
    put(7, 39, "||")
    put(8, 39, "||")

    # pond with two fish
    put(7, 17, "_.-~~~~~~~-._")
    put(8, 15, "(   ><>   <><   )")
    put(9, 16, "`-.__~~~__.-'")

    # grass: fill the two bottom rows, then dot in flowers
    for c in range(W):
        if g[9][c] == " ":
            g[9][c] = ","
    for c in range(W):
        g[10][c] = ","
    for c in (4, 11, 34, 42):
        g[10][c] = "*"

    return ["".join(row).rstrip() for row in g]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def main():
    lines = build_grid()
    maxlen = max(len(l) for l in lines)
    width = round(maxlen * CHW) + 2 * PAD
    height = H * LH + 2 * PAD

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="{width}" height="{height}" role="img" '
        f'aria-label="A small ASCII-art garden: a smiley sun, two trees, a pond with fish, a cloud and flowers">',
        "<title>ASCII garden</title>",
        "<style>",
        "text{font-family:'SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace;"
        f"font-size:{FS}px;font-weight:600;fill:#24292f;white-space:pre;}}",
        "@media (prefers-color-scheme:dark){text{fill:#e6edf3;}}",
        "</style>",
    ]
    for i, line in enumerate(lines):
        y = PAD + i * LH + FS
        out.append(f'<text x="{PAD}" y="{y}" xml:space="preserve">{esc(line)}</text>')
    out.append("</svg>")

    with open("assets/garden.svg", "w") as f:
        f.write("\n".join(out))
    print(f"wrote assets/garden.svg  ({width}x{height}px, transparent)")


if __name__ == "__main__":
    main()
