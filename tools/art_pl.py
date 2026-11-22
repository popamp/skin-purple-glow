"""The playlist's sheet, and the library's title in the same pieces.

The playlist's frame is cut in pieces the player tiles, so the title strip
is drawn piece by piece with the same parts the other windows use whole.
"""
from parts import (RIGHT_BUTTONS, TITLE_H, button, centred, lettered_button, strip_ground, thumb, title_button, title_name,
                   well)
from art_main import mini_transport

NAME = "PLAYLIST"
TOP_H = 20  # the top pieces: the title strip and the panel above the list
LIST_TOP = 19  # the list's well: its top rim's row in the top pieces
# The pieces: x in the sheet, focused at row 0, not at row 21
TOP_LEFT, PLATE, TOP_TILE, TOP_RIGHT = 0, 26, 127, 153
PLATE_W, PIECE_W = 100, 25
# Bottom pieces (38 high) and the menu buttons
BOTTOM = 38
MENU_WORDS = (
    (0, (("ADD", "URL"), ("ADD", "DIR"), ("ADD", "FILE"))),
    (54, (("REM", "ALL"), ("CROP", ""), ("REM", "SEL"), ("REM", "MISC"))),
    (104, (("INV", "SEL"), ("SEL", "ZERO"), ("SEL", "ALL"))),
    (154, (("SORT", "LIST"), ("FILE", "INFO"), ("MISC", "OPTS"))),
    (204, (("NEW", "LIST"), ("SAVE", "LIST"), ("LOAD", "LIST"))),
)
MENU_BARS = ((48, 54), (100, 72), (150, 54), (200, 54), (250, 54))
BUTTONS = (("ADD", 14), ("REM", 43), ("SEL", 72), ("MISC", 101))  # at row 8 of the bottom left


def panel_rows(p, x, y, w):
    """The panel between the title strip and the list."""
    p.rect(x, y + TITLE_H, w, TOP_H - TITLE_H, "body")


def top_left(p, y, focused):
    strip_ground(p, 0, y, PIECE_W, focused, left=True)
    panel_rows(p, 0, y, PIECE_W)
    p.rect(0, y + TITLE_H, 1, TOP_H - TITLE_H, "glow")
    p.rect(11, y + LIST_TOP, PIECE_W - 11, 1, "glow-dim")


def plate(p, x, y, focused, name):
    """The plate the window's name is on, in the middle of the strip."""
    strip_ground(p, x, y, PLATE_W, focused)
    title_name(p, name, x, x + PLATE_W, y, focused)
    panel_rows(p, x, y, PLATE_W)
    p.rect(x, y + LIST_TOP, PLATE_W, 1, "glow-dim")


def top_tile(p, y, focused):
    strip_ground(p, TOP_TILE, y, PIECE_W, focused)
    panel_rows(p, TOP_TILE, y, PIECE_W)
    p.rect(TOP_TILE, y + LIST_TOP, PIECE_W, 1, "glow-dim")


def top_right(p, y, focused):
    x = TOP_RIGHT
    strip_ground(p, x, y, PIECE_W, focused, right=True)
    title_button(p, x + PIECE_W - 20, y + 3, "shade")
    title_button(p, x + PIECE_W - 11, y + 3, "close")
    panel_rows(p, x, y, PIECE_W)
    p.rect(x + PIECE_W - 1, y + TITLE_H, 1, TOP_H - TITLE_H, "glow")
    p.rect(x, y + LIST_TOP, 6, 1, "glow-dim")
    p.rect(x + 9, y + LIST_TOP, 10, 1, "glow-dim")


def left_tile(p):
    p.rect(0, 42, 12, 29, "body")
    p.rect(0, 42, 1, 29, "glow")
    p.rect(11, 42, 1, 29, "glow-dim")


def scroll_groove(p, x, y, h):
    """The scroll bar's groove beside the list: a well without ends, as it is tiled."""
    p.rect(x, y, 1, h, "glow-dim")
    p.rect(x + 1, y, 8, h, "lcd")
    p.rect(x + 9, y, 1, h, "glow-dim")


def right_tile(p):
    p.rect(31, 42, 20, 29, "body")
    p.rect(31, 42, 1, 29, "glow-dim")
    scroll_groove(p, 35, 42, 29)
    p.rect(50, 42, 1, 29, "glow")


