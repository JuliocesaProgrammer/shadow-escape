
from PIL import Image

for index in range(4):
    filename = f"images/hero_idle_{index}.png"
    image = Image.open(filename).convert("RGBA")

    pixels = image.load()

    for y in range(image.height):
        for x in range(image.width):
            red, green, blue, alpha = pixels[x, y]

            if red > 240 and green > 240 and blue > 240:
                pixels[x, y] = (255, 255, 255, 0)

    image.save(filename)

print("Fundo branco removido dos 4 sprites!")
