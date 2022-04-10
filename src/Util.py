import pygame
from meta import meta

def row_col_to_pos(r: int, c: int) -> list[int]:
    x = r * meta.screen.CELL_HEIGHT
    y = c * meta.screen.CELL_WIDTH
    return (x, y)

def parse_spritesheet():
    global sprite_info
    import json
    sprite_json = open('../resources/sprites.json').readlines()[0]
    sprite_json = json.loads(sprite_json)
    sprite_dict = dict()
    for o in sprite_json:
        sprite_dict[o['name']] = o
    return sprite_dict

def image_from_json(img, json_data) -> list[str]:
    return json_data[img]

def get_image(img) -> list[pygame.Surface]:
    global spritesheet, sprite_info
    spritesheet = pygame.image.load('../resources/spritesheet.png').convert_alpha()
    i = image_from_json(img, sprite_info)
    x, y, w, h = i['x'], i['y'], i['width'], i['height']
    rect = pygame.Rect((x, y, w, h))
    surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA, 32)
    surf.blit(spritesheet, (0, 0), rect)
    return surf

sprite_info = parse_spritesheet()