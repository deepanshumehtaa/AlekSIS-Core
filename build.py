"""Build utility code for AlekSIS-Core, called by poetry"""

import os
from xml.dom import minidom

from cairosvg import svg2png


def bag_display(svg_xml):
    """Modify SVG to only display schoolbag"""
    for elem in svg_xml.getElementsByTagName("g"):
        if elem.attributes.get("id", None).value == "widgets-with-shadow":
            elem.setAttribute("display", "none")
        elif elem.attributes.get("id", None).value == "favicon-bag":
            del elem.attributes["display"]

    return svg_xml


icon_dir = "aleksis/core/static/icons"
icons = {
    "android": {"sizes": [192, 512], "source": "aleksis/core/static/img/aleksis-icon.svg"},
    "apple": {"sizes": [76, 114, 152, 180], "source": "aleksis/core/static/img/aleksis-icon.svg"},
    "favicon": {
        "sizes": [16, 32, 48],
        "source": "aleksis/core/static/img/aleksis-icon.svg",
        "preprocess": bag_display,
    },
}


def build(setup_kwargs):
    """Generate build files, namely PNG icons"""
    os.makedirs(icon_dir, exist_ok=True)

    for group in icons:
        svg_xml = minidom.parse(icons[group]["source"])
        if preprocess := icons[group].get("preprocess", None):
            svg_xml = preprocess(svg_xml)

        for size in icons[group]["sizes"]:
            target = os.path.join(icon_dir, f"{group}_{size}.png")
            scale = size / 256
            svg2png(
                bytestring=svg_xml.toxml().encode("utf-8"), dpi=1200, scale=scale, write_to=target
            )

    setup_kwargs["package_data"]["aleksis.core"] += ["static/icons/*"]


if __name__ == "__main__":
    build()
