"""The media library's own pictures: the display under its title, the panel under its list and the title's
right end with Maximize.

The display lies across the window from the title's lower part to the list's top rim: one well with the play
state, the clock, the song title and the bit rate at its left, and the visualizer filling the rest. The panel
under the list has the position bar across the whole window and under it the status, the transport in the
middle, the volume and the LIST button. Both are a left end, a tiled middle and a right end, so the wells run
on across the pieces. windows.py lays their controls out.
"""
from art_bar import COLON_ROWS, COLON_X
from art_pl import BOTTOM, PIECE_W, bottom_ground, grip, top_right
from parts import TITLE_H, letters, lettered_button, title_button, well

MARGIN, RIGHT_MARGIN = 11, 6  # the wells from the window's left, and to its right

# --- the display --------------------------------------------------------------------------------------

STRIP_TOP, STRIP_H = TITLE_H, 49
LIST_TOP = STRIP_TOP + STRIP_H  # where the list starts, under the strip's last row: the list's top rim
DISPLAY_TOP, DISPLAY_H = 2, 44  # the well, in the strip
STRIP_LEFT, STRIP_RIGHT, TILE = 220, 16, 8
# The left block in the well, in the window: the clock's corner, the song title's row, the bit rate's row
CLOCK = (MARGIN + 10, STRIP_TOP + DISPLAY_TOP + 4)
TITLE_ROW = STRIP_TOP + DISPLAY_TOP + 20
RATE_ROW = STRIP_TOP + DISPLAY_TOP + 33
INFO_W = 196  # the left block's width from the well's left; the visualizer starts after it
VIS_X = MARGIN + INFO_W + 4
VIS_INSET = 3  # the visualizer inside the well, at its top, bottom and right
KBPS_X, KHZ_X = MARGIN + 4, MARGIN + 56  # the numbers; their words follow them


def ground(p, w, left=False, right=False):
    """A strip piece's panel, the window's edges at its ends and the list's top rim along its last row."""
    p.rect(0, 0, w, STRIP_H, "body")
    if left:
        p.rect(0, 0, 1, STRIP_H, "glow")
        p.rect(MARGIN, STRIP_H - 1, w - MARGIN, 1, "glow-dim")
    elif right:
        p.rect(w - 1, 0, 1, STRIP_H, "glow")
        p.rect(0, STRIP_H - 1, w - RIGHT_MARGIN, 1, "glow-dim")
    else:
        p.rect(0, STRIP_H - 1, w, 1, "glow-dim")


def run(p, x, y, w, h, piece_w, left=False, right=False):
    """A well from `x` across `w` that goes on into the next piece where it is open: its rim there lies past
    the picture's edge, which cuts it off."""
    x0 = x if left else -1
    x1 = x + w if right else piece_w + 1
    well(p, x0, y, x1 - x0, h)


def strip_left(p):
    w = STRIP_LEFT
    ground(p, w, left=True)
    run(p, MARGIN, DISPLAY_TOP, w - MARGIN, DISPLAY_H, w, left=True)
    cx, cy = CLOCK
    for y in COLON_ROWS:
        p.rect(cx + COLON_X, cy - STRIP_TOP + y, 2, 2, "glow")
    row = RATE_ROW - STRIP_TOP
    letters(p, "KBPS", KBPS_X + 20, row, "glow-mid")
    letters(p, "KHZ", KHZ_X + 15, row, "glow-mid")
    # a line between the song's block and the visualizer
    p.rect(VIS_X - 3, DISPLAY_TOP + 3, 1, DISPLAY_H - 6, "glow-dim")


def strip_mid(p):
    ground(p, TILE)
    run(p, 0, DISPLAY_TOP, TILE, DISPLAY_H, TILE)


def strip_right(p):
    w = STRIP_RIGHT
    ground(p, w, right=True)
    run(p, 0, DISPLAY_TOP, w - RIGHT_MARGIN, DISPLAY_H, w, right=True)


# --- the panel under the list -----------------------------------------------------------------------------

# Rows in the panel: the position bar's groove (a well 4 high, the thumb 10 across it), the buttons' row
GROOVE_TOP, GROOVE_H, SEEK_TOP = 5, 4, 2
BUTTONS_TOP = 16
BOTTOM_LEFT, BOTTOM_RIGHT = 130, 120
STATUS = (MARGIN, BUTTONS_TOP + 3, 110, 12)  # the status well: x, y, w, h in the left end
LIST_BUTTON = (BOTTOM_RIGHT - 42, BUTTONS_TOP, 22, 18)  # in the right end, clear of the resize grip
TRANSPORT_W = 113 + 3 + 22  # Previous to Next, a gap and Open


def groove(p, x0, x1, piece_w, left=False, right=False):
    run(p, x0, GROOVE_TOP, x1 - x0, GROOVE_H, piece_w, left, right)
    a, b = (x0 + 1 if left else 0), (x1 - 1 if right else piece_w)
    p.rect(a, GROOVE_TOP + 1, b - a, GROOVE_H - 2, "glow-dim")


def bottom_left(p):
    w = BOTTOM_LEFT
    bottom_ground(p, 0, 0, w, left=True)
    p.rect(1, 0, MARGIN - 1, 1, "body")  # the rim starts under the list
    groove(p, MARGIN, w, w, left=True)
    well(p, *STATUS)


def bottom_mid(p):
    bottom_ground(p, 0, 0, TILE)
    groove(p, 0, TILE, TILE)


def bottom_right(p):
    w = BOTTOM_RIGHT
    bottom_ground(p, 0, 0, w, right=True)
    scroll_end = w - 20 + 4  # the list's scroll groove closes on the rim
    p.rect(scroll_end, 0, 1, 1, "glow-dim")
    p.rect(scroll_end + 1, 0, 8, 1, "glow-dim")
    groove(p, 0, w - RIGHT_MARGIN, w, right=True)
    x, y, bw, bh = LIST_BUTTON
    lettered_button(p, x, y, bw, bh, "LIST")
    grip(p, w - 3, BOTTOM - 3)


# --- the title's right end: Maximize and Close, focused at row 0, not at row 21; Maximize pressed at row 42

TITLE_RIGHT_H = 51


def title_right(p):
    for y, focused in ((0, True), (21, False)):
        top_right(p, y, focused, x=0, glyph="max")
    title_button(p, 0, 42, "max", True)


PICTURES = {
    "strip-left": (STRIP_LEFT, STRIP_H, strip_left),
    "strip-mid": (TILE, STRIP_H, strip_mid),
    "strip-right": (STRIP_RIGHT, STRIP_H, strip_right),
    "bottom-left": (BOTTOM_LEFT, BOTTOM, bottom_left),
    "bottom-mid": (TILE, BOTTOM, bottom_mid),
    "bottom-right": (BOTTOM_RIGHT, BOTTOM, bottom_right),
    "title-right": (PIECE_W, TITLE_RIGHT_H, title_right),
}
