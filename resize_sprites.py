
from PIL import Image

for index in range(4):
    filename = f"images/hero_idle_{index}.png"

    image = Image.open(filename).convert("RGBA")
    image = image.resize((40, 60), Image.Resampling.NEAREST)
    image.save(filename)

print("Sprites restaurados para 40x60!")
