from PIL import Image

img = Image.open(r".\room[1,1].png")

for x in range(0, 490, 1):
    for y in range(0, 490, 1):
        r,v,b = img.getpixel((x, y))
        if r < 127 :
            new_r = 0
        else:
            new_r = 255

        if v < 127 :
            new_v = 0
        else:
            new_v = 255
        
        if b < 127 :
            new_b = 0
        else:
            new_b = 255

        """if r == v == b:
            new_r = 61
            new_v = 61
            new_b = 61"""
            
        img.putpixel((x, y), (new_r, new_v, new_b))

img.show()

img.save(r".\room[1,1].png")