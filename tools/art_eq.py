"""The equalizer's sheets."""
from parts import BOX, eq_thumb, lettered_button, letters, centred, level_colour, title_button, title_strip, well, window

NAME = "EQUALIZER"
GRAPH = (85, 16, 115, 21)  # the graph's well round its 113 x 19 picture at 86, 17
BANDS = [21] + [78 + 18 * i for i in range(10)]  # the preamp's and the bands' sliders, 14 x 63 from row 38
FREQUENCIES = ("PRE", "60", "170", "310", "600", "1K", "3K", "6K", "12K", "14K", "16K")
SCALE = (("+12", 39), ("0", 66), ("-12", 94))  # beside the preamp: text, top
TOGGLES = (("ON", 26, (10, 128, 69, 187)), ("AUTO", 32, (36, 154, 95, 213)))  # word, width, x: off, off pressed, on, on pressed
TOGGLE_Y = 119
FRAME_W, FRAME_H = 14, 63


def eq_window(p):
    window(p, 0, 0, 275, 116)
    title_strip(p, 0, 0, 275, NAME, True)
    well(p, *GRAPH)
    for x, text in zip(BANDS, FREQUENCIES):
        centred(p, text, x - 3, 104, FRAME_W + 6, "ink")
    for text, y in SCALE:
        letters(p, text, 58 - len(text) * 5, y, "ink")


RAILS = (4, 9)  # a slider's two rails, from its left
THUMB = 11
CAP = 3  # how far down (and up) a rail's end flares into its little triangle


def rails(x, y):
    """A slider's two glowing rails, each flaring at both ends into a small triangle, as one outline."""
    d = ""
    for r in RAILS:
        rx = x + r
        d += f"M{rx} {y + CAP}h1V{y + FRAME_H - CAP}h-1z"
        d += f"M{rx - 2} {y}h5v1h-1v1h-1v1h-1v-1h-1v-1h-1z"  # rows 5, 3 and 1 wide: a triangle in whole pixels
        d += f"M{rx - 2} {y + FRAME_H}h5v-1h-1v-1h-1v-1h-1v1h-1v1h-1z"
    return d


def slider_frame(p, x, y, k):
    """One frame of a band's slider, `k` from 0 at the bottom to 27 at the top: the rails, and between them
    under the thumb's middle the level, lit."""
    p.rect(x, y, FRAME_W, FRAME_H + 1, "body")
    middle = y + round((27 - k) * (FRAME_H - THUMB) / 27) + THUMB // 2
    left, right = RAILS
    p.rect(x + left + 1, middle, right - left - 1, y + FRAME_H - CAP - middle, "glow-mid")
    p.rect(x + left + 2, middle, right - left - 3, y + FRAME_H - CAP - middle, "glow-dim")
    p.path(rails(x, y), "glow")


def graph(p):
    """The graph's ground with its grid, the column of line colours beside it and the preamp's line."""
    p.rect(0, 294, 113, 19, "lcd")
    p.path("".join(f"M{1 + 12 * i} 294h1v19h-1z" for i in range(10)) + "M0 303h113v1h-113z", "glow-deep")
    for row in range(19):
        p.rect(115, 294 + row, 1, 1, level_colour(round(27 * (1 - row / 18))))
    p.rect(0, 314, 113, 1, "glow-mid")


def eqmain(p):
    p.rect(0, 0, 275, 315, "base")
    eq_window(p)
    title_button(p, 0, 116, "close")
    title_button(p, 0, 116 + BOX, "close", True)
    for word, w, xs in TOGGLES:
        for x, (on, pressed) in zip(xs, ((False, False), (False, True), (True, False), (True, True))):
            lettered_button(p, x, TOGGLE_Y, w, 12, word, pressed, on)
    title_strip(p, 0, 134, 275, NAME, True)
    title_strip(p, 0, 149, 275, NAME, False)
    for k in range(28):
        slider_frame(p, 13 + (k % 14) * 15, 164 + (k // 14) * 65, k)
    eq_thumb(p, 0, 164)
    eq_thumb(p, 0, 176, True)
    lettered_button(p, 224, 164, 44, 12, "PRESETS")
    lettered_button(p, 224, 176, 44, 12, "PRESETS", True)
    graph(p)


def eq_ex(p):
    """The shaded equalizer: its title strip, focused and not, and the pressed buttons."""
    p.rect(0, 0, 275, 82, "base")
    for y, focused in ((0, True), (15, False)):
        title_strip(p, 0, y, 275, NAME, focused, ("unshade", "close"), shaded=True)
    title_button(p, 1, 38, "unshade", True)
    title_button(p, 11, 38, "close", True)
