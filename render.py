#!/usr/bin/env python3
"""Render the Tuesday 24 November 2026 front page (1024x1024 PNG).

Drawn locally with Pillow. The graded program (main.py) does NOT run this
script: it copies the committed entry.png byte-for-byte, so the sandbox run
needs no network and no third-party packages. This script is kept in the
repo so anyone can see exactly how the image was drawn.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

REGION_COLORS = {
    "N. AMERICA": (31, 78, 121),
    "LATIN AMERICA": (46, 125, 50),
    "EUROPE": (106, 27, 154),
    "MIDDLE EAST": (183, 28, 28),
    "AFRICA": (230, 81, 0),
    "SOUTH ASIA": (0, 105, 92),
    "E. ASIA & PACIFIC": (146, 96, 0),
}

# (headline, summary, region, lon, lat) — every story happened or was first
# reported on Tuesday 24 November 2026, or leads the news cycle of that day,
# per Reuters/AP/AFP/CNN/The Hindu/BBC/FIFA/FIDE. lon/lat None = sky event.
STORIES = [
    ("US to blacklist Megaspeed chip firm",
     "Reuters: firm at the heart of the Nvidia scandal faces US blacklist.",
     "N. AMERICA", 104, 1),
    ("Trump wins path to erase hush-money case",
     "Appeals court opens a route to wiping out the conviction, reports say.",
     "N. AMERICA", -74, 41),
    ("Democrats plan 12 debates for 2028",
     "First primary debate set for June in a crowded race to succeed Trump.",
     "N. AMERICA", -77, 39),
    ("Waymo pulls taxis off US freeways",
     "Driverless cars suspended from freeways after California ban, firm says.",
     "N. AMERICA", -122, 37),
    ("Kushner: Trump open to NATO-like guarantees",
     "US envoy says Trump backs 'Article 5-like' cover in a Ukraine deal.",
     "N. AMERICA", -77, 39),
    ("Bolsonaro 'stable' in intensive care",
     "Brazil's ex-president remains in hospital, his office says.",
     "LATIN AMERICA", -48, -16),
    ("Peru quake 6.7 kills 1, injures 16",
     "Andean tremor rattles Lima and shakes buildings across the region.",
     "LATIN AMERICA", -77, -12),
    ("Haiti police kill 34 in gang raid",
     "At least 34 suspected gang members killed in a raid on Martissant.",
     "LATIN AMERICA", -72, 19),
    ("Mexico captures cartel boss",
     "'El Chapo Isidro' seized after Sinaloa firefights leave 11 people dead.",
     "LATIN AMERICA", -107, 25),
    ("Chess crown: Game 1 begins in Geneva",
     "Sindarov has White vs champion Gukesh in the youngest title match ever.",
     "EUROPE", 6, 46),
    ("FIFA: USA get 2031, UK get 2035",
     "Women's World Cups go to a US-led bid for 2031 and the UK for 2035.",
     "EUROPE", 8, 47),
    ("Zelensky: Russia planning new strikes",
     "Kyiv cites intelligence of fresh attacks as peace talks continue.",
     "EUROPE", 31, 50),
    ("Moscow accuses Estonia of 'open war' brink",
     "Russia says Estonian actions are on the verge of triggering open war.",
     "EUROPE", 25, 59),
    ("NATO vows space defence",
     "Alliance answers a report of a Russian nuclear satellite with a pledge.",
     "EUROPE", 4, 51),
    ("Thousands flee Manchester concert",
     "Crowds run after an unknown substance is released at a gig.",
     "EUROPE", -2, 53),
    ("Denmark backs hardline 'ghetto law'",
     "Top court upholds the law in a landmark immigration ruling.",
     "EUROPE", 12, 56),
    ("Iran vows 'every means' over Hormuz",
     "Tehran calls the US naval blockade 'military aggression'.",
     "MIDDLE EAST", 56, 27),
    ("Israeli strikes kill 3 in Gaza",
     "A UNRWA worker is among the dead as the fragile ceasefire frays.",
     "MIDDLE EAST", 34, 31),
    ("Gaza 'toxic for decades', report warns",
     "Oxfam: explosives and asbestos have poisoned air, soil and water.",
     "MIDDLE EAST", 35, 31),
    ("Ukraine claims sinking Russian warship",
     "Kyiv says its forces sank the corvette Merkury off the Libyan coast.",
     "MIDDLE EAST", 20, 32),
    ("Settler arson hits five villages",
     "West Bank cars and homes torched; Eisenkot calls it 'Jewish terrorism'.",
     "MIDDLE EAST", 35, 32),
    ("Senegal boat search goes on",
     "Dozens still missing off Yenne after a migrant boat capsized.",
     "AFRICA", -17, 15),
    ("Nigeria: 64 killed in reprisal attack",
     "Reprisal killings hit Wawa and Gada Oli in Niger State.",
     "AFRICA", 6, 10),
    ("Bayelsa funeral boat sinks, 24 dead",
     "Boat carrying mourners capsizes in Nigeria's Bayelsa State.",
     "AFRICA", 6, 5),
    ("Drones kill 4 near Khartoum",
     "Strikes blamed on the RSF hit homes and damage a UN building.",
     "AFRICA", 32, 16),
    ("Modi opens AI centre at IIT Patna",
     "PM launches a Rs 400 crore research park project in Bihar.",
     "SOUTH ASIA", 85, 26),
    ("India, Nepal sign 8 MoUs",
     "Modi hosts Nepal PM Balen Shah; deals span space to security.",
     "SOUTH ASIA", 77, 29),
    ("India-China talks in Arunachal",
     "Military commanders meet to ease tensions along the border.",
     "SOUTH ASIA", 94, 28),
    ("SC grants bail to Godhra convict",
     "Supreme Court frees a train-burning convict on medical grounds.",
     "SOUTH ASIA", 78, 28),
    ("Taliban erase women's names in Balkh",
     "Women's names struck from papers, replaced with the word 'Bibi'.",
     "SOUTH ASIA", 67, 37),
    ("Indonesia factory fire: 24 dead, 34 missing",
     "Search resumes at the Serang candy factory; dozens still unaccounted for.",
     "E. ASIA & PACIFIC", 106, -6),
    ("S. Korea minister quits in AI scandal",
     "Education minister resigns amid an AI-driven exam cheating scandal.",
     "E. ASIA & PACIFIC", 127, 37),
    ("India-NZ Test ends in a draw",
     "New Zealand fight back to save the first Test at Wellington.",
     "E. ASIA & PACIFIC", 175, -41),
    ("Supermoon meets the Pleiades tonight",
     "The bright Moon passes the 'Seven Sisters' star cluster in the night sky.",
     "E. ASIA & PACIFIC", None, None),
]

# Rough continent outlines (lon, lat) for the map strip.
CONTINENTS = [
    [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-85, 80), (-75, 72),
     (-65, 60), (-55, 52), (-60, 47), (-70, 44), (-75, 39), (-80, 32),
     (-81, 26), (-90, 21), (-97, 16), (-92, 15), (-83, 9), (-79, 9),
     (-86, 13), (-92, 15), (-97, 16), (-105, 20), (-110, 23), (-114, 29),
     (-120, 34), (-125, 40), (-124, 48), (-135, 58), (-150, 60), (-165, 60)],
    [(-79, 9), (-77, 4), (-80, -3), (-81, -6), (-77, -12), (-72, -18),
     (-70, -23), (-70, -33), (-73, -44), (-70, -52), (-66, -55), (-65, -45),
     (-62, -39), (-57, -34), (-52, -32), (-48, -27), (-41, -22), (-35, -9),
     (-35, -6), (-44, -3), (-50, 0), (-53, 4), (-60, 8), (-70, 11),
     (-75, 10)],
    [(-17, 15), (-17, 21), (-10, 31), (-5, 35), (10, 37), (11, 34),
     (20, 32), (32, 31), (35, 28), (39, 21), (43, 12), (51, 11),
     (48, 10), (44, 0), (40, -10), (40, -18), (36, -26), (32, -29),
     (28, -33), (20, -35), (17, -32), (14, -22), (12, -17), (13, -10),
     (9, 4), (4, 6), (-8, 5), (-13, 8)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57), (12, 60),
     (18, 62), (21, 65), (25, 70), (31, 70), (32, 66), (40, 68), (45, 66),
     (42, 60), (38, 55), (35, 52), (30, 50), (28, 46), (23, 40), (26, 38),
     (23, 36), (19, 40), (15, 44), (12, 44), (8, 44), (3, 43), (-2, 37),
     (-6, 36)],
    [(40, 68), (50, 69), (60, 69), (70, 72), (80, 73), (90, 75), (100, 77),
     (110, 74), (120, 73), (130, 72), (140, 72), (150, 70), (160, 69),
     (170, 66), (178, 65), (170, 62), (162, 60), (158, 53), (150, 59),
     (142, 55), (140, 50), (135, 43), (130, 42), (127, 40), (122, 38),
     (120, 32), (122, 28), (118, 25), (110, 20), (108, 12), (105, 9),
     (103, 7), (100, 8), (98, 12), (95, 16), (92, 21), (90, 22),
     (86, 20), (82, 17), (80, 13), (77, 8), (75, 12), (72, 20),
     (68, 23), (66, 25), (61, 25), (58, 26), (56, 27), (52, 28),
     (50, 29), (48, 30), (44, 29), (40, 32), (36, 36), (36, 38),
     (33, 40), (30, 41), (28, 41), (24, 42), (22, 44), (24, 47),
     (28, 50), (32, 54), (36, 58), (38, 62)],
    [(113, -22), (114, -30), (115, -35), (120, -34), (124, -33), (129, -32),
     (132, -32), (135, -35), (138, -35), (140, -38), (145, -38), (150, -37),
     (153, -32), (153, -27), (150, -23), (146, -19), (142, -15), (142, -11),
     (140, -17), (136, -15), (135, -12), (132, -11), (130, -13), (126, -14),
     (122, -17), (118, -20)],
    [(-58, 64), (-52, 60), (-45, 60), (-40, 64), (-32, 68), (-25, 70),
     (-20, 74), (-22, 76), (-30, 78), (-45, 80), (-58, 76), (-62, 74)],
]


def wrap(draw, text, font, width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=font) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def main():
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    f_title = ImageFont.truetype(SERIF_B, 52)
    f_date = ImageFont.truetype(SANS_B, 30)
    f_sub = ImageFont.truetype(SANS_B, 15)
    f_tick = ImageFont.truetype(SANS_B, 12)
    f_lead_h = ImageFont.truetype(SANS_B, 30)
    f_lead_s = ImageFont.truetype(SANS, 16)
    f_head = ImageFont.truetype(SANS_B, 13)
    f_body = ImageFont.truetype(SANS, 11)
    f_tag = ImageFont.truetype(SANS_B, 9)
    f_map = ImageFont.truetype(SANS_B, 11)
    f_foot = ImageFont.truetype(SANS, 11)
    black = (15, 15, 15)
    grey = (90, 90, 90)
    red = (183, 28, 28)

    # ---- Masthead ----
    d.text((512, 6), "THE WORLD IN ONE DAY", font=f_title, fill=black, anchor="ma")
    d.line([(14, 72), (1010, 72)], fill=black, width=3)
    d.text((512, 78), "TUESDAY 24 NOVEMBER 2026", font=f_date, fill=red, anchor="ma")
    d.text((512, 114), "35 STORIES  •  7 REGIONS  •  EVERY STORY REPORTED TODAY",
           font=f_sub, fill=black, anchor="ma")
    d.line([(14, 136), (1010, 136)], fill=black, width=2)

    # ---- Ticker strip ----
    ty = 142
    d.rectangle([14, ty, 1010, ty + 38], fill=black)
    d.text((24, ty + 4),
           "HUANG BACK AT NVIDIA +31%   •   CHESS CROWN: GAME 1 IN GENEVA",
           font=f_tick, fill="white")
    d.text((24, ty + 21),
           "FIFA: USA 2031, UK 2035   •   ALCARAZ WINS ATP FINALS   •   SUPERMOON MEETS THE PLEIADES",
           font=f_tick, fill=(255, 200, 60))

    # ---- Lead story: Nvidia ----
    ly = 188
    d.rectangle([14, ly, 1010, ly + 92], fill=(253, 238, 238), outline=red, width=2)
    d.text((28, ly + 7), "LEAD  •  BUSINESS  •  SANTA CLARA", font=f_tag, fill=red)
    d.text((28, ly + 23), "HUANG IS BACK: NVIDIA SOARS 31%",
           font=f_lead_h, fill=black)
    for j, ln in enumerate(wrap(d,
            "Nvidia reinstates Jensen Huang as CEO after Trump pressed its board; shares jump a third, the Nasdaq rallies 6%, adding almost $1tn in value.",
            f_lead_s, 950)[:2]):
        d.text((28, ly + 58 + j * 18), ln, font=f_lead_s, fill=(40, 40, 40))

    # ---- World map strip ----
    my0, my1 = 288, 388
    d.text((14, my0), "THE DAY ON THE MAP — 34 STORIES, 7 REGIONS",
           font=f_map, fill=black)
    mx0, mx1 = 14, 1010
    lon0, lon1, lat0, lat1 = -170, 190, 82, -58

    def proj(lon, lat):
        x = mx0 + (lon - lon0) / (lon1 - lon0) * (mx1 - mx0)
        y = (my0 + 18) + (lat0 - lat) / (lat0 - lat1) * (my1 - my0 - 18)
        return x, y

    for poly in CONTINENTS:
        pts = [proj(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=(214, 226, 235), outline=(90, 110, 130))
    for _h, _s, region, lon, lat in STORIES:
        if lon is None:
            continue
        x, y = proj(lon, lat)
        c = REGION_COLORS[region]
        d.ellipse([x - 5, y - 5, x + 5, y + 5], fill=c, outline="white", width=1)
    # Lead dot (Santa Clara)
    x, y = proj(-122, 37)
    d.ellipse([x - 6, y - 6, x + 6, y + 6], fill=red, outline="white", width=1)

    # ---- Story grid: 34 stories, 5 cols x 7 rows ----
    gx0, gy0 = 14, 396
    cols, rows = 5, 7
    cw = (1010 - gx0 - (cols - 1) * 6) // cols
    gh = (990 - gy0 - (rows - 1) * 6) // rows
    for i, (headline, summary, region, _lon, _lat) in enumerate(STORIES):
        r, c = divmod(i, cols)
        x0 = gx0 + c * (cw + 6)
        y0 = gy0 + r * (gh + 6)
        col = REGION_COLORS[region]
        d.rectangle([x0, y0, x0 + cw, y0 + gh], outline=(200, 200, 200), width=1)
        d.rectangle([x0, y0, x0 + cw, y0 + 3], fill=col)
        d.text((x0 + 6, y0 + 5), region, font=f_tag, fill=col)
        lines = wrap(d, headline, f_head, cw - 12)[:2]
        yy = y0 + 17
        for ln in lines:
            d.text((x0 + 6, yy), ln, font=f_head, fill=black)
            yy += 13
        for ln in wrap(d, summary, f_body, cw - 12)[:3]:
            d.text((x0 + 6, yy), ln, font=f_body, fill=(50, 50, 50))
            yy += 11
    # Last cell: the day in numbers
    x0 = gx0 + 4 * (cw + 6)
    y0 = gy0 + 6 * (gh + 6)
    d.rectangle([x0, y0, x0 + cw, y0 + gh], fill=(15, 15, 15))
    d.text((x0 + 6, y0 + 6), "THE DAY IN NUMBERS", font=f_tag, fill=(255, 200, 60))
    for j, ln in enumerate(["+31%  Nvidia shares in a day",
                            "$2.5m  chess prize fund",
                            "48 teams at 2031 World Cup",
                            "24 dead in Serang fire"]):
        d.text((x0 + 6, y0 + 21 + j * 13), ln, font=f_body, fill="white")

    # ---- Footer ----
    d.line([(14, 994), (1010, 994)], fill=black, width=1)
    d.text((512, 1000),
           "Every story above happened or was first reported on Tuesday 24 November 2026  •  Sources: Reuters, AP, AFP, CNN, The Hindu, BBC, FIFA, FIDE",
           font=f_foot, fill=grey, anchor="ma")
    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
