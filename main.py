import os
from PIL import Image, ImageDraw, ImageFont
W, H = 1024, 1024
OUT = os.path.join(os.environ.get('MAKEFUN_OUTPUT_DIR', 'out'), 'entry.png')
BG, INK, RED, NAVY, CREAM, GREY, GREEN, BLUE, ORANGE = (250, 246, 236), (20, 20, 20), (178, 34, 34), (28, 48, 88), (238, 228, 205), (110, 110, 110), (34, 120, 60), (30, 90, 170), (200, 110, 20)
def F(s, b=False, serif=False):
    p = '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf' if serif and b else '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if b else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    try: return ImageFont.truetype(p, s)
    except Exception: return ImageFont.load_default()
def wrap(d, t, f, w):
    words, lines, cur = t.split(), [], ''
    for wd in words:
        s = (cur + ' ' + wd).strip()
        if d.textlength(s, font=f) <= w: cur = s
        else: lines.append(cur); cur = wd
    if cur: lines.append(cur)
    return lines
def text(d, x, y, t, f, fill=INK, anchor='la'):
    d.text((x, y), t, font=f, fill=fill, anchor=anchor)
def chip(d, x, y, label):
    c = {'CONFIRMED': GREEN, 'OFFICIAL': BLUE, 'REPORTED': (90, 90, 90), 'CLAIM': ORANGE}.get(label, (90, 90, 90))
    f = F(8, True); w = d.textlength(label, font=f) + 10
    d.rounded_rectangle([x, y, x + w, y + 13], 3, fill=c); d.text((x + 5, y + 2), label, font=f, fill=(255, 255, 255)); return w
def scene(d, x, y, w, h, kind, giant=None):
    d.rectangle([x, y, x + w, y + h], fill=NAVY if kind in ('tower', 'court', 'party') else (45, 70, 110) if kind == 'sea' else (70, 90, 60) if kind == 'field' else (60, 60, 90))
    d.rectangle([x, y + h - 18, x + w, y + h], fill=(30, 30, 30))
    if kind == 'tower':
        d.rectangle([x + w * .42, y + 12, x + w * .58, y + h - 18], fill=(200, 200, 210)); d.polygon([(x + w * .42, y + 12), (x + w * .5, y - 2), (x + w * .58, y + 12)], fill=(220, 220, 230))
        for i in range(5): d.rectangle([x + w * .08 + i * w * .15, y + h - 38, x + w * .19 + i * w * .15, y + h - 18], fill=(90, 90, 110))
        d.ellipse([x + w * .62, y + 8, x + w * .78, y + 24], fill=(255, 180, 60)); d.polygon([(x + w * .66, y + 30), (x + w * .74, y + 26), (x + w * .70, y + 36)], fill=(255, 120, 40))
    elif kind == 'party':
        d.rectangle([x + w * .30, y + 20, x + w * .70, y + h - 18], fill=(150, 40, 40)); d.rectangle([x + w * .44, y + 45, x + w * .56, y + h - 18], fill=(40, 40, 40))
        d.rectangle([x + w * .10, y + h - 42, x + w * .30, y + h - 18], fill=(240, 240, 230)); d.line([x + w * .10, y + h - 42, x + w * .30, y + h - 42], fill=RED, width=3); d.rectangle([x + w * .72, y + 30, x + w * .92, y + h - 30], fill=(245, 245, 240)); d.line([x + w * .75, y + 38, x + w * .89, y + 38], fill=INK, width=2); d.line([x + w * .75, y + 46, x + w * .89, y + 46], fill=INK, width=2)
    elif kind == 'court':
        d.rectangle([x + w * .15, y + 22, x + w * .85, y + h - 18], fill=(210, 205, 190)); d.polygon([(x + w * .12, y + 22), (x + w * .5, y + 2), (x + w * .88, y + 22)], fill=(180, 40, 40))
        for i in range(4): d.rectangle([x + w * .20 + i * w * .16, y + 34, x + w * .28 + i * w * .16, y + h - 18], fill=(240, 235, 220))
    elif kind == 'sea':
        d.rectangle([x, y + h - 16, x + w, y + h], fill=(30, 80, 120)); d.rectangle([x + w * .25, y + h - 34, x + w * .75, y + h - 16], fill=(200, 60, 40)); d.rectangle([x + w * .35, y + h - 44, x + w * .65, y + h - 34], fill=(240, 240, 240))
    elif kind == 'chart':
        d.line([(x + 8, y + h - 22), (x + w * .4, y + h - 45), (x + w * .7, y + h - 55), (x + w - 8, y + 10)], fill=(255, 210, 60), width=4)
        d.line([(x + 8, y + h - 30), (x + w - 8, y + h - 30)], fill=(255, 255, 255), width=2)
    elif kind == 'trophy':
        d.ellipse([x + w * .40, y + 6, x + w * .60, y + 26], fill=(255, 210, 60)); d.rectangle([x + w * .46, y + 26, x + w * .54, y + h - 6], fill=(255, 210, 60))
    elif kind == 'space':
        d.ellipse([x + w * .70, y + 8, x + w * .86, y + 24], fill=(220, 220, 220)); d.rectangle([x + w * .45, y + 20, x + w * .52, y + h - 20], fill=(240, 240, 240)); d.polygon([(x + w * .45, y + 20), (x + w * .485, y + 4), (x + w * .52, y + 20)], fill=(200, 40, 40))
    elif kind == 'heli':
        d.ellipse([x + w * .30, y + 22, x + w * .70, y + 44], fill=(90, 110, 90)); d.line([(x + w * .15, y + 26), (x + w * .85, y + 26)], fill=(200, 200, 200), width=3)
    else:
        d.rectangle([x + w * .20, y + 10, x + w * .80, y + h - 14], fill=(200, 200, 200)); d.rectangle([x + w * .30, y + 18, x + w * .70, y + h - 8], fill=(120, 120, 140))
    if giant:
        gf = F(44 if len(str(giant)) <= 2 else 30, True); d.text((x + w - 8, y + 4), str(giant), font=gf, fill=(255, 255, 255), anchor='ra', stroke_width=2, stroke_fill=(0, 0, 0))
