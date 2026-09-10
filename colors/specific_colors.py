"""
Valores de HSV em OpenCV
    Valor H/Matiz: Varia de 0 até 179
    Valor do S/Saturação: Varia de 0 até 255
    Valor V/Brilho: Varia de 0 até 255
"""

LOWER_COLORS = { # Tonalidade de cores mais claras/fracas
    # Vermelhos e Rosas
    "red": (160, 100, 100),
    "crimson": (170, 100, 100), # Carmesim
    "maroon": (160, 100, 20),   # Vinho
    "pink": (145, 100, 100),    # Rosa
    "coral": (5, 150, 150),     # Coral
    "salmon": (5, 100, 150),    # Salmão
    
    # Laranjas, Beges e Marrons
    "peach": (5, 50, 150),      # Pêssego
    "beige": (10, 20, 200),     # Bege (Saturação muito baixa)
    "orange": (5, 100, 100),    # Laranja
    "tangerine": (8, 150, 150), # Tangerina (Laranja mais intenso)
    "rust": (5, 100, 50),       # Ferrugem
    "bronze": (10, 100, 50),    # Bronze
    "brown": (10, 100, 20),     # Marrom
    "chocolate": (5, 100, 20),  # Chocolate (Marrom bem escuro)
    
    # Amarelos e Esverdeados
    "amber": (12, 150, 150),    # Âmbar
    "gold": (15, 100, 150),     # Dourado
    "khaki": (20, 50, 100),     # Caqui
    "yellow": (20, 100, 100),   # Amarelo
    "mustard": (20, 150, 100),  # Mostarda
    "olive": (20, 100, 50),     # Oliva
    
    # Verdes
    "lime": (25, 150, 150),     # Verde Limão
    "green": (35, 100, 100),    # Verde Padrão
    "emerald": (50, 150, 100),  # Esmeralda (Verde mais puro/fechado)
    "forest_green": (40, 100, 20), # Verde Floresta (Escuro)
    "mint": (60, 50, 150),      # Menta
    
    # Cianos e Azuis
    "teal": (75, 100, 50),      # Verde-azulado
    "turquoise": (80, 100, 100),# Turquesa
    "cyan": (85, 100, 100),     # Ciano
    "sky_blue": (90, 50, 150),  # Azul Celeste
    "blue": (100, 100, 100),    # Azul Padrão
    "royal_blue": (105, 150, 100), # Azul Real
    "navy": (100, 100, 20),     # Azul Marinho
    
    # Roxos e Violetas
    "indigo": (115, 100, 100),  # Índigo
    "violet": (125, 100, 100),  # Violeta
    "purple": (130, 100, 100),  # Roxo
    "lavender": (130, 20, 150), # Lavanda (Saturação baixa, alto brilho)
    "plum": (130, 100, 20),     # Ameixa (Roxo escuro)
    "magenta": (140, 100, 100), # Magenta
    
    # Cores neutras
    "white": (0, 0, 200),       # Branco
    "silver": (0, 0, 150),      # Prata
    "gray": (0, 0, 40),         # Cinza
    "black": (0, 0, 0)          # Preto
}

UPPER_COLORS = { 
    # Vermelhos e Rosas
    "red": (179, 255, 255),
    "crimson": (179, 255, 255),
    "maroon": (179, 255, 100),
    "pink": (160, 255, 255),
    "coral": (15, 255, 255),
    "salmon": (15, 200, 255),
    
    # Laranjas, Beges e Marrons
    "peach": (15, 150, 255),
    "beige": (25, 80, 255),
    "orange": (15, 255, 255),
    "tangerine": (15, 255, 255),
    "rust": (15, 255, 150),
    "bronze": (20, 255, 150),
    "brown": (20, 255, 150),
    "chocolate": (15, 255, 100),
    
    # Amarelos e Esverdeados
    "amber": (20, 255, 255),
    "gold": (25, 255, 255),
    "khaki": (30, 150, 255),
    "yellow": (30, 255, 255),
    "mustard": (25, 255, 200),
    "olive": (40, 255, 150),
    
    # Verdes
    "lime": (45, 255, 255),
    "green": (85, 255, 255),
    "emerald": (70, 255, 255),
    "forest_green": (65, 255, 100),
    "mint": (75, 150, 255),
    
    # Cianos e Azuis
    "teal": (90, 255, 200),
    "turquoise": (95, 255, 255),
    "cyan": (100, 255, 255),
    "sky_blue": (105, 200, 255),
    "blue": (130, 255, 255),
    "royal_blue": (120, 255, 255),
    "navy": (130, 255, 100),
    
    # Roxos e Violetas
    "indigo": (125, 255, 255),
    "violet": (135, 255, 255),
    "purple": (145, 255, 255),
    "lavender": (150, 100, 255),
    "plum": (150, 255, 100),
    "magenta": (160, 255, 255),
    
    # Cores neutras
    "white": (179, 30, 255),
    "silver": (179, 40, 200),
    "gray": (179, 50, 150),
    "black": (179, 255, 50)
}

TRIGGER_COLOR = { 
    # Formato BGR (Azul, Verde, Vermelho) para desenhar na tela
    "red": (0, 0, 255),
    "crimson": (60, 20, 220),
    "maroon": (0, 0, 128),
    "pink": (200, 130, 255),
    "coral": (80, 127, 255),
    "salmon": (114, 128, 250),
    
    "peach": (173, 213, 255),
    "beige": (220, 245, 245),
    "orange": (0, 165, 255),
    "tangerine": (0, 140, 255),
    "rust": (34, 87, 183),
    "bronze": (50, 127, 205),
    "brown": (19, 69, 139),
    "chocolate": (30, 105, 210),
    
    "amber": (0, 191, 255),
    "gold": (0, 215, 255),
    "khaki": (140, 230, 240),
    "yellow": (0, 255, 217),
    "mustard": (88, 206, 255),
    "olive": (0, 128, 128),
    
    "lime": (50, 205, 50),
    "green": (0, 255, 0),
    "emerald": (80, 200, 80),
    "forest_green": (34, 139, 34),
    "mint": (153, 255, 153),
    
    "teal": (128, 128, 0),
    "turquoise": (208, 224, 64),
    "cyan": (255, 255, 0),
    "sky_blue": (235, 206, 135),
    "blue": (255, 0, 0),
    "royal_blue": (225, 105, 65),
    "navy": (128, 0, 0),
    
    "indigo": (130, 0, 75),
    "violet": (226, 43, 138),
    "purple": (255, 0, 128),
    "lavender": (250, 230, 230),
    "plum": (141, 56, 142),
    "magenta": (255, 0, 255),
    
    # Cores Neutras
    "white": (255, 255, 255),
    "silver": (192, 192, 192),
    "gray": (128, 128, 128),
    "black": (0, 0, 0)
}