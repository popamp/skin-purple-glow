"""The windows skin.toml lays out itself: the main window's bar view and the media library."""
from art_bar import (BAR_H, BAR_LEFT, BAR_MIN, BAR_RIGHT, BOX, CLOCK, DISPLAY_X, REPEAT, SHUFFLE, THUMB_TOP, TOGGLE_H, VOLUME_H,
                     VOLUME_THUMB, VOLUME_TOP, VOLUME_W)
from art_main import STATES
from kit import sheet_file
from art_pl import PLATE_W
import art_ml as ml


def toml(v):
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, dict):
        return "{ " + ", ".join(f"{k} = {toml(x)}" for k, x in v.items()) + " }"
    if isinstance(v, (list, tuple)):
        return "[" + ", ".join(toml(x) for x in v) + "]"
    return f'"{v}"' if isinstance(v, str) else str(v)


def element(kind, place, view="bar", **keys):
    """One element as TOML; a place with a text in it is `edges`, else `rect`."""
    where = "edges" if any(isinstance(v, str) for v in place) else "rect"
    return ["", f"[[window.{view}.element]]", f'type = "{kind}"', f"{where} = {toml(list(place))}",
            *(f"{k} = {toml(v)}" for k, v in keys.items())]  # fmt: skip


def area(sheet, x, y, w, h):
    return {"file": sheet_file(sheet), "area": [x, y, w, h]}


def end(x):
    """A place in the bar's right end, counted from where that end starts."""
    return f"end-{BAR_RIGHT - x}"


def sprite(sheet, w, h, normal, pressed):
    return {"normal": area(sheet, *normal, w, h), "pressed": area(sheet, *pressed, w, h)}


def toggle(sheet, states, w, h, at, flag, click, **more):
    """A toggle: `states` are its off, off pressed, on and on pressed corners in `sheet`."""
    x, y = at
    pics = {k: area(sheet, sx, sy, w, h) for k, (sx, sy) in zip(("normal", "pressed", "on", "on_pressed"), states)}
    return element("toggle", (end(x), y, end(x + w), y + h), **pics, flag=flag, click=click, **more)


GAP = 3  # between the bar's ends and Main Menu and Close, and between them and their neighbours
TRANSPORT_X = GAP + BOX + GAP
CONTROLS = "bar/controls"


def middle(h):
    """The row that puts something `h` high in the bar's middle."""
    return (BAR_H - h) // 2


def bar_window():
    b, mid = BOX, middle(BOX)
    e = ["", "[[window]]", 'key = "main"', "", "[window.bar]", 'edge = "bottom"', f"size = [{BAR_MIN}, {BAR_H}]"]
    e += element("image", (0, 0, BAR_LEFT, BAR_H), normal="bar/left.svg")
    e += element("image", (BAR_LEFT, 0, end(0), BAR_H), normal="bar/mid.svg", fill="tile")
    e += element("image", (end(0), 0, "end", BAR_H), normal="bar/right.svg")
    e += element("button", (GAP, mid, b, b), **sprite(CONTROLS, b, b, (0, 0), (0, b)),
                 menu_press="main", cursor="mainmenu", tip="Main Menu")  # fmt: skip
    transport = (
        (0, 23, "previous", "Previous", {"shift": "back5s", "ctrl": "start-of-list", "menu": "previous"}),
        (23, 23, "play", "Play", {"shift": "open-file", "ctrl": "open-url", "menu": "play"}),
        (46, 23, "pause", "Pause", {"menu": "pause"}),
        (69, 23, "stop", "Stop", {"shift": "stop-fadeout", "ctrl": "stop-after-current", "menu": "stop"}),
        (92, 22, "next", "Next", {"shift": "fwd5s", "ctrl": "end-of-list", "menu": "next"}),
    )
    for sx, w, click, tip, more in transport:
        e += element("button", (TRANSPORT_X + sx, middle(18), w, 18), **sprite("cbuttons", w, 18, (sx, 0), (sx, 18)), click=click,
                     **more, tip=tip)  # fmt: skip
    e += element("button", (TRANSPORT_X + 114 + GAP, middle(16), 22, 16), **sprite("cbuttons", 22, 16, (114, 0), (114, 16)),
                 click="open-file", shift="open-folder", ctrl="open-url", menu="eject", tip="Open")  # fmt: skip
    for sx, state in ((0, "playing"), (9, "paused"), (18, "stopped")):
        e += element("image", (DISPLAY_X + 4, middle(9), 9, 9), normal=area("playpaus", sx, 0, 9, 9), show=state)
    e += element("clock", (*CLOCK, 63, 13), hide="stopped")
    e += element("button", (*CLOCK, 63, 13), press="toggle-time-mode", menu="time")
    e += element("vis", (BAR_LEFT - 80, middle(16), 76, 16))
    e += element("button", (BAR_LEFT - 80, middle(16), 76, 16), press="cycle-vis-mode", menu="vis")
    e += element("marquee", (BAR_LEFT + 3, 3, end(-3), 9), double="file-info", cursor="songname",
                 tip="Song Title (right-click for options)", menu="song-title")  # fmt: skip
    thumb = sprite("posbar", 29, 10, (248, 0), (278, 0))
    e += element("slider", (BAR_LEFT, THUMB_TOP, end(0), THUMB_TOP + 10), value="position", thumb=thumb, thumb_len=29,
                 live=False, show="seekable", cursor="posbar", menu="seek")  # fmt: skip
    e += volume((end(9), middle(VOLUME_H)))
    eq = ((0, 61), (46, 61), (0, 73), (46, 73))
    e += toggle("shufrep", eq, 23, 12, (82, middle(12)), "eq-window", "toggle-eq-window")
    e += toggle("shufrep", [(x + 23, y) for x, y in eq], 23, 12, (106, middle(12)), "playlist-window", "toggle-playlist-window")
    rows = [TOGGLE_H * i for i in range(len(STATES))]
    (sx, sw), (rx, rw) = SHUFFLE, REPEAT
    e += toggle(CONTROLS, [(sx, y) for y in rows], sw, TOGGLE_H, (133, middle(TOGGLE_H)), "shuffle", "toggle-shuffle", menu="shuffle")
    e += toggle(CONTROLS, [(rx, y) for y in rows], rw, TOGGLE_H, (133 + sw, middle(TOGGLE_H)), "repeat", "toggle-repeat", menu="repeat")
    close = 133 + sw + rw + GAP
    assert close + b + GAP == BAR_RIGHT, "Close sits as far from the bar's end as from Repeat"
    e += element("button", (end(close), mid, end(close + b), mid + b), **sprite(CONTROLS, b, b, (b, 0), (b, b)),
                 click="exit", tip="Close")  # fmt: skip
    return e


