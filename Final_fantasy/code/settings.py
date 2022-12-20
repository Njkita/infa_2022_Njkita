# игровые настройки
WIDTH    = 1280	
HEIGTH   = 720
FPS      = 60

TILESIZE = 64

HITBOX_OFFSET = {
	'player': -26,
	'object': -40,
	'grass': -10,
	'invisible': 0}

#пользовательский интерфейс 
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
FONT = '../graphics/font/joystix.ttf' #шрифт
FONT_SIZE = 18

#цвета интерфейса
HEALTH_COLOR = '#FF1493'
ENERGY_COLOR = '#7B68EE'
BORDER_COLOR_ACTIVE = 'gold'
TEXT_COLOR_SELECTED = '#111111'
BAR_COLOR = '#EEEEEE'
BAR_COLOR_SELECTED = '#111111'
UPGRADE_BACK_COLOR_SELECTED = '#EEEEEE'

#прочие цвета
WATER_COLOR = '#71ddee'
BACK_COLOR = '#222222'
BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'

#оружие 
weapon_data = {
	'sword': {'cooldown': 100, 'damage': 15,
           'graphic':'../graphics/weapons/sword/full.png'},
	'lance': {'cooldown': 400, 'damage': 30,
           'graphic':'../graphics/weapons/lance/full.png'},
	'axe': {'cooldown': 300, 'damage': 20, 
         'graphic':'../graphics/weapons/axe/full.png'},
	'rapier':{'cooldown': 50, 'damage': 8, 
           'graphic':'../graphics/weapons/rapier/full.png'},
	'sai':{'cooldown': 80, 'damage': 10, 
        'graphic':'../graphics/weapons/sai/full.png'}
            }

#магия
magic_data = {
	'flame': {'strength': 5,'cost': 20,
           'graphic':'../graphics/particles/flame/fire.png'},
	'heal' : {'strength': 20,'cost': 10,
           'graphic':'../graphics/particles/heal/heal.png'}
            }

#монстры
monster_data = {
	'raccoon': {'health': 300,'exp':250,'damage':40,'attack_type': 'claw',
             'speed': 2, 'resistance': 3, 'attack_radius': 120, 
             'notice_radius': 400},
    'orgalorg': {'health': 100,'exp':100,'damage':20,'attack_type': 'slash', 
              'speed': 3, 'resistance': 3, 'attack_radius': 80, 
              'notice_radius': 360},
	'litch': {'health': 100,'exp':110,'damage':8,'attack_type': 'thunder',
            'speed': 4, 'resistance': 3, 'attack_radius': 60, 
            'notice_radius': 350},
	'evil_plant': {'health': 70,'exp':120,'damage':6,'attack_type': 'leaf_attack',
            'speed': 3, 'resistance': 3, 'attack_radius': 50, 
            'notice_radius': 300}
            }




