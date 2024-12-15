from PIL import Image, ImageFont, ImageDraw
import os

font = ImageFont.truetype(os.path.dirname(__file__) + "/blackpink.otf", 230)

def blackpink(teks):
    # Calculate text size using `getbbox` for more compatibility
    length = font.getbbox(teks)
    text_width = length[2] - length[0]
    text_height = length[3] - length[1]

    # Create a new image
    img = Image.new("RGB", (text_width + 100, text_height), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Draw the text centered
    text_position = ((img.width // 2) - (text_width // 2), -25)
    draw.text(text_position, teks, fill=(255, 148, 224), font=font)

    # Paste the image onto a new canvas
    hasil = Paste(img)
    img2 = Image.new("RGB", (hasil.width + 400, hasil.height + 400), color=(0, 0, 0))
    img2.paste(hasil, (int((img2.width / 2) - (hasil.width / 2)), int((img2.height / 2) - (hasil.height / 2))))

    return img2

def Paste(im):
    new = Image.new("RGB", (im.width + 20, im.height + 20), color=(255, 148, 224))
    new.paste(im, (int((new.width / 2) - (im.width / 2)), int((new.height / 2) - (im.height / 2))))
    return new
