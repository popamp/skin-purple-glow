"""Pictures as SVG: whole rectangles and outlines in colours named by their role.

A role of the glow (GLOW) is a class on the element, which a colour set
gives another colour; the dark grounds (FIXED) stay the same in every set.
"""
import colorsys
import os

# The glow by role, in the first colour set; a colour set turns every one round the colour wheel
GLOW = {
    "glow": "#ff2cff",  # the lines, the lettering, what is lit
    "glow-light": "#ffb0ff",  # highlights: pressed buttons, the thumbs' tops
    "glow-mid": "#b01cc0",  # labels, an unfocused window's lines
    "glow-dim": "#5c0a68",  # the wells' frames, unlit lettering
    "glow-deep": "#24032c",  # faint fills: a button's face, the graph's grid
    "ink": "#2a8cff",  # the lettering and the buttons' signs, blue against the glow
    "ink-light": "#a8d4ff",  # pressed
    "ink-dim": "#14427e",  # unlit
    "thumb": "#1a5cff",  # the equalizer's thumbs
    "thumb-light": "#6c9cff",
    "thumb-dark": "#082a8c",
}
FIXED = {
    "lcd": "#000000",  # the display's ground
    "body": "#06010a",  # the windows' panel
    "title": "#0e0a13",  # the title strips: flat, a shade lighter than the panel
    "base": "#000000",  # the sheets' spare room
    "steel": "#9a9a9a",  # the grey sliders: their light line
    "steel-mid": "#5e5e5e",
    "steel-dark": "#303030",
}

FIRST_SET = "Purple"
# (name, turn round the colour wheel in degrees from Purple)
OTHER_SETS = (("Cyan", -115), ("Lime", 165), ("Amber", 95), ("Crimson", 55))


def hexc(rgb):
    return "#%02x%02x%02x" % tuple(round(v * 255) for v in rgb)


def turned(c, degrees):
    h, l, s = colorsys.rgb_to_hls(*(int(c[i : i + 2], 16) / 255 for i in (1, 3, 5)))
    return hexc(colorsys.hls_to_rgb((h + degrees / 360) % 1, l, s))


def colour_sets():
    """skin.toml's [colors] tables: Purple as drawn, the others turned round the wheel."""
    lines = [f"[colors.{FIRST_SET}]", *(f'{role} = "{c}"' for role, c in GLOW.items())]
    for name, degrees in OTHER_SETS:
        lines += ["", f"[colors.{name}]", *(f'{role} = "{turned(c, degrees)}"' for role, c in GLOW.items())]
    return lines


def colour(role):
    """The fill of a role (or a #rrggbb colour) and its class when a set changes it."""
    if role in GLOW:
        return GLOW[role], f' class="{role}"'
    return FIXED.get(role, role), ""


class Gradient:
    """A vertical gradient between two roles, top to bottom."""

    def __init__(self, top, bottom):
        self.top, self.bottom = top, bottom


class Picture:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.defs, self.body, self.ids = [], [], {}

    def paint(self, p):
        if not isinstance(p, Gradient):
            fill, cls = colour(p)
            return f'fill="{fill}"{cls}'
        key = (p.top, p.bottom)
        if key not in self.ids:
            gid = self.ids[key] = f"g{len(self.ids)}"
            stops = [f'<stop offset="{offset}" stop-color="{colour(role)[0]}"{suffixed(role, "stop")}/>' for offset, role in ((0, p.top), (1, p.bottom))]
            self.defs.append(f'<linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1">{"".join(stops)}</linearGradient>')
        return f'fill="url(#{self.ids[key]})"'

    def rect(self, x, y, w, h, paint):
        if w > 0 and h > 0:
            self.body.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" {self.paint(paint)}/>')

    def path(self, d, paint):
        if d:
            self.body.append(f'<path d="{d}" {self.paint(paint)}/>')

    def rounded(self, x, y, w, h, r, paint, edge):
        """A box with corners rounded by `r`, filled with `paint` and outlined in `edge` along its inside."""
        fill = self.paint(paint)
        colour_, cls = colour(edge)
        classes = " ".join(c for c in (class_of(fill), f"{edge}-stroke" if cls else "") if c)
        fill = fill.split(" class=")[0]
        cls = f' class="{classes}"' if classes else ""
        self.body.append(f'<rect x="{x + 0.5}" y="{y + 0.5}" width="{w - 1}" height="{h - 1}" rx="{r}" {fill} stroke="{colour_}"{cls}/>')

    def glow(self, x, y, w, h, r, role, strength=0.8):
        """A soft light round the box: its outline, blurred, which spreads past the outline on both sides."""
        if "glow" not in self.ids:
            self.ids["glow"] = "glow"
            self.defs.append('<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="1"/></filter>')
        self.body.append(f'<rect x="{x + 0.5}" y="{y + 0.5}" width="{w - 1}" height="{h - 1}" rx="{r}" fill="none" stroke="{colour(role)[0]}" '
                         f'stroke-width="3" opacity="{strength}" filter="url(#glow)"{suffixed(role, "stroke")}/>')

    def ellipse(self, cx, cy, rx, ry, paint):
        self.body.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" {self.paint(paint)}/>')

    def line(self, d, role, width=1):
        """A stroked outline, for the few shapes that are lines."""
        self.body.append(f'<path d="{d}" fill="none" stroke="{colour(role)[0]}" stroke-width="{width}"{suffixed(role, "stroke")}/>')

    def svg(self):
        head = f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}">'
        defs = f"<defs>\n{chr(10).join(self.defs)}\n</defs>\n" if self.defs else ""
        return f"{head}\n{defs}" + "\n".join(self.body) + "\n</svg>\n"

    def save(self, path):
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.svg())


def suffixed(role, kind):
    """The class of a role's gradient stop or stroke, which the sets colour as they do its fills."""
    return f' class="{role}-{kind}"' if role in GLOW else ""


def class_of(attrs):
    """The class in a `fill=".." class=".."` pair, or nothing."""
    return attrs.split(' class="')[1].rstrip('"') if ' class="' in attrs else ""
