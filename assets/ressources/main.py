import json
import sys
import requests
from PIL import Image, ImageSequence
import io
import math
import time

if __name__ == '__main__':
    with open('/home/cheese/code/Jac-Website-CRC-2024/assets/ressources/load.json', 'r+') as f:
        data = json.load(f)
        idx = 0
        imgs = []
        for item, url in data.items():
            url = url["url"]
            if "var" in data[item].keys():
                for idx, var in enumerate(data[item]["var"]):
                    Image.open(io.BytesIO(requests.get(url.replace("${}", var)).content)).resize((64, 64)).save(f"{item}_{idx}.png")
                    data[item]["var"][var] = f"/assets/img/mc/{item}_{var}.png"
            elif url.find("github"):
                Image.open(io.BytesIO(requests.get(url).content)).resize((64, 64), Image.Resampling.LANCZOS).save(f"{item}.png")
            else:
                Image.open(io.BytesIO(requests.get(url).content)).save(f"{item}.png")
            data[item]["texture"] = f"/assets/img/mc/{item}.png"
            time.sleep(2)
            print(item)
            data[item].pop("url", None)
            data[item].pop("idx", None)
        json.dump(data, f)
                


                    
        

            
            
