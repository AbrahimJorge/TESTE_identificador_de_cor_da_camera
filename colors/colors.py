"""
Valores de HSV em OpenCV

    Valor H/Matiz: Varia de 0 até 179
    Valor do S/Saturação: Varia de 0 até 255
    Valor V/Brilho: Varia de 0 até 255
"""

LOWER_COLORS = { # Tonalidade de cores mais claras/fracas
    # Nome da cor : (Matiz, Saturação, Brilho)
    "red": (160, 100, 100),     # Vermelho
    "crimson": (170, 100, 100), # Carmesim (Vermelho escuro/rosado)
    "maroon": (160, 100, 20),   # Vinho
    "salmon": (5, 100, 150),    # Salmão
    "peach": (5, 50, 150),      # Pêssego (Laranja bem claro)
    "coral": (5, 150, 150),     # Coral
    "orange": (5, 100, 100),    # Laranja
    "brown": (10, 100, 20),     # Marrom
    "khaki": (20, 50, 100),     # Caqui / Bege
    "gold": (15, 100, 150),     # Dourado
    "yellow": (20, 100, 100),   # Amarelo
    "mustard": (20, 150, 100),  # Mostarda
    "olive": (20, 100, 50),     # Oliva
    "lime": (25, 150, 150),     # Verde Limão
    "green": (35, 100, 100),    # Verde
    "mint": (60, 50, 150),      # Menta (Verde claro pastel)
    "teal": (75, 100, 50),      # Verde-azulado / Teal
    "turquoise": (80, 100, 100),# Turquesa
    "cyan": (85, 100, 100),     # Ciano / Azul claro
    "blue": (100, 100, 100),    # Azul
    "navy": (100, 100, 20),     # Azul Marinho
    "indigo": (115, 100, 100),  # Índigo (Entre azul e roxo)
    "violet": (125, 100, 100),  # Violeta
    "purple": (130, 100, 100),  # Roxo
    "magenta": (140, 100, 100), # Magenta
    "pink": (145, 100, 100),    # Rosa
    
    # Cores neutras
    "white": (0, 0, 200),       # Branco
    "silver": (0, 0, 150),      # Prata/Cinza Claro
    "gray": (0, 0, 40),         # Cinza
    "black": (0, 0, 0)          # Preto
}

UPPER_COLORS = { # Tonalidade de cores mais escuras/fortes
    # Nome da cor : (Matiz, Saturação, Brilho)
    "red": (179, 255, 255),
    "crimson": (179, 255, 255),
    "maroon": (179, 255, 100),
    "salmon": (15, 200, 255),
    "peach": (15, 150, 255),
    "coral": (15, 255, 255),
    "orange": (15, 255, 255),
    "brown": (20, 255, 150),
    "khaki": (30, 150, 255),
    "gold": (25, 255, 255),
    "yellow": (30, 255, 255),
    "mustard": (25, 255, 200),
    "olive": (40, 255, 150),
    "lime": (45, 255, 255),
    "green": (85, 255, 255),
    "mint": (75, 150, 255),
    "teal": (90, 255, 200),
    "turquoise": (95, 255, 255),
    "cyan": (100, 255, 255),
    "blue": (130, 255, 255),
    "navy": (130, 255, 100),
    "indigo": (125, 255, 255),
    "violet": (135, 255, 255),
    "purple": (145, 255, 255),
    "magenta": (160, 255, 255),
    "pink": (160, 255, 255),
    
    # Cores neutras
    "white": (179, 30, 255),
    "silver": (179, 40, 200),
    "gray": (179, 50, 150),
    "black": (179, 255, 50)
}

"""
O OpenCV trabalha com BGR ao invés de RGB.
"""

TRIGGER_COLOR = { # Faz uma marcação na cor correspondente (Formato BGR: Azul, Verde, Vermelho)
    "red": (0, 0, 255),
    "crimson": (60, 20, 220),   # Carmesim
    "maroon": (0, 0, 128),      # Vinho
    "salmon": (114, 128, 250),  # Salmão
    "peach": (173, 213, 255),   # Pêssego
    "coral": (80, 127, 255),    # Coral
    "orange": (0, 165, 255),    # Laranja
    "brown": (19, 69, 139),     # Marrom
    "khaki": (140, 230, 240),   # Caqui / Bege
    "gold": (0, 215, 255),      # Dourado
    "yellow": (0, 255, 217),    # Amarelo
    "mustard": (88, 206, 255),  # Mostarda
    "olive": (0, 128, 128),     # Oliva
    "lime": (50, 205, 50),      # Verde Limão
    "green": (0, 255, 0),       # Verde
    "mint": (153, 255, 153),    # Menta
    "teal": (128, 128, 0),      # Verde-azulado
    "turquoise": (208, 224, 64),# Turquesa
    "cyan": (255, 255, 0),      # Ciano
    "blue": (255, 0, 0),        # Azul
    "navy": (128, 0, 0),        # Azul Marinho
    "indigo": (130, 0, 75),     # Índigo
    "violet": (226, 43, 138),   # Violeta
    "purple": (255, 0, 128),    # Roxo
    "magenta": (255, 0, 255),   # Magenta
    "pink": (200, 130, 255),    # Rosa
    
    # Cores Neutras
    "white": (255, 255, 255),   # Branco
    "silver": (192, 192, 192),  # Prata
    "gray": (128, 128, 128),    # Cinza
    "black": (0, 0, 0)          # Preto
}