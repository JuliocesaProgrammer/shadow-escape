
from PIL import Image

image = Image.open("images/hero_idle.png").convert("RGBA")

frame_width = image.width // 4
frame_height = image.height

for index in range(4):
    left = index * frame_width

    frame = image.crop((
        left,
        0,
        left + frame_width,
        frame_height
    ))

    frame.save(f"images/hero_idle_{index}.png")

print("Os 4 quadros foram separados!")