HEROES = [('1 RIYADH \u00b7 MIDDLE EAST', 'CONFIRMED', 'tower', '11', 'Houthi drone hits Riyadh\u2019s tallest tower again, 11 hurt', 'A drone struck the PIF tower, the tallest in Riyadh, for the second time in a week. At least 11 people were hurt, including 2 Saudis, 2 Indians, 3 Nepalis and 4 Egyptians.'), ('2 SHANGHAI \u00b7 ASIA', 'OFFICIAL', 'party', '62', 'China probes Shanghai party chief Chen Jining', 'Chen Jining, 62, faces a probe over serious violations. He is the fourth Politburo member to fall under investigation this year.'), ('3 NEW YORK \u00b7 US / TECH', 'CONFIRMED', 'court', '10/12', 'Huawei guilty on 10 of 12 counts', 'A US jury found Huawei guilty on 10 of 12 counts, including trade-secret theft and bank fraud. It was cleared of racketeering, with sentencing in September 2027.')]
CARDS = [('4 ZAPORIZHZHIA \u00b7 EUROPE', 'REPORTED', 'tower', 'Russian attacks kill 9 across Ukraine in a day', 'Nine were killed and 81 hurt as Russia launched 96 drones, with 73 shot down.'), ('5 CAS \u00b7 AFRICA / SPORT', 'OFFICIAL', 'trophy', 'CAS hands Senegal back the AFCON title', 'CAS restored Senegal as champions after a 3-0 Morocco forfeit, making the final 1-0.'), ('6 HORMUZ \u00b7 MIDDLE EAST', 'REPORTED', 'sea', 'IRGC attacks container ship in Hormuz', 'A container ship was attacked in Hormuz, its navigation disabled near Khasab, Oman.'), ('7 NEW YORK \u00b7 MARKETS', 'CONFIRMED', 'chart', 'Dow closes above 50,000 for the first time', 'The Dow closed at 50,018, first above 50,000, as the Taiex jumped 8.99 percent.'), ('8 REDMOND \u00b7 TECH', 'REPORTED', 'field', 'Microsoft declares \u2018Code Red\u2019 after historic outage', 'After a 24-hour outage, Microsoft set a one-hour global recovery target.'), ('9 ESKISEHIR \u00b7 EUROPE', 'REPORTED', 'heli', 'Turkish military helicopter crash kills 5', 'A military AS-532 helicopter crashed near Eskisehir, killing all five people on board.'), ('10 CARTAGENA \u00b7 AMERICAS', 'REPORTED', 'field', 'Supermarket hostages: 25 held in Cartagena', 'Twenty-five were held hostage in a Cartagena supermarket; five elderly women were freed.'), ('11 ADEN \u00b7 MIDDLE EAST', 'REPORTED', 'sea', 'Houthis advance within 60 km of Aden', 'Houthi forces advanced to within 60 km of Aden, in the latest push in Yemen.'), ('12 LAHJ \u00b7 MIDDLE EAST', 'REPORTED', 'field', 'Saudi strikes kill 25, wound 6 in Yemen', 'Saudi strikes on a bus and truck in Lahj killed 25 people and wounded six.'), ('13 JIUQUAN \u00b7 SPACE', 'OFFICIAL', 'space', 'China names first foreign astronaut for Tiangong', 'China named Tang Hongbo, Wu Yi and Zeeshan Ali, the first foreign astronaut.')]
ALSO = [(14, 'Ankara', 'Haftar visits Turkey for the first time.', 'REPORTED'), (15, 'London', 'UK sanctions Houthis and four officials.', 'OFFICIAL'), (16, 'Villavicencio', 'Car bomb injures 23 people.', 'REPORTED'), (17, 'Gaza', 'Israel kills Hamas internal security chief.', 'REPORTED'), (18, 'Baghdad', 'Iraq orders federal control of Kurdish oilfields.', 'OFFICIAL'), (19, 'Gaza', 'Meningitis alert after 272 cases in October.', 'OFFICIAL'), (20, 'DR Congo', 'Missing Cessna 208, rebels claim shootdown.', 'CLAIM'), (21, 'Hanoi', 'Hot-pot explosion kills at least six.', 'REPORTED'), (22, 'Gulf of Finland', 'Ukraine hits Russian ship Sparta II.', 'REPORTED'), (23, 'Kuala Lumpur', 'Malaysia to return thousands of migrants.', 'OFFICIAL'), (24, 'Ulleungdo', 'South Korea shelter order as Russian jets enter ADIZ.', 'OFFICIAL'), (25, 'Dhaka', 'Hasina plans return on 16 December.', 'REPORTED'), (26, 'The Hague', 'Fourteen nations endorse ICJ Myanmar ruling.', 'REPORTED'), (27, 'Jakarta', 'Indonesia nominates two vice-president candidates.', 'OFFICIAL'), (28, 'Beijing', 'China sentences official Ma to death for spying.', 'OFFICIAL'), (29, 'Brussels', 'NATO vows defence against space threat.', 'OFFICIAL'), (30, 'Mexico City', 'US drone aided El Chapo Isidro capture, arrested Fri 20 Nov.', 'REPORTED'), (31, 'San Salvador', 'Bukele names three soldiers killed in Haiti.', 'OFFICIAL'), (32, 'Ottawa', 'Pentagon rebukes Canada: only 41.9% of air fleet ready.', 'REPORTED'), (33, 'Washington', 'US adds Megaspeed to trade blacklist.', 'OFFICIAL'), (34, 'Kyiv', 'Zelensky urges Ukraine, Russia, US and Europe talks soon.', 'REPORTED'), (35, 'Ras Al Khaimah', 'UAE bus-truck crash kills 13 people.', 'REPORTED'), (36, 'London', 'England records 5,258 heat deaths in summer 2026.', 'OFFICIAL'), (37, 'Kourou', 'Ariane 6 lofts 36 Amazon satellites.', 'OFFICIAL'), (38, 'Cikande', 'Factory-fire toll rises to 26 people.', 'REPORTED')]
NUMBERS = [('11', 'hurt in Riyadh'), ('9', 'killed in Ukraine'), ('50,018', 'Dow close'), ('+8.99%', 'Taiex record'), ('25', 'killed in Yemen'), ('26', 'Cikande toll'), ('10/12', 'Huawei counts'), ('96', 'drones at Ukraine')]
PINS = [(1, 24.7, 46.7, 0, 0), (2, 31.2, 121.5, 0, 0), (3, 40.7, -74.0, 0, 0), (4, 47.8, 35.2, 0, 0), (5, 14.7, -17.4, 0, 0), (6, 26.5, 56.3, 0, 0), (7, 40.7, -74.0, 16, 14), (8, 47.7, -122.1, 0, 0), (9, 39.8, 30.5, 0, 0), (10, 10.4, -75.5, 0, 0), (11, 12.8, 45.0, 0, 0), (12, 13.0, 44.9, -16, 12), (13, 39.7, 98.5, 0, 0)]
LEGEND = ['1 Riyadh', '2 Shanghai', '3 New York', '4 Zaporizhzhia', '5 Dakar', '6 Hormuz', '7 New York', '8 Redmond', '9 Eskisehir', '10 Cartagena', '11 Aden', '12 Lahj', '13 Jiuquan']
LAND = [[(-168, 66), (-140, 70), (-120, 71), (-95, 80), (-80, 73), (-65, 60), (-55, 47), (-70, 42), (-80, 32), (-85, 30), (-97, 26), (-105, 20), (-95, 16), (-85, 12), (-95, 18), (-105, 23), (-120, 32), (-125, 48), (-165, 60)], [(-80, 10), (-60, 5), (-50, 0), (-35, -8), (-40, -20), (-48, -28), (-58, -35), (-65, -45), (-70, -55), (-75, -40), (-80, -20), (-80, -5)], [(-10, 36), (-9, 43), (0, 46), (-2, 50), (5, 53), (8, 57), (18, 56), (21, 60), (30, 70), (40, 68), (35, 60), (28, 45), (23, 40), (19, 42), (12, 44), (3, 42), (-2, 37)], [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (32, 31), (35, 28), (43, 12), (51, 10), (48, 0), (40, -10), (35, -20), (28, -33), (20, -35), (15, -27), (12, -18), (9, 4), (-8, 5), (-15, 12)], [(40, 68), (60, 70), (80, 73), (110, 76), (140, 72), (170, 66), (178, 65), (162, 60), (158, 52), (142, 45), (135, 35), (127, 35), (120, 28), (110, 20), (105, 10), (100, 8), (95, 15), (90, 22), (80, 8), (75, 20), (65, 25), (58, 26), (50, 30), (45, 30), (42, 38)], [(113, -22), (122, -14), (132, -12), (142, -11), (150, -22), (153, -28), (150, -37), (140, -38), (130, -32), (120, -34), (113, -26)], [(-5, 50), (-3, 53), (-5, 56), (-2, 58), (0, 53)], [(130, 31), (135, 34), (140, 38), (142, 43), (140, 45)], [(95, -5), (100, -2), (105, -6), (110, -7), (115, -8), (120, -10)]]
def main():
    im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im); M = 24; x0, x1 = M, W - M; cw = x1 - x0; y = 14
    text(d, x0, y, 'THE WORLD ON ONE PAGE', F(11, True), RED); text(d, x1, y, '38 STORIES \u00b7 6 REGIONS \u00b7 13 FIELDS', F(11, True), INK, 'ra'); y += 18
    d.line([(x0, y), (x1, y)], fill=RED, width=2); y += 6
    text(d, x0, y, 'Tuesday 24 November 2026', F(30, True, True)); text(d, x1, y + 10, 'All from one day', F(11, False), GREY, 'ra'); y += 40
    text(d, x0, y, 'Riyadh tower hit again \u00b7 Shanghai chief probed \u00b7 Huawei guilty on 10 of 12 counts', F(11, False), RED); y += 18
    regs = [('Europe', 9, (200, 60, 60)), ('Middle East', 8, (220, 130, 40)), ('Asia', 8, (40, 120, 80)), ('Africa', 2, (200, 160, 40)), ('Americas', 7, (60, 90, 160)), ('World/Space', 4, (110, 60, 140))]
    bx = x0
    for name, n, col in regs:
        s = f'{name} {n}'; w = d.textlength(s, font=F(10, True)) + 16; d.rounded_rectangle([bx, y, bx + w, y + 20], 3, fill=col); d.text((bx + 8, y + 4), s, font=F(10, True), fill=(255, 255, 255)); bx += w + 6
    text(d, x1, y + 4, 'Wires read to 23:00 UTC', F(9, False), GREY, 'ra'); y += 28
    d.rectangle([x0, y, x1, y + 52], fill=(255, 255, 255), outline=(200, 200, 200))
    for i, (num, lab) in enumerate(NUMBERS):
        cx = x0 + i * cw // 8 + cw // 16; text(d, cx, y + 4, num, F(20, True), RED, 'ma'); text(d, cx, y + 30, lab, F(8, False), GREY, 'ma')
    y += 58
    text(d, x0, y, '02:15 NATO space defence \u00b7 08:16 Hanoi blast \u00b7 10:42 Saudi strikes \u00b7 14:27 Riyadh tower \u00b7 16:51 Houthis near Aden \u00b7 18:58 Hormuz attack \u00b7 20:41 Huawei guilty', F(9, False), INK); y += 16
    hw = (cw - 16) // 3; hy = y
    for i, (kick, st, kind, giant, head, deck) in enumerate(HEROES):
        hx = x0 + i * (hw + 8); d.rectangle([hx, hy, hx + hw, hy + 184], outline=(190, 190, 190), fill=(255, 255, 255))
        scene(d, hx + 1, hy + 1, hw - 2, 96, kind, giant)
        text(d, hx + 6, hy + 102, kick, F(9, True), RED); chip(d, hx + hw - 78, hy + 101, st)
        for j, ln in enumerate(wrap(d, head, F(12, True), hw - 12)): text(d, hx + 6, hy + 118 + j * 14, ln, F(12, True))
        for j, ln in enumerate(wrap(d, deck, F(9, False), hw - 12)[:3]): text(d, hx + 6, hy + 148 + j * 12, ln, F(9, False))
    y = hy + 192
    cw5 = (cw - 32) // 5
    for row in range(2):
        ry = y + row * 116
        for col in range(5):
            c = CARDS[row * 5 + col]; cx = x0 + col * (cw5 + 8); d.rectangle([cx, ry, cx + cw5, ry + 110], outline=(190, 190, 190), fill=(255, 255, 255))
            scene(d, cx + 1, ry + 1, cw5 - 2, 48, c[2])
            text(d, cx + 5, ry + 52, c[0], F(7, True), RED); chip(d, cx + cw5 - 62, ry + 51, c[1])
            hl = wrap(d, c[3], F(9, True), cw5 - 10)
            for j, ln in enumerate(hl[:2]): text(d, cx + 5, ry + 64 + j * 11, ln, F(9, True))
            dl = wrap(d, c[4], F(8, False), cw5 - 10)
            for j, ln in enumerate(dl[:3] if len(hl[:2]) == 1 else dl[:2]): text(d, cx + 5, ry + 64 + len(hl[:2]) * 11 + j * 10, ln, F(8, False))
    y += 240
    text(d, x0, y, 'THE WORLD MAP \u2014 13 STORIES PINNED', F(11, True), INK); y += 16
    mx, my, mw, mh = x0, y, 640, 156
    d.rectangle([mx, my, mx + mw, my + mh], fill=(190, 220, 235), outline=(150, 150, 150))
    def proj(lon, lat): return mx + (lon + 180) / 360 * mw, my + (72 - lat) / (72 + 55) * mh
    for poly in LAND:
        pts = [proj(lon, lat) for lon, lat in poly]; d.polygon(pts, fill=(216, 201, 163), outline=(150, 130, 100))
    for n, lat, lon, dx, dy in PINS:
        px, py = proj(lon, lat); qx, qy = px + dx, py + dy
        if dx or dy: d.line([(px, py), (qx, qy)], fill=RED, width=1)
        d.ellipse([qx - 9, qy - 9, qx + 9, qy + 9], fill=RED, outline=(255, 255, 255)); d.text((qx, qy - 1), str(n), font=F(9, True), fill=(255, 255, 255), anchor='mm')
    lx = mx + mw + 14
    text(d, lx, my, 'PINNED STORIES', F(10, True), RED)
    for i, s in enumerate(LEGEND):
        col = i % 2; r = i // 2; text(d, lx + col * 155, my + 18 + r * 13, s, F(9, False))
    text(d, lx, my + 18 + 7 * 13 + 4, 'Redmond is on the US west', F(9, False), GREY); text(d, lx, my + 18 + 7 * 13 + 16, 'coast, below Canada.', F(9, False), GREY); text(d, lx, my + 18 + 7 * 13 + 28, 'Pins 3 and 7 sit on the', F(9, False), GREY); text(d, lx, my + 18 + 7 * 13 + 40, 'US east coast.', F(9, False), GREY)
    y = my + mh + 8
    text(d, x0, y, 'ALSO ON TUESDAY 24 NOVEMBER \u2014 25 MORE STORIES', F(11, True), INK); y += 16
    for i, (n, city, head, st) in enumerate(ALSO):
        col = i // 9; r = i % 9; ax = x0 + col * (cw // 3 + 4); ay = y + r * 12
        s = f'{n} {city}: {head} [{st}]'; f = F(7, False)
        while d.textlength(s, font=f) > cw // 3 - 4 and ' ' in head: head = head.rsplit(' ', 1)[0].rstrip('.,'); s = f'{n} {city}: {head}. [{st}]'
        text(d, ax, ay, s, f)
    y += 9 * 12 + 4
    d.rectangle([x0, y, x1, y + 38], fill=(178, 34, 34))
    text(d, x0 + 8, y + 4, 'DATE CHECK: Every story happened or was first reported on Tue 24 Nov 2026; wires read to 23:00 UTC. LEFT OUT (not 24 Nov):', F(9, True), (255, 255, 255))
    text(d, x0 + 8, y + 20, 'Hormuz mines (23 Nov) \u00b7 Nvidia CEO (23 Nov) \u00b7 EU sanctions (23 Nov) \u00b7 COP31 (22 Nov) \u00b7 El Chapo arrest Fri 20 Nov. NOT YET: Shenzhou-24 launch (25 Nov) \u00b7 Huawei sentence (Sep 2027) \u00b7 MPR vote (11 Dec).', F(9, False), (255, 255, 255))
    y += 44
    text(d, x0, y, 'Sources: Saudi officials \u00b7 CCDI \u00b7 US court \u00b7 Reuters \u00b7 AP \u00b7 UKMTO \u00b7 CAS \u00b7 CMSA \u00b7 wires. CONFIRMED = 2+ outlets \u00b7 OFFICIAL = on record \u00b7 REPORTED = one outlet \u00b7 CLAIM = one side.', F(8, False), GREY)
    text(d, x0, y + 12, 'Scenes are drawn in code, not photographs. Tuesday 24 November 2026 \u00b7 38 stories \u00b7 drawn in code.', F(8, False), GREY)
    os.makedirs(os.path.dirname(OUT) or '.', exist_ok=True); im.save(OUT, optimize=True)
if __name__ == '__main__': main()
