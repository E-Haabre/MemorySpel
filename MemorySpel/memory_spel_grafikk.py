import random
import pygame
from pathlib import Path



sprites_path = Path(__file__).resolve().parent
sprites_path = sprites_path / "Spritesheets"

spritesLett_path = sprites_path / "SpritesLett"
spritesMedium_path = sprites_path / "SpritesMedium"
#spritesVanskelig_path = sprites_path / "SpritesVanskelig.png"

lett1 = spritesLett_path / "ark1.png"
lett2 = spritesLett_path / "bro1.png"
lett3 = spritesLett_path / "dør1.png"
lett4 = spritesLett_path / "fuglebur.png"
lett5 = spritesLett_path / "hus1.png"
lett6 = spritesLett_path / "katt.png"
lett7 = spritesLett_path / "kopp.png"
lett8 = spritesLett_path / "ku.png"
lett9 = spritesLett_path / "mugge.png"
lett10 = spritesLett_path / "planet1.png"
lett11 = spritesLett_path / "pyramide1.png"
lett12 = spritesLett_path / "rekkert.png"
lett13 = spritesLett_path  / "sky1.png"
lett14 = spritesLett_path / "smukk.png"
lett15 = spritesLett_path / "sol.png"
lett16 = spritesLett_path / "tann.png"
lett17 = spritesLett_path / "verktøy1.png"
lett18 = spritesLett_path / "tennis.png"

bilder = [lett1, lett2, lett3, lett4, lett5, lett6, lett7, lett8, lett9, lett10, lett11, lett12, lett13, lett14, lett15, lett16, lett17, lett18]

bilder = [pygame.image.load(sprite) for sprite in bilder]
print(bilder)

# VANSKELIGHETSGRAD: LETT
colors = ['#e06954', '#2b4c6b', '#51b386', '#f7d367', '#b8f8d3', '#4ad4ef','#7367ef', '#e36bd9', '#efe267', \
          '#511880', '#085cc9', '#83c638', '#faf118', '#f2843e', '#b01d78', '#940d21', '#cf2121', '#ff4854', \
          '#60903b', '#13624b', '#a2fcce', '#eefcf4', '#21a469', '#002bff']
random.shuffle(colors)
random.shuffle(bilder)