def bottom_ground(p, x, y, w, left=False, right=False):
    """A bottom piece's panel: the list's lower rim along its top, the window's edge along its bottom."""
    p.rect(x, y, w, BOTTOM, "body")
    p.rect(x, y, w, 1, "glow-dim")
    p.rect(x, y + BOTTOM - 1, w, 1, "glow")
    if left:
        p.rect(x, y, 1, BOTTOM - 1, "glow")
    if right:
        p.rect(x + w - 1, y, 1, BOTTOM, "glow")


def bottom_left(p):
    bottom_ground(p, 0, 72, 125, left=True)
    p.rect(1, 72, 10, 1, "body")  # the rim starts under the list
    p.rect(11, 72, 1, 1, "glow-dim")
    for word, x in BUTTONS:
        lettered_button(p, x, 80, 22, 18, word)


def grip(p, x, y):
    """The resize grip: a triangle of dots whose corner is at `x`, `y`, the window's bottom right inside its edge."""
    d = "".join(f"M{x - 3 * a} {y - 3 * b}h1v1h-1z" for a in range(4) for b in range(4 - a))
    p.path(d, "glow")


def bottom_right(p):
    x0, y0 = 126, 72
    bottom_ground(p, x0, y0, 150, right=True)
    scroll_end = x0 + 150 - 20 + 4
    p.rect(scroll_end, y0, 1, 1, "glow-dim")
    p.rect(scroll_end + 1, y0, 8, 1, "glow-dim")
    well(p, x0 + 4, y0 + 8, 92, 10)
    well(p, x0 + 4, y0 + 21, 57, 12)
    mini_transport(p, x0 + 4, y0 + 21, 57, 12)
    well(p, x0 + 65, y0 + 21, 36, 12)
    p.rect(x0 + 84, y0 + 25, 1, 1, "glow")
    p.rect(x0 + 84, y0 + 27, 1, 1, "glow")
    lettered_button(p, x0 + 106, y0 + 8, 22, 18, "LIST")
    grip(p, x0 + 150 - 3, y0 + BOTTOM - 3)


def bottom_tile(p):
    bottom_ground(p, 179, 0, 25)


def vis_piece(p):
    bottom_ground(p, 205, 0, 75)
    well(p, 207, 9, 73, 20)


def shade_pieces(p):
    """The shaded playlist: the left end at 72, 42, the tile under it, the right end with its buttons, focused at row 42, not at 57."""
    strip_ground(p, 72, 42, 25, True, left=True, bottom=True)
    strip_ground(p, 72, 57, 25, True, bottom=True)  # the tile between them
    for y, focused in ((42, True), (57, False)):
        strip_ground(p, 99, y, 50, focused, right=True, bottom=True)
        title_button(p, 99 + 50 - 21, y + 3, "unshade")
        title_button(p, 99 + 50 - 11, y + 3, "close")


def menu_item(p, x, y, words, pressed):
    button(p, x, y, 22, 18, pressed)
    d = 1 if pressed else 0
    ink = "glow-mid" if pressed else "glow"
    top, bottom = words
    if not bottom:
        centred(p, top, x + d, y + 6 + d, 22, ink)
        return
    centred(p, top, x + d, y + 2 + d, 22, ink)
    centred(p, bottom, x + d, y + 10 + d, 22, ink)


def menus(p):
    for x, items in MENU_WORDS:
        for i, words in enumerate(items):
            for dx, pressed in ((0, False), (23, True)):
                menu_item(p, x + dx, 111 + 19 * i, words, pressed)
    for x, h in MENU_BARS:
        p.rect(x, 111, 3, h, "glow")
        p.rect(x + 2, 111, 1, h, "glow-dim")


def pledit(p):
    p.rect(0, 0, 280, 186, "base")
    for y, focused in ((0, True), (21, False)):
        top_left(p, y, focused)
        plate(p, PLATE, y, focused, NAME)
        top_tile(p, y, focused)
        top_right(p, y, focused)
    left_tile(p)
    right_tile(p)
    title_button(p, 52, 42, "close", True)
    title_button(p, 62, 42, "shade", True)
    thumb(p, 52, 53, 8, 18, grip="h")
    thumb(p, 61, 53, 8, 18, True, grip="h")
    shade_pieces(p)
    bottom_left(p)
    bottom_right(p)
    bottom_tile(p)
    vis_piece(p)
    menus(p)


# --- the library's title, on the playlist's plate -----------------------------------------------------

LIBRARY = "MEDIA LIBRARY"


def ml_title(p):
    for y, focused in ((0, True), (21, False)):
        plate(p, 0, y, focused, LIBRARY)
