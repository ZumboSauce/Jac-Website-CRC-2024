from PIL import Image
import pathlib
import math

glint_path =  pathlib.Path(__file__).parent.parent.resolve() / "img/mc/Enchanted_Item_Glint.png"

if __name__ == '__main__':
    scale = 4
    glint_f = Image.open(glint_path).resize((64*scale, 64*scale), resample=Image.Resampling.BICUBIC)
    glint_h = 64 * scale
    glint_w = 64 * scale
    glint = Image.new('RGB', (glint_h*2*scale, glint_w*2*scale))
    for i in range(round(glint.width/glint_w)):
        for j in range(round(glint.height/glint_h)):
            glint.paste(glint_f, (0+64*scale*i, 0+64*scale*j))
    glint = glint.rotate(45, expand=1, resample=Image.Resampling.BICUBIC)
    x = glint.width
    y = glint.height
    #glint = glint.crop((x, y, x+64, y+64))
    glint.save('enchant.png')
    frames = []
    sl_sz = 1
    for i in range(glint.width):
        slice = glint.crop((0, 0, 1, y))
        main = glint.crop((1, 0, y, y))
        glint.paste(slice, (x-1, 0, x, y))
        glint.paste(main, (0, 0, x-1, y))
        frames.append(glint.copy().crop((x/2 - 32 ,y/2 - 32, x/2 + 32, y/2 + 32)))
    frames[0].save("enchant.gif", format="GIF", append_images=frames[1:], save_all=True, duration=50, loop=0, optimize=False)
    
    