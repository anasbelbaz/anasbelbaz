import math, random
random.seed(7)

W, Hh = 104, 40
CHW, LH, FS, PAD = 8.0, 15, 13, 14
cx, cy, a, b = 51, 19, 36, 14

g = [[" "]*W for _ in range(Hh)]
def put(r,c,ch,force=False):
    if 0<=r<Hh and 0<=c<W and (force or g[r][c]==" "): g[r][c]=ch

def radius(t):
    return (1 + 0.17*math.sin(3*t+0.6) + 0.12*math.sin(5*t+1.3)
              + 0.07*math.sin(7*t) + 0.05*math.sin(2*t+2.1))
def point(t):
    r = radius(t); return (cx + a*r*math.cos(t), cy + b*r*math.sin(t))
def slope_char(dx, dy):
    ang = math.degrees(math.atan2(dy, dx)) % 180
    if ang < 22.5 or ang >= 157.5: return "="
    if 67.5 <= ang < 112.5:        return "|"
    return "/" if (dy/dx if dx else 9) < 0 else "\\"

N = 1000
centre_px = []
for i in range(N):
    t = 2*math.pi*i/N
    gx, gy = point(t); gx2, gy2 = point(t+0.01)
    centre_px.append((PAD+gx*CHW, PAD+gy*LH))
    put(round(gy), round(gx), slope_char(gx2-gx, gy2-gy))

gx, gy = point(math.pi/2); gx2, gy2 = point(math.pi/2+0.01)
px, py = PAD+gx*CHW, PAD+gy*LH
dx, dy = (gx2-gx)*CHW, (gy2-gy)*LH; L=math.hypot(dx,dy) or 1
nx, ny = -dy/L, dx/L
for k,s in enumerate(range(-10,11,4)):
    put(round((py+ny*s-PAD)/LH), round((px+nx*s-PAD)/CHW), "#" if k%2 else ":", force=True)

lines = ["".join(r).rstrip() for r in g]
Wd = max(len(l) for l in lines); width=round(Wd*CHW)+2*PAD; height=Hh*LH+2*PAD
def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
out=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">',
"<style>text{font-family:Consolas,Menlo,monospace;font-size:%dpx;font-weight:600;fill:#1f2328;white-space:pre;}"
"@media(prefers-color-scheme:dark){text{fill:#e6edf3;}} .car{font-weight:800;} "
'.memo{font-family:"Segoe Script","Bradley Hand","Snell Roundhand","Brush Script MT",'
'"Lucida Handwriting",cursive;font-weight:500;font-size:26px;}</style>'%FS]
for i,l in enumerate(lines):
    out.append(f'<text x="{PAD}" y="{PAD+i*LH+FS}" xml:space="preserve">{esc(l)}</text>')

mx, my = PAD+cx*CHW, PAD+cy*LH
out.append(f'<text class="memo" x="{mx:.0f}" y="{my-8:.0f}" text-anchor="middle">in loving memory of</text>')
out.append(f'<text class="memo" x="{mx:.0f}" y="{my+18:.0f}" text-anchor="middle">loving memories...</text>')

# ---- little car sprites lapping the circuit ----
SPRITE = ["  ___  ", "_/o o\\_", " (_)(_)"]     # 3-line side-view car
pts = centre_px[::6]
d = "M " + " L ".join(f"{x:.1f},{y:.1f}" for (x,y) in pts) + " Z"
for k in range(5):
    dur = round(random.uniform(7.5, 11.0), 1)
    beg = round(-random.uniform(0.0, dur), 1)
    rows = "".join(
        f'<text class="car" x="0" y="{off}" text-anchor="middle" xml:space="preserve">{esc(SPRITE[i])}</text>'
        for i, off in enumerate((-9, 4, 17)))
    out.append(f'<g>{rows}<animateMotion dur="{dur}s" begin="{beg}s" '
               f'repeatCount="indefinite" path="{d}"/></g>')
out.append("</svg>")
open("assets/track.svg","w").write("\n".join(out))
print("\n".join(lines[:2]), "...")