def library_window():
    """The media library in the playlist's frame, with its own name on the title, the display with the
    visualizer under the title and the transport under the list."""
    pl = lambda x, y, w, h: area("pledit", x, y, w, h)
    focus = lambda x: {"normal": pl(x, 0, 25, 20), "inactive": pl(x, 21, 25, 20)}
    v, w = "normal", PLATE_W
    e = ["", "[[window]]", 'key = "library"', 'placement = "docked"', 'empty_press = "nothing"', "wheel_scrolls_list = true",
         "", "[window.normal]", "size = [400, 232]", "resize_step = [25, 29]", 'cursor = "pnormal"']  # fmt: skip
    e += element("image", (0, 0, 25, 20), v, **focus(0))
    e += element("image", (25, 0, "end-25", 20), v, **focus(127), fill="tile")
    right = lambda y: {"file": "ml/title-right.svg", "area": [0, y, 25, 20]}
    e += element("image", ("end-25", 0, "end", 20), v, normal=right(0), inactive=right(21))
    title = {"file": "ml/title.svg"}
    e += element("image", (f"center-{w // 2}", 0, f"center+{w - w // 2}", 20), v,
                 normal=title | {"area": [0, 0, w, 20]}, inactive=title | {"area": [0, 21, w, 20]})  # fmt: skip
    e += three("strip", ml.STRIP_TOP, ml.LIST_TOP, ml.STRIP_LEFT, ml.STRIP_RIGHT, v)
    e += element("image", (0, ml.LIST_TOP, 12, "end-38"), v, normal=pl(0, 42, 12, 29), fill="tile")
    e += element("image", ("end-20", ml.LIST_TOP, "end", "end-38"), v, normal=pl(31, 42, 20, 29), fill="tile")
    e += three("bottom", "end-38", "end", ml.BOTTOM_LEFT, ml.BOTTOM_RIGHT, v)
    e += element("drag", (0, 0, "end-22", ml.STRIP_TOP + ml.DISPLAY_TOP), v, double="toggle-library-maximize", cursor="ptbar")
    e += element("button", ("end-20", 3, "end-11", 12), v, pressed={"file": "ml/title-right.svg", "area": [0, 42, 9, 9]},
                 click="toggle-library-maximize", tip="Maximize")  # fmt: skip
    e += element("button", ("end-11", 3, "end-2", 12), v, pressed=pl(52, 42, 9, 9), click="toggle-library-window",
                 cursor="pclose", tip="Close")  # fmt: skip
    e += display_controls(v)
    thumb = {"normal": pl(52, 53, 8, 18), "pressed": pl(61, 53, 8, 18)}
    e += element("library", (12, ml.LIST_TOP, "end-7", "end-38"), v, menu="library", thumb=thumb)
    e += bottom_controls(v)
    e += element("resize", ("end-20", "end-20", "end", "end"), v, cursor="psize")
    return e


def centre(dx):
    """A place `dx` from the window's middle."""
    return f"center+{dx}" if dx >= 0 else f"center-{-dx}"


def three(name, top, bottom, left_w, right_w, v):
    """A row of the library's pieces: `name`-left, `name`-mid tiled and `name`-right."""
    at = lambda part: {"normal": f"ml/{name}-{part}.svg"}
    left = (0, top, left_w, bottom - top) if isinstance(bottom, int) else (0, top, left_w, bottom)  # all numbers: a rect
    e = element("image", left, v, **at("left"))
    e += element("image", (left_w, top, f"end-{right_w}", bottom), v, **at("mid"), fill="tile")
    e += element("image", (f"end-{right_w}", top, "end", bottom), v, **at("right"))
    return e


