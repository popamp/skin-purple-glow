"""The parts every window is made of, each drawn here once: the window, its title strip and title buttons,
the wells, the buttons, lamps, thumbs and the lettering.

Everything is a thin glowing outline on black, as in the Winamp skin Purple Glow v2: a frame is one path,
a face one gradient.
"""
import os
import re

from kit import Gradient

# --- lettering: text.svg's letters, 5 x 6 cells -------------------------------------------------------

CELL_W, CELL_H = 5, 6
ROWS = ('ABCDEFGHIJKLMNOPQRSTUVWXYZ"@', "0123456789….:()-'!_+\\/[]^&%,=$#")
TEXT_SVG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "text.svg")


def moved(piece, dx, dy):
    """An outline of M, H and V steps moved by `dx`, `dy`."""

    def step(m):
        op, a, b = m.group(1), int(m.group(2)), m.group(3)
        if op == "M":
            return f"M{a + dx} {int(b) + dy}"
        return f"{op}{a + (dx if op == 'H' else dy)}"

    return re.sub(r"([MHV])(-?\d+)(?: (-?\d+))?", step, piece)


def load_font(path=TEXT_SVG):
    """text.svg's letters, each as its outline's pieces moved to the cell's corner."""
    with open(path, encoding="utf-8") as f:
        d = re.search(r'<path d="([^"]*)"', f.read()).group(1)
    letters = {}
    for piece in re.findall(r"M[^M]*", d):
        x, y = (int(v) for v in re.match(r"M(\d+) (\d+)", piece).groups())
        row, col = y // CELL_H, x // CELL_W
        if row < len(ROWS) and col < len(ROWS[row]):
            letters.setdefault(ROWS[row][col], []).append(moved(piece, -col * CELL_W, -row * CELL_H))
    return letters


FONT = load_font()


def text_width(text):
    return len(text) * CELL_W - 1


def letters(p, text, x, y, paint):
    """`text` in the skin's letters, its top left corner at `x`, `y`."""
    p.path("".join(moved(piece, x + i * CELL_W, y) for i, ch in enumerate(text) for piece in FONT.get(ch, ())), paint)


