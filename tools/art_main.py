"""The main window's sheets."""
from parts import ink as ink_of
from parts import (BOX, CELL_H, button, centred, groove, letters, lettered_button, press, rule, thumb, title_button, title_strip,
                   strip_ground, well, window)

NAME = "POPAMP"

# --- main.svg ------------------------------------------------------------------------------------------

DISPLAY = (8, 20, 97, 43)  # the clock, the vis and the clutterbar
MARQUEE = (108, 22, 161, 17)
KBPS, KHZ = (108, 40, 22, 13), (153, 40, 17, 13)
MONOSTER = (210, 39, 59, 17)
LOGO = (249, 90, 17, 16)
RULES = (68, 85)  # the grooves above and below the position bar
COLON = (72, (30, 35))  # the clock's colon: x, rows


# The bolt of Popamp's logo (assets/logo/popamp.svg), in that drawing's units.
BOLT = ((117.57, 68.60), (151.46, 68.60), (128.00, 108.08), (158.91, 108.08), (108.26, 187.40), (124.28, 131.54), (97.09, 131.54))


def logo(p, x, y, w, h):
    """Popamp's lightning bolt, glowing on the panel, as tall as the place `w` x `h` and centred in it."""
    xs, ys = [px for px, _ in BOLT], [py for _, py in BOLT]
    scale = (h - 1) / (max(ys) - min(ys))
    left = x + (w - (max(xs) - min(xs)) * scale) / 2
    top = y + 0.5
    points = "L".join(f"{left + (px - min(xs)) * scale:.2f} {top + (py - min(ys)) * scale:.2f}" for px, py in BOLT)
    p.path(f"M{points}Z", "glow")


def main(p):
    window(p, 0, 0, 275, 116)
    title_strip(p, 0, 0, 275, NAME, True, ("min", "shade", "close"), menu=True)
    well(p, *DISPLAY)
    x, rows = COLON
    for y in rows:
        p.rect(x, y, 2, 2, "glow")
    for w in (MARQUEE, KBPS, KHZ, MONOSTER):
        well(p, *w)
    letters(p, "KBPS", KBPS[0] + KBPS[2] + 1, 43, "ink")
    letters(p, "KHZ", KHZ[0] + KHZ[2] + 1, 43, "ink")
    for y in RULES:
        rule(p, 8, y, 260)
    logo(p, *LOGO)


# --- cbuttons.svg: the transport ----------------------------------------------------------------------

TRANSPORT = (("previous", 0, 23), ("play", 23, 23), ("pause", 46, 23), ("stop", 69, 23), ("next", 92, 22))


def transport_glyph(name, x, y, h=8):
    """A transport sign `h` high as whole triangles, bars and squares, its top left at `x`, `y`; and its width."""
    t, d = h // 4, h - 1 - (8 - h) // 2  # a bar's thickness; a triangle's depth: 7 at 8 high, 4 at 6
    p = (h + 1) // 3  # a pause bar's width

    def right(x0):  # a triangle pointing right, its base at x0
        return f"M{x0} {y}L{x0 + d} {y + h // 2}L{x0} {y + h}Z"

    def left(x1):  # pointing left, its base at x1
        return f"M{x1} {y}L{x1 - d} {y + h // 2}L{x1} {y + h}Z"

    def bar(x0, w, y0=y, bh=h):
        return f"M{x0} {y0}h{w}v{bh}h{-w}z"

    e = h - t - 1  # eject's triangle's height
    shapes = {
        "previous": (bar(x, t) + left(x + t + 1 + d), t + 1 + d),
        "play": (right(x), d),
        "pause": (bar(x, p) + bar(x + h - p, p), h),
        "stop": (bar(x, h), h),
        "next": (right(x) + bar(x + d + 1, t), t + 1 + d),
        "eject": (f"M{x} {y + e}L{x + e} {y}L{x + 2 * e} {y + e}Z" + bar(x, 2 * e, y + e + 1, t), 2 * e),
    }
    return shapes[name]


