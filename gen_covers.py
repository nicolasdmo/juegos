import hashlib, os, json

OUT = "C:/Users/nico/juegos/roms/covers"
os.makedirs(OUT, exist_ok=True)

CONSOLES = {
    "nes":   {"color": "#f87171", "dark": "#3b0202", "label": "NES",  "stripe": "#ef4444"},
    "gb":    {"color": "#4ade80", "dark": "#012b0f", "label": "GB",   "stripe": "#22c55e"},
    "sms":   {"color": "#38bdf8", "dark": "#011929", "label": "SMS",  "stripe": "#0ea5e9"},
    "gg":    {"color": "#fb923c", "dark": "#1c0a00", "label": "GG",   "stripe": "#f97316"},
    "atari": {"color": "#c084fc", "dark": "#1a0428", "label": "ATR",  "stripe": "#a855f7"},
}

GAMES = [
    ("blaster.nes",            "Blaster",            "nes"),
    ("cheril-the-goddess.nes", "Cheril the Goddess", "nes"),
    ("croom.nes",              "Croom",              "nes"),
    ("driar.nes",              "Driar",              "nes"),
    ("flappybird.nes",         "Flappy Bird",        "nes"),
    ("invaders.nes",           "Invaders",           "nes"),
    ("snailmaze.nes",          "Snail Maze",         "nes"),
    ("super-tilt-bro.nes",     "Super Tilt Bro",     "nes"),
    ("thwaite.nes",            "Thwaite",            "nes"),
    ("twindragons.nes",        "Twin Dragons",       "nes"),
    ("blastah.gb",             "Blastah",            "gb"),
    ("brickster.gbc",          "Brickster",          "gb"),
    ("burly.gbc",              "Burly",              "gb"),
    ("combatsoccer.gbc",       "Combat Soccer",      "gb"),
    ("geometrix.gbc",          "Geometrix",          "gb"),
    ("initiald.gbc",           "Initial D",          "gb"),
    ("klondike.gbc",           "Klondike",           "gb"),
    ("pokedamon.gbc",          "Pokedamon",          "gb"),
    ("ucity.gbc",              "uCity GBC",          "gb"),
    ("3dcity.sms",             "3D City",            "sms"),
    ("astroforce.sms",         "Astro Force",        "sms"),
    ("blockquest.sms",         "Block Quest",        "sms"),
    ("bloki.sms",              "Bloki",              "sms"),
    ("datastorm.sms",          "Datastorm",          "sms"),
    ("galacticrevenge.sms",    "Galactic Revenge",   "sms"),
    ("lander1.sms",            "Lander",             "sms"),
    ("pongmaster.sms",         "Pong Master",        "sms"),
    ("shootingstars.sms",      "Shooting Stars",     "sms"),
    ("waimanu.sms",            "Waimanu",            "sms"),
    ("dangerousdemolition.gg", "Dangerous Demo",     "gg"),
    ("firetrack.gg",           "Fire Track",         "gg"),
    ("nibbles.gg",             "Nibbles",            "gg"),
    ("swabby.gg",              "Swabby",             "gg"),
    ("wingwarriors.gg",        "Wing Warriors",      "gg"),
    ("anguna.bin",             "Anguna",             "atari"),
    ("bitquest.bin",           "Bit Quest",          "atari"),
    ("fishy.bin",              "Fishy",              "atari"),
    ("flappy_the_duck.bin",    "Flappy the Duck",    "atari"),
    ("halo2600.bin",           "Halo 2600",          "atari"),
    ("nanowing.bin",           "Nano Wing",          "atari"),
    ("stardust.bin",           "Stardust",           "atari"),
    ("thrust.bin",             "Thrust",             "atari"),
    ("turtlebay.bin",          "Turtle Bay",         "atari"),
    ("winterfortress.bin",     "Winter Fortress",    "atari"),
]

def nh(name):
    return int(hashlib.md5(name.encode()).hexdigest(), 16)

def hsl(h, s, l):
    h = (h % 360) / 360.0
    s = s / 100.0
    l = l / 100.0
    if s == 0:
        r = g = b = l
    else:
        def htr(p, q, t):
            t = t % 1.0
            if t < 1/6.0: return p + (q - p) * 6 * t
            if t < 0.5:   return q
            if t < 2/3.0: return p + (q - p) * (2/3.0 - t) * 6
            return p
        q = l * (1 + s) if l < 0.5 else l + s - l * s
        p = 2 * l - q
        r = htr(p, q, h + 1/3.0)
        g = htr(p, q, h)
        b = htr(p, q, h - 1/3.0)
    return "#{:02x}{:02x}{:02x}".format(int(r*255), int(g*255), int(b*255))

