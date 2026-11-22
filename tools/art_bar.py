"""The bar view's own pictures: a strip of the main window's panel with the display's well along it, and its
controls of an even height.

The bar is 22 high, so only what is an even number of pixels high sits in its middle. The transport, Open, EQ
and PL buttons are the main window's own sprites; Main Menu and Close, Shuffle and Repeat and the volume are
drawn here again from the same parts, a pixel taller or shorter. windows.py lays them out.
"""
from art_main import FRAMES, STATES, track
from parts import lettered_button, thumb, title_button, well

BAR_H = 22
# The bar's fixed ends (the middle, the title's, is tiled) and the narrowest bar
BAR_LEFT, BAR_RIGHT, BAR_MIN = 318, 226, 640
# The display's well from its left, across the middle into the right end's first WELL_END pixels
DISPLAY_X, WELL_END = 161, 4
WELL_TOP, WELL_H = 1, BAR_H - 2
# The clock's left (its minus sign's place, the digits after it) and its colon
CLOCK = (171, 4)
COLON_X, COLON_ROWS = 36, (4, 9)
# The position bar's whole thumb under the title, on its groove's row
THUMB_TOP, GROOVE_ROW = 10, 5


def display(p, x, w, left=False, right=False):
    """The display's well across `x`..`x + w`, open where it goes on into the next piece: its rim there lies
    past the picture's edge, which cuts it off."""
    well(p, x - (0 if left else 1), WELL_TOP, w + (0 if left else 1) + (0 if right else 1), WELL_H)


def panel(p, w):
    """The bar's panel: flat, without the window's edge, as it lies along the screen's."""
    p.rect(0, 0, w, BAR_H, "body")


def left(p):
    panel(p, BAR_LEFT)
    display(p, DISPLAY_X, BAR_LEFT - DISPLAY_X, left=True)
    cx, cy = CLOCK
    for y in COLON_ROWS:
        p.rect(cx + COLON_X, cy + y, 2, 2, "glow")


def mid(p):
    panel(p, 8)
    display(p, 0, 8)
    p.rect(0, THUMB_TOP + GROOVE_ROW - 1, 8, 2, "glow-dim")


def right(p):
    panel(p, BAR_RIGHT)
    display(p, 0, WELL_END, right=True)


# controls.svg: Main Menu and Close, normal over pressed; Shuffle and Repeat in their four states; the volume
BOX = 12
TOGGLE_H, SHUFFLE, REPEAT = 16, (2 * BOX, 47), (2 * BOX + 47, 28)
VOLUME_W, VOLUME_H, VOLUME_WELL = 68, 14, 4
VOLUME_TOP = len(STATES) * TOGGLE_H
VOLUME_THUMB = (VOLUME_TOP + FRAMES * VOLUME_H, 14, 12)  # its row, width and height: normal at 15, pressed at 0
CONTROLS_W = REPEAT[0] + REPEAT[1]


def controls(p):
    p.rect(0, 0, CONTROLS_W, VOLUME_THUMB[0] + VOLUME_THUMB[2], "base")
    for x, glyph in ((0, "menu"), (BOX, "close")):
        title_button(p, x, 0, glyph, size=BOX)
        title_button(p, x, BOX, glyph, True, size=BOX)
    for row, (on, pressed) in enumerate(STATES):
        for (x, w), word in ((SHUFFLE, "SHUFFLE"), (REPEAT, "REP")):
            lettered_button(p, x, TOGGLE_H * row, w, TOGGLE_H, word, pressed, on)
    for k in range(FRAMES):
        track(p, 0, VOLUME_TOP + VOLUME_H * k, VOLUME_W, k, h=VOLUME_H, well_h=VOLUME_WELL)
    y, w, h = VOLUME_THUMB
    thumb(p, 15, y, w, h)
    thumb(p, 0, y, w, h, True)


PICTURES = {"left": (BAR_LEFT, BAR_H, left), "mid": (8, BAR_H, mid), "right": (BAR_RIGHT, BAR_H, right),
            "controls": (CONTROLS_W, VOLUME_THUMB[0] + VOLUME_THUMB[2], controls)}  # fmt: skip
