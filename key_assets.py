import os
from PIL import Image

assets_dir = r"c:\Users\OK\Downloads\files\young-run-game\assets"
brain_dir = r"C:\Users\OK\.gemini\antigravity\brain\88245df1-9d55-4096-a2a1-e47d11423332"

def remove_magenta(img):
    img = img.convert("RGBA")
    data = img.get_flattened_data() if hasattr(img, 'get_flattened_data') else img.getdata()
    newData = []
    
    # Simple chroma keying logic for near-magenta colors
    for item in data:
        # Check if R and B are high, and G is low, which indicates magenta pinkish background
        if item[0] > 200 and item[1] < 100 and item[2] > 200:
            newData.append((255, 255, 255, 0)) # Transparent
        else:
            newData.append(item)
            
    img.putdata(newData)
    return img

def process_and_save(prefix, final_name):
    # Find the generated file in brain dir
    target_path = None
    # We look for the most recently created file matching the prefix to avoid older generations
    matches = []
    for f in os.listdir(brain_dir):
        if f.startswith(prefix) and f.endswith(".png"):
            matches.append(os.path.join(brain_dir, f))
            
    if not matches:
        print(f"File starting with {prefix} not found.")
        return
        
    # Sort by modify time to get the latest
    matches.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    target_path = matches[0]
        
    img = Image.open(target_path)
    img_keyed = remove_magenta(img)
    
    out_path = os.path.join(assets_dir, final_name)
    img_keyed.save(out_path)
    print(f"Saved {out_path}")

print("Processing transparent retro images...")

os.makedirs(assets_dir, exist_ok=True)

# Map prefix to final filename
asset_map = {
    "retro_char_idle": "char_idle.png",
    "retro_char_run": "char_run.png",
    "retro_char_jump": "char_jump.png",
    "retro_char_slide": "char_slide.png",
    "retro_char_fall": "char_fall.png",
    "retro_char_doublejump": "char_djump.png",
    "retro_obs_hareubang": "obs_hareubang.png",
    "retro_obs_wall": "obs_wall.png",
    "retro_obs_bird": "obs_bird.png",
    "retro_item_gel": "item_gel.png",
    "retro_item_water": "item_water.png",
    "retro_bg_sky": "bg_sky.png",
    "retro_bg_mid": "bg_mid.png",
    "retro_bg_front": "bg_front.png"
}

for prefix, final_name in asset_map.items():
    process_and_save(prefix, final_name)

print("Done processing transparent images.")
