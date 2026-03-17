import os
from PIL import Image

assets_dir = r"c:\Users\OK\Downloads\files\young-run-game\assets"
brain_dir = r"C:\Users\OK\.gemini\antigravity\brain\88245df1-9d55-4096-a2a1-e47d11423332"

def remove_magenta(img):
    img = img.convert("RGBA")
    datas = img.getdata()
    newData = []
    
    # Simple chroma keying logic for near-magenta colors
    for item in datas:
        # Check if R and B are high, and G is low, which indicates magenta pinkish background
        if item[0] > 200 and item[1] < 100 and item[2] > 200:
            newData.append((255, 255, 255, 0)) # Transparent
        else:
            newData.append(item)
            
    img.putdata(newData)
    return img

def split_and_key(filename, cols, rows, prefix, names=None):
    # Find the generated file in brain dir (using startswith because of timestamp)
    target_path = None
    for f in os.listdir(brain_dir):
        if f.startswith(filename) and f.endswith(".png"):
            target_path = os.path.join(brain_dir, f)
            break
            
    if not target_path:
        print(f"File starting with {filename} not found.")
        return
        
    img = Image.open(target_path)
    img_keyed = remove_magenta(img)
    
    w, h = img_keyed.size
    cw = w // cols
    ch = h // rows
    
    idx = 0
    for y in range(rows):
        for x in range(cols):
            box = (x * cw, y * ch, (x + 1) * cw, (y + 1) * ch)
            cropped = img_keyed.crop(box)
            if names and idx < len(names):
                name = names[idx]
            else:
                name = f"{prefix}_{idx}.png"
            
            out_path = os.path.join(assets_dir, name)
            cropped.save(out_path)
            print(f"Saved {out_path}")
            idx += 1

print("Processing transparent images...")

# Character: 1x6
char_names = ["char_idle.png", "char_run.png", "char_jump.png", "char_doublejump.png", "char_slide.png", "char_fall.png"]
split_and_key("char_sheet_magenta", 6, 1, "char", char_names)

# Items: 2x2
item_names = ["item_gel.png", "item_water.png", "obs_hareubang.png", "obs_wall.png"]
split_and_key("items_sheet_magenta", 2, 2, "item", item_names)

# Bird: 1x1
bird_names = ["obs_bird.png"]
split_and_key("bird_magenta", 1, 1, "obs", bird_names)

# Background: 1x3 vertical layers
bg_names = ["bg_sky.png", "bg_mid.png", "bg_front.png"]
split_and_key("bg_parallax_transparent", 1, 3, "bg", bg_names)

print("Done processing transparent images.")