def sign(p, name, x, y, w, h, size, ink="ink"):
    """A transport sign `size` high in the middle of the `w` x `h` box at `x`, `y`."""
    _, gw = transport_glyph(name, 0, 0, size)
    p.path(transport_glyph(name, x + (w - gw) // 2, y + (h - size) // 2, size)[0], ink)


def cbuttons(p):
    p.rect(0, 0, 136, 36, "base")
    for name, x, w in TRANSPORT:
        for y, pressed in ((0, False), (18, True)):
            button(p, x, y, w, 18, pressed)
            d = press(pressed)
            sign(p, name, x + d, y + d, w, 18, 8, ink_of(pressed))
    for y, pressed in ((0, False), (16, True)):
        button(p, 114, y, 22, 16, pressed)
        d = press(pressed)
        sign(p, "eject", 114 + d, y + d, 22, 16, 8, ink_of(pressed))


# --- shufrep.svg: repeat, shuffle, EQ and PL ----------------------------------------------------------

STATES = ((False, False), (False, True), (True, False), (True, True))  # off, off pressed, on, on pressed


def shufrep(p):
    p.rect(0, 0, 92, 85, "base")
    for row, (on, pressed) in enumerate(STATES):
        lettered_button(p, 0, 15 * row, 28, 15, "REP", pressed, on)
        lettered_button(p, 28, 15 * row, 47, 15, "SHUFFLE", pressed, on)
    for x0, pressed in ((0, False), (46, True)):
        for y, on in ((61, False), (73, True)):
            lettered_button(p, x0, y, 23, 12, "EQ", pressed, on)
            lettered_button(p, x0 + 23, y, 23, 12, "PL", pressed, on)


# --- titlebar.svg: the title strips, their buttons and the clutterbar ----------------------------------

X0 = 27  # the strips' left in the sheet
CLUTTER = "OAIDV"
CLUTTER_AT = (3, 11, 18, 25, 33)  # each letter's place down the bar
CLUTTER_LIT = ((304, 47, 8, 8), (312, 55, 8, 7), (320, 62, 8, 7), (328, 69, 8, 8), (336, 77, 8, 7))
SHADE_TIME = (127, 2, 31, 10)  # the shaded window's clock well, mini transport and position bar
SHADE_TRANSPORT = (167, 2, 59, 10)
SHADE_POS = (226, 4, 17, 7)


def loose_buttons(p):
    """The buttons the player lays over the strips: normal in the top row, pressed below."""
    for x, y, glyph in ((0, 0, "menu"), (9, 0, "min"), (18, 0, "close")):
        title_button(p, x, y, glyph)
        title_button(p, x, y + BOX, glyph, True)
    for y, glyph in ((18, "shade"), (27, "unshade")):
        title_button(p, 0, y, glyph)
        title_button(p, 9, y, glyph, True)
    shade_pos(p, 0, 36)
    thumb(p, 20, 36, 3, 7)


def shade_pos(p, x, y):
    """The shaded window's little position bar: a grey groove."""
    p.rect(x, y, 17, 7, "body")
    groove(p, x, y + 2, 17)


def mini_transport(p, x, y, w, h, eject=True):
    """The small transport signs in a well, 6 high, one to every 9 pixels: previous, play, pause, stop, next, eject."""
    well(p, x, y, w, h)
    signs = ("previous", "play", "pause", "stop", "next") + (("eject",) if eject else ())
    x0 = x + (w - 9 * len(signs)) // 2
    for i, name in enumerate(signs):
        sign(p, name, x0 + 9 * i, y, 9, h, 6)


def shade_strip(p, y, focused):
    strip_ground(p, X0, y, 275, left=True, right=True, bottom=True)
    title_button(p, X0 + 6, y + 3, "menu")
    letters(p, NAME, X0 + 20, y + 4, "ink" if focused else "ink-dim")
    well(p, X0 + SHADE_TIME[0], y + SHADE_TIME[1], *SHADE_TIME[2:])
    p.rect(X0 + 144, y + 5, 1, 1, "glow")
    p.rect(X0 + 144, y + 7, 1, 1, "glow")
    mini_transport(p, X0 + SHADE_TRANSPORT[0], y + SHADE_TRANSPORT[1], *SHADE_TRANSPORT[2:])
    shade_pos(p, X0 + SHADE_POS[0], y + SHADE_POS[1])
    for x, glyph in ((244, "min"), (254, "unshade"), (264, "close")):
        title_button(p, X0 + x, y + 3, glyph)


def clutter_letter(p, x, y, i, lit):
    centred(p, CLUTTER[i], x, y, 8, "ink" if lit else "ink-dim")


def clutterbar(p):
    p.rect(304, 0, 8, 43, "lcd")
    for i, at in enumerate(CLUTTER_AT):
        clutter_letter(p, 304, at + (7 - CELL_H) // 2, i, False)
    for i, (x, y, w, h) in enumerate(CLUTTER_LIT):
        p.rect(x, y, w, h, "lcd")
        clutter_letter(p, x, y + (h - CELL_H) // 2, i, True)


def titlebar(p):
    p.rect(0, 0, 344, 87, "base")
    loose_buttons(p)
    for y, focused in ((0, True), (15, False), (57, True), (72, False)):  # the last two: the classic sheet's spare pair
        title_strip(p, X0, y, 275, NAME, focused, ("min", "shade", "close"), menu=True)
    shade_strip(p, 29, True)
    shade_strip(p, 42, False)
    clutterbar(p)


# --- the sliders ---------------------------------------------------------------------------------------


def posbar(p):
    p.rect(0, 0, 307, 10, "body")
    groove(p, 0, 4, 248)
    thumb(p, 248, 0, 29, 10)
    thumb(p, 278, 0, 29, 10, True)


FRAMES, STEP = 28, 15


def track(p, x, y, w, h=13):
    """One frame of the volume or balance track: a grey groove across its middle, the same at every level."""
    p.rect(x, y, w, h, "body")
    groove(p, x, y + (h - 3) // 2 + 1, w)


def slider_sheet(p, x, w):
    p.rect(0, 0, 68, 433, "base")
    for k in range(FRAMES):
        track(p, x, STEP * k, w)
    thumb(p, 15, 422, 14, 11, left=True)
    thumb(p, 0, 422, 14, 11, True, left=True)


def volume(p):
    slider_sheet(p, 0, 68)


def balance(p):
    slider_sheet(p, 9, 38)


# --- the display's indicators --------------------------------------------------------------------------


def monoster(p):
    p.rect(0, 0, 58, 24, "lcd")
    for y, lit in ((0, True), (12, False)):
        ink = "ink" if lit else "ink-dim"
        centred(p, "STEREO", 0, y + 3, 29, ink)
        centred(p, "MONO", 29, y + 3, 27, ink)


def playpaus(p):
    p.rect(0, 0, 42, 9, "lcd")
    p.path("M2 1L7 4.5L2 8Z", "glow")
    p.path("M11 1h2v7h-2zM14 1h2v7h-2z", "glow-light")
    p.rect(20, 2, 5, 5, "glow-mid")
    p.rect(36, 0, 3, 9, "lcd")
    p.rect(40, 2, 1, 5, "glow")
