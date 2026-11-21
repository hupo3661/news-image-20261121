#!/usr/bin/env python3
"""Render the world-news infographic for Saturday 21 November 2026.

Draws a 1024x1024 broadsheet-style front page with PIL and saves it
as entry.png next to this script. Every word is rendered as real
text; every icon is a shape drawn by the code. No network, no clock,
no randomness, so the output bytes are identical on every run.

Layout (cream paper, red accent, ink text):
  red top bar, masthead with the date, a full-width lead panel for
  the Peru earthquake with a drawn seismograph trace, five ruled
  story rows underneath, and a sources footer.
"""

import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (251, 247, 239)
INK = (26, 26, 26)
GREY = (96, 90, 82)
RED = (178, 38, 30)
RED_TINT = (250, 235, 230)
HAIRLINE = (205, 196, 182)
CHIP_BG = (178, 38, 30)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
PLAIN = os.path.join(FONT_DIR, "DejaVuSans.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Split text into lines that fit max_w pixels."""
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def tracked(draw, xy, text, fnt, fill, spacing=3):
    """Draw text with extra letter spacing (for kickers and tags)."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + spacing
    return x


class Page:
    """A thin wrapper around an ImageDraw with layout helpers."""

    def __init__(self):
        self.img = Image.new("RGB", (W, H), PAPER)
        self.d = ImageDraw.Draw(self.img)

    def rule(self, y, x0=48, x1=976, fill=HAIRLINE, width=1):
        self.d.line([(x0, y), (x1, y)], fill=fill, width=width)

    def chip(self, x, y, label):
        fnt = font(BOLD, 19)
        pad_x, pad_y = 12, 7
        tw = self.d.textlength(label, font=fnt)
        self.d.rounded_rectangle(
            [x, y, x + tw + 2 * pad_x, y + 34], radius=4, fill=CHIP_BG
        )
        self.d.text((x + pad_x, y + pad_y), label, font=fnt, fill=(255, 255, 255))

    def headline(self, x, y, text, size, max_w, leading=None):
        fnt = font(BOLD, size)
        lines = wrap(self.d, text, fnt, max_w)
        leading = leading or int(size * 1.22)
        for line in lines:
            self.d.text((x, y), line, font=fnt, fill=INK)
            y += leading
        return y

    def body(self, x, y, text, size, max_w, fill=GREY, leading=None):
        fnt = font(PLAIN, size)
        lines = wrap(self.d, text, fnt, max_w)
        leading = leading or int(size * 1.35)
        for line in lines:
            self.d.text((x, y), line, font=fnt, fill=fill)
            y += leading
        return y

    def quake_trace(self, x, y, w, h, colour=RED):
        """A seismograph squiggle: flat, then a burst, then settling."""
        mid = y + h // 2
        pts = []
        for i in range(w + 1):
            t = i / w
            if t < 0.18 or t > 0.82:
                amp = 2
            elif t < 0.30:
                amp = 10 + (t - 0.18) / 0.12 * 26
            elif t < 0.62:
                amp = 36 + 14 * math.sin(t * 40)
            else:
                amp = 36 * (1 - (t - 0.62) / 0.20)
            pts.append((x + i, mid + amp * math.sin(i * 0.55)))
        self.d.line(pts, fill=colour, width=3)
        self.d.line([(x, mid), (x + w, mid)], fill=(214, 196, 188), width=1)

    def number_disc(self, x, y, n):
        self.d.ellipse([x, y, x + 44, y + 44], outline=RED, width=3)
        fnt = font(BOLD, 22)
        label = str(n)
        tw = self.d.textlength(label, font=fnt)
        self.d.text((x + 22 - tw / 2, y + 9), label, font=fnt, fill=RED)


LEAD = {
    "tag": "EARTHQUAKE  •  PERU",
    "headline": "Magnitude 6.8 quake shakes central Peru",
    "summary": (
        "The tremor struck the Andean region of Junin and was felt in "
        "Lima, sending residents into the streets. No immediate "
        "casualties or major damage were reported."
    ),
    "big": "6.8",
    "big_label": "MAGNITUDE",
}

ROWS = [
    {
        "tag": "COURT  •  THE HAGUE",
        "headline": "ICJ: Myanmar committed genocide against the Rohingya",
        "summary": "Landmark judgment finds Myanmar responsible for genocidal acts against the Rohingya.",
    },
    {
        "tag": "WAR  •  UKRAINE / POLAND",
        "headline": "Russian missile lands in Poland amid Ukraine strikes",
        "summary": "It came down as Russia fired about 100 missiles at Ukraine while Kyiv's allies held drills.",
    },
    {
        "tag": "DIPLOMACY  •  LONDON / BRUSSELS",
        "headline": "UK and EU strike landmark post-Brexit reset deal",
        "summary": "The deal resets the post-Brexit relationship; London now seeks even closer ties.",
    },
    {
        "tag": "MARKETS  •  TECH",
        "headline": "Tech sell-off drags markets down as Anthropic slides",
        "summary": "Shares fell a day after the AI firm's record $81.3bn debut, pulling tech lower.",
    },
    {
        "tag": "JUSTICE  •  NEW YORK",
        "headline": "US court jails Nikhil Gupta for 235 months",
        "summary": "He was sentenced for a murder-for-hire plot against a Sikh separatist on US soil.",
    },
]


def build():
    page = Page()
    d = page.d

    # --- top bar + masthead -------------------------------------------
    d.rectangle([0, 0, W, 8], fill=RED)
    tracked(d, (48, 32), "THE WORLD IN ONE IMAGE", font(BOLD, 21), RED, spacing=4)
    d.text((48, 62), "Saturday, 21 November 2026",
           font=font(BOLD, 46), fill=INK)
    d.text((48, 118), "Six stories from around the world — as reported today",
           font=font(PLAIN, 20), fill=GREY)
    page.rule(150, width=2)

    # --- lead panel: Peru earthquake ----------------------------------
    lx, ly, lw, lh = 48, 170, 928, 238
    d.rectangle([lx, ly, lx + lw, ly + lh], fill=RED_TINT)
    d.rectangle([lx, ly, lx + 7, ly + lh], fill=RED)
    page.chip(lx + 28, ly + 20, LEAD["tag"])
    page.headline(lx + 28, ly + 68, LEAD["headline"], 33, 560)
    page.body(lx + 28, ly + 152, LEAD["summary"], 20, 560)
    # magnitude + trace on the right of the panel
    big = font(BOLD, 74)
    d.text((lx + 640, ly + 26), LEAD["big"], font=big, fill=RED)
    tracked(d, (lx + 646, ly + 112), LEAD["big_label"], font(BOLD, 17), RED)
    page.quake_trace(lx + 620, ly + 158, 280, 58)

    # --- five ruled story rows ----------------------------------------
    y = 432
    for i, row in enumerate(ROWS, start=2):
        page.number_disc(48, y + 6, i)
        tracked(d, (112, y), row["tag"], font(BOLD, 16), RED, spacing=2)
        page.headline(112, y + 26, row["headline"], 25, 864)
        page.body(112, y + 60, row["summary"], 19, 864)
        y += 98
        if i < 6:
            page.rule(y - 8)

    # --- footer --------------------------------------------------------
    page.rule(928, width=2)
    d.text((48, 944),
           "All six events happened, or were first reported, on Saturday 21 November 2026.",
           font=font(BOLD, 17), fill=INK)
    d.text((48, 972),
           "Sources: Reuters (Peru quake; ICJ ruling; Poland missile)  •  BBC (UK–EU deal; tech sell-off)  •  The Hindu (Gupta sentence)",
           font=font(PLAIN, 15), fill=GREY)
    d.text((48, 994),
           "Drawn programmatically — every word is rendered text, every icon a drawn shape.",
           font=font(PLAIN, 15), fill=GREY)

    return page.img


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "entry.png")
    img = build()
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