def display_controls(v):
    """The display's song block and its visualizer."""
    cx, cy = ml.CLOCK
    e = []
    for sx, state in ((0, "playing"), (9, "paused"), (18, "stopped")):
        e += element("image", (ml.MARGIN + 4, cy + 2, 9, 9), v, normal=area("playpaus", sx, 0, 9, 9), show=state)
    e += element("clock", (cx, cy, 63, 13), v, hide="stopped")
    e += element("button", (cx, cy, 63, 13), v, press="toggle-time-mode", menu="time")
    e += element("marquee", (ml.MARGIN + 4, ml.TITLE_ROW, ml.VIS_X - ml.MARGIN - 10, 9), v, double="file-info", cursor="songname",
                 tip="Song Title (right-click for options)", menu="song-title")  # fmt: skip
    for x, text in ((ml.KBPS_X, "kbps"), (ml.KHZ_X, "khz")):
        e += element("text", (x, ml.RATE_ROW, 15, 6), v, text=text)
    top = ml.STRIP_TOP + ml.DISPLAY_TOP + ml.VIS_INSET
    bottom = ml.STRIP_TOP + ml.DISPLAY_TOP + ml.DISPLAY_H - ml.VIS_INSET
    vis = (ml.VIS_X, top, f"end-{ml.RIGHT_MARGIN + ml.VIS_INSET}", bottom)
    e += element("vis", vis, v)
    e += element("button", vis, v, press="cycle-vis-mode", menu="vis")
    return e


def bottom_controls(v):
    """Under the list: the position bar across the window; the status, the transport in the middle, the volume
    and LIST under it."""
    at = lambda y: f"end-{ml.BOTTOM - y}"
    e = element("slider", (ml.MARGIN, at(ml.SEEK_TOP), f"end-{ml.RIGHT_MARGIN}", at(ml.SEEK_TOP + 10)), v, value="position",
                thumb=sprite("posbar", 29, 10, (248, 0), (278, 0)), thumb_len=29, live=False, show="seekable", cursor="posbar",
                menu="seek")  # fmt: skip
    sx, sy, sw, sh = ml.STATUS
    e += element("text", (sx + 3, at(sy + 3), sx + sw - 3, at(sy + 9)), v, text="library-status")
    left = ml.TRANSPORT_W // 2
    transport = (
        (0, 23, "previous", "Previous", {"shift": "back5s", "ctrl": "start-of-list", "menu": "previous"}),
        (23, 23, "library-play", "Play the picked track", {"shift": "open-file", "ctrl": "open-url", "menu": "play"}),
        (46, 23, "pause", "Pause", {"menu": "pause"}),
        (69, 23, "stop", "Stop", {"shift": "stop-fadeout", "ctrl": "stop-after-current", "menu": "stop"}),
        (92, 22, "next", "Next", {"shift": "fwd5s", "ctrl": "end-of-list", "menu": "next"}),
    )
    y = ml.BUTTONS_TOP
    for x, bw, click, tip, more in transport:
        e += element("button", (centre(x - left), at(y), centre(x + bw - left), at(y + 18)), v,
                     **sprite("cbuttons", bw, 18, (x, 0), (x, 18)), click=click, **more, tip=tip)  # fmt: skip
    x = 113 + GAP
    e += element("button", (centre(x - left), at(y + 1), centre(x + 22 - left), at(y + 17)), v,
                 **sprite("cbuttons", 22, 16, (114, 0), (114, 16)), click="open-file", shift="open-folder", ctrl="open-url", menu="eject",
                 tip="Open")  # fmt: skip
    lx, ly, lw, lh = ml.LIST_BUTTON
    from_end = ml.BOTTOM_RIGHT - lx
    e += volume((f"end-{from_end + 6 + VOLUME_W}", at(y + (18 - VOLUME_H) // 2)), v)
    e += element("button", (f"end-{from_end}", at(ly), f"end-{from_end - lw}", at(ly + lh)), v, menu_release="library",
                 tip="Library Menu")  # fmt: skip
    return e


def volume(at, view="bar"):
    """The bar's volume slider with its left top corner at `at`, counted from the window's end."""
    x, y = at
    right = f"end-{int(x[4:]) - VOLUME_W}"
    bottom = f"end-{int(y[4:]) - VOLUME_H}" if isinstance(y, str) else y + VOLUME_H
    track = {"file": sheet_file(CONTROLS), "first": [0, VOLUME_TOP, VOLUME_W, VOLUME_H], "step": [0, VOLUME_H], "count": 28}
    ty, tw, th = VOLUME_THUMB
    thumb = {"normal": area(CONTROLS, 15, ty, tw, th), "pressed": area(CONTROLS, 0, ty, tw, th)}
    thumb = {k: v | {"offset": [0, (VOLUME_H - th) // 2]} for k, v in thumb.items()}
    return element("slider", (x, y, right, bottom), view, value="volume", track=track, thumb=thumb, thumb_len=tw, reset=200,
                   wheel_step=8, cursor="volbal", tip="Volume")  # fmt: skip