def centred(p, text, x, y, w, paint):
    letters(p, text, x + (w - text_width(text)) // 2, y, paint)


# --- frames and wells ---------------------------------------------------------------------------------


def frame(p, x, y, w, h, paint):
    """A one-pixel outline round the `w` x `h` box, as one path."""
    p.path(f"M{x} {y}h{w}v{h}h{-w}zM{x + 1} {y + 1}v{h - 2}h{w - 2}v{2 - h}z", paint)


def well(p, x, y, w, h, inside="lcd"):
    """A dark place in the panel: the display, a text, a groove, framed in dim glow."""
    p.rect(x, y, w, h, inside)
    frame(p, x, y, w, h, "glow-dim")


def rule(p, x, y, w):
    """A thin line across the panel."""
    p.rect(x, y, w, 1, "glow-dim")


def window(p, x, y, w, h):
    """A window's panel, its glowing edge and a dim line inside it."""
    p.rect(x, y, w, h, "body")
    frame(p, x, y, w, h, "glow")
    frame(p, x + 2, y + 2, w - 4, h - 4, "glow-deep")


# --- buttons -----------------------------------------------------------------------------------------

RAISED, SUNK = Gradient("glow-deep", "body"), Gradient("glow-dim", "glow-deep")


def button(p, x, y, w, h, pressed=False):
    """A rounded button a pixel inside its place, with a soft glow round it in that pixel; pressed, it lights up.
    A title button is too small for the glow and the margin: they would cover its sign."""
    big = min(w, h) >= 12
    r, m = (2.5, 1) if big else (1.5, 0)  # corner radius; margin left for the glow
    if big:
        p.glow(x + m, y + m, w - 2 * m, h - 2 * m, r, "glow", 1 if pressed else 0.85)
    p.rounded(x + m, y + m, w - 2 * m, h - 2 * m, r, SUNK if pressed else RAISED, "glow-light" if pressed else "glow")


def press(pressed):
    """How far what is on a button moves when it is pressed: it lights up instead."""
    return 0


def ink(pressed):
    """The colour of what is on a button: blue, lighter when pressed."""
    return "ink-light" if pressed else "ink"


def lamp(p, x, y, on):
    p.rect(x, y, 2, 2, "glow-light" if on else "glow-dim")


def lettered_button(p, x, y, w, h, text, pressed=False, lit=None):
    """A button with a word on it, and a lamp at its left when `lit` is not None (on or off)."""
    button(p, x, y, w, h, pressed)
    top = y + (h - CELL_H) // 2
    if lit is None:
        centred(p, text, x, top, w, ink(pressed))
        return
    lamp(p, x + 4, top + 2, lit)
    centred(p, text, x + 7, top, w - 7, ink(pressed) if lit else "ink-dim")


# --- the title strip and its buttons ------------------------------------------------------------------

TITLE_H = 14
BOX = 9  # a title button
# focused or not: the name. The edge is the window's and glows the same either way.
NAME_INK = {True: "ink", False: "ink-dim"}
# A title button's glyph as rectangles in its 9 x 9 box (Main Menu's and Close's are drawn to any size)
GLYPHS = {
    "min": ((2, 5, 5, 1),),
    "shade": ((2, 2, 5, 1),),
    "unshade": ((2, 2, 5, 1), (2, 3, 1, 3), (6, 3, 1, 3), (2, 6, 5, 1)),
}


def menu_glyph(size):
    """Main Menu's three lines in a `size` box, one pixel thick, as many rows above as below."""
    top = (size - 5) // 2
    return tuple((2, top + 2 * i, size - 4, 1) for i in range(3))


def title_button(p, x, y, glyph, pressed=False, size=BOX):
    button(p, x, y, size, size, pressed)
    if glyph == "close":
        a, b = 2.5, size - 2.5
        p.line(f"M{x + a} {y + a}L{x + b} {y + b}M{x + b} {y + a}L{x + a} {y + b}", ink(pressed), 1)
        return
    rects = menu_glyph(size) if glyph == "menu" else GLYPHS[glyph]
    p.path("".join(f"M{x + gx} {y + gy}h{gw}v{gh}h{-gw}z" for gx, gy, gw, gh in rects), ink(pressed))


def strip_ground(p, x, y, w, left=False, right=False, bottom=False):
    """The strip from `x` to `x + w`: one flat near-black fill with the window's edge along its top (and its
    ends, and its bottom when the strip is the whole shaded window)."""
    edge = "glow"
    p.rect(x, y, w, TITLE_H, "title")
    p.rect(x, y, w, 1, edge)
    if bottom:
        p.rect(x, y + TITLE_H - 1, w, 1, edge)
    if left:
        p.rect(x, y, 1, TITLE_H, edge)
    if right:
        p.rect(x + w - 1, y, 1, TITLE_H, edge)


def title_name(p, text, x0, x1, y, focused):
    """A window's name in the middle of `x0`..`x1`."""
    left = x0 + (x1 - x0 - text_width(text)) // 2
    letters(p, text, left, y + 4, NAME_INK[focused])


# Where a window's title buttons are, from its right end; Main Menu from its left
RIGHT_BUTTONS = {"min": 31, "shade": 21, "unshade": 21, "close": 11}
MENU_X = 6
RULES_FROM, RULES_TO = 6, 4  # the name's room's margins: from the left end (or after Main Menu), up to the first button


def title_strip(p, x, y, w, name, focused, buttons=("shade", "close"), menu=False, shaded=False):
    """A whole title strip: ground, name and buttons, as every window has it."""
    strip_ground(p, x, y, w, left=True, right=True, bottom=shaded)
    start = x + (MENU_X + BOX + RULES_FROM - 3 if menu else RULES_FROM)
    first = min((RIGHT_BUTTONS[b] for b in buttons), default=0)
    title_name(p, name, start, x + w - first - RULES_TO, y, focused)
    if menu:
        title_button(p, x + MENU_X, y + 3, "menu")
    for b in buttons:
        title_button(p, x + w - RIGHT_BUTTONS[b], y + 3, b)


# --- sliders ------------------------------------------------------------------------------------------


def groove(p, x, y, w):
    """A grey slider's groove: a dark line with a lighter one along its middle, three pixels high."""
    p.rect(x, y, w, 3, "steel-dark")
    p.rect(x, y + 1, w, 1, "steel-mid")


def thumb(p, x, y, w, h, pressed=False, upright=False, left=False):
    """A grey slider's thumb under a glowing line along its top (and its left side when `left`): a dark frame
    round a grey face with a light line along it, lying or, on an `upright` slider's thumb, standing."""
    p.rect(x, y, w, 1, "glow-light" if pressed else "glow")
    if left:
        p.rect(x, y, 1, h, "glow-light" if pressed else "glow")
    bx, by = x + left, y + 2
    bw, bh = w - left, h - 2
    p.rect(bx, by, bw, bh, "steel-dark")
    p.rect(bx + 1, by + 1, bw - 2, bh - 2, "steel" if pressed else "steel-mid")
    if not upright and bh > 4:
        p.rect(bx + 2, by + bh // 2, bw - 4, 1, "steel-dark" if pressed else "steel")
    elif bw > 4:
        p.rect(bx + bw // 2, by + 2, 1, bh - 4, "steel-dark" if pressed else "steel")


def eq_thumb(p, x, y, pressed=False):
    """The equalizer's 11 x 11 thumb: two blue triangles facing each other across its middle, their slanting
    sides curved in, and a light round between their points."""
    p.path(f"M{x + 0.5} {y + 1}Q{x + 5.5} {y + 8} {x + 10.5} {y + 1}V{y + 10}Q{x + 5.5} {y + 3} {x + 0.5} {y + 10}Z",
           Gradient("thumb-light", "thumb") if pressed else Gradient("thumb", "thumb-dark"))
    p.ellipse(x + 5.5, y + 5.5, 1.5, 2.5, "ink-light" if pressed else "thumb-light")


def level_colour(k, n=27):
    """A level's glow, brighter as it rises from 0 to `n`."""
    return ("glow-mid", "glow", "glow-light")[min(2, 3 * k // (n + 1))]
