import PIL.ImageFont


__ALL__ = "text_with_padding"


def text_with_padding(font: PIL.ImageFont.FreeTypeFont, text: str, padding: int = -1) -> tuple:
    ascent, descent = font.getmetrics()
    (width, baseline), (offset_x, offset_y) = font.font.getsize(text)
    height = ascent+descent
    y_offset = descent-offset_y
    if padding < 0:
        padding = offset_y+descent
    shape = (width+padding, height+padding)
    pos = (padding/2, padding/2+y_offset)
    return (shape, pos)