def make_svg(filename, display_name, con_id):
    c = CONSOLES[con_id]
    h = nh(filename)

    hue  = h % 360
    hue2 = (hue + 55) % 360
    hue3 = (hue + 130) % 360

    bg1  = hsl(hue,  30, 7)
    bg2  = hsl(hue2, 40, 12)
    acc1 = hsl(hue,  88, 60)
    acc2 = hsl(hue2, 88, 55)
    acc3 = hsl(hue3, 75, 72)

    # 8x9 pixel sprite, mirrored
    PX = 13
    COLS, ROWS = 8, 9
    sw = COLS * PX - 1
    spx = (200 - sw) // 2
    spy = 8
    pixel_rects = []
    colors = [acc1, acc2, acc3, hsl(hue, 65, 80)]
    for row in range(ROWS):
        for half in range(4):
            bit = (h >> (row * 4 + half)) & 1
            if not bit:
                continue
            for col in [half, COLS - 1 - half]:
                px = spx + col * PX
                py = spy + row * PX
                ci = (row + half + (h >> (row + half + 3))) % len(colors)
                pixel_rects.append(
                    '<rect x="{}" y="{}" width="12" height="12" fill="{}"/>'.format(px, py, colors[ci])
                )

    # Tiny star dots
    star_rects = []
    for i in range(7):
        sx = (h >> (i * 6 + 1)) % 185 + 7
        sy = (h >> (i * 6 + 4)) % 108 + 4
        ci = i % len(colors)
        star_rects.append(
            '<rect x="{}" y="{}" width="2" height="2" fill="{}" opacity="0.55"/>'.format(sx, sy, colors[ci])
        )

    # Title lines
    words = display_name.split()
    lines = []
    cur = ""
    for w in words:
        candidate = (cur + " " + w).strip()
        if len(candidate) <= 13:
            cur = candidate
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    lines = lines[:2]

    title_els = []
    base_y = 158
    for i, ln in enumerate(lines):
        ty = base_y + i * 22
        title_els.append(
            '<text x="100" y="{}" text-anchor="middle" font-family="monospace,sans-serif" '
            'font-size="13" font-weight="900" letter-spacing="1" fill="white">{}</text>'.format(ty, ln.upper())
        )

    uid = abs(h) % 999999

    lines_svg   = "\n      ".join(pixel_rects)
    stars_svg   = "\n      ".join(star_rects)
    title_svg   = "\n      ".join(title_els)

    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 280" width="200" height="280">\n'
        '  <defs>\n'
        '    <linearGradient id="bg{u}" x1="0" y1="0" x2="0.6" y2="1">\n'
        '      <stop offset="0%" stop-color="{b1}"/>\n'
        '      <stop offset="100%" stop-color="{b2}"/>\n'
        '    </linearGradient>\n'
        '    <linearGradient id="bot{u}" x1="0" y1="0" x2="0" y2="1">\n'
        '      <stop offset="0%" stop-color="rgba(0,0,0,0.52)"/>\n'
        '      <stop offset="100%" stop-color="rgba(0,0,0,0.88)"/>\n'
        '    </linearGradient>\n'
        '    <pattern id="scan{u}" width="1" height="3" patternUnits="userSpaceOnUse">\n'
        '      <rect y="2" width="200" height="1" fill="rgba(0,0,0,0.12)"/>\n'
        '    </pattern>\n'
        '  </defs>\n'
        '  <rect width="200" height="280" fill="url(#bg{u})"/>\n'
        '  <rect width="200" height="280" fill="url(#scan{u})"/>\n'
        '  {stars}\n'
        '  <rect x="0" y="0" width="200" height="134" fill="rgba(0,0,0,0.22)"/>\n'
        '  {pixels}\n'
        '  <rect x="0" y="130" width="200" height="3" fill="{a1}" opacity="0.9"/>\n'
        '  <rect x="0" y="133" width="200" height="1" fill="{a2}" opacity="0.4"/>\n'
        '  <rect x="0" y="134" width="200" height="146" fill="url(#bot{u})"/>\n'
        '  <rect x="0" y="134" width="5" height="146" fill="{stripe}" opacity="0.88"/>\n'
        '  {title}\n'
        '  <rect x="12" y="250" width="44" height="18" rx="3" fill="{ccolor}" opacity="0.92"/>\n'
        '  <text x="34" y="263" text-anchor="middle" font-family="monospace" font-size="10" font-weight="700" fill="#000">{label}</text>\n'
        '  <rect x="134" y="250" width="54" height="18" rx="3" fill="rgba(255,255,255,0.06)" stroke="{a1}" stroke-width="1"/>\n'
        '  <text x="161" y="263" text-anchor="middle" font-family="monospace" font-size="7" fill="{a1}" letter-spacing="0.5">HOMEBREW</text>\n'
        '</svg>'
    ).format(
        u=uid, b1=bg1, b2=bg2, a1=acc1, a2=acc2,
        stripe=c["stripe"], ccolor=c["color"], label=c["label"],
        stars=stars_svg, pixels=lines_svg, title=title_svg
    )
    return svg

covers_by_console = {k: {} for k in CONSOLES}
for fname, dname, con_id in GAMES:
    svg = make_svg(fname, dname, con_id)
    out_name = fname.rsplit(".", 1)[0] + ".svg"
    out_path = os.path.join(OUT, out_name)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg)
    covers_by_console[con_id][fname] = "roms/covers/" + out_name

base = "C:/Users/nico/juegos/roms"
for con_id, mapping in covers_by_console.items():
    if not mapping:
        continue
    p = os.path.join(base, con_id, "covers.json")
    with open(p, "w", encoding="utf-8") as f:
        json.dump(mapping, f, indent=2, ensure_ascii=False)

print("Done! {} covers generated".format(len(GAMES)))
for k, m in covers_by_console.items():
    print("  {}: {} games".format(k, len(m)))
