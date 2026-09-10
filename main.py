import cv2
import numpy as np
import imutils
import tkinter as tk
import pandas as pd
from scipy.spatial import KDTree
import ssl

# ==========================================
# SIMULAÇÃO DOS SEUS MÓDULOS EXTERNOS
# ==========================================
# (Substitua pela sua importação real se desejar: from functions.color_translation import traduzir_cor)
def traduzir_cor(nome_cor):
    # Função dummy apenas para o código funcionar direto.
    return nome_cor 

# Variáveis globais para armazenar a árvore e nomes
arvore_cores = None
nomes_cores = None

# ==========================================
# DATASET DE CORES
# ==========================================
def load_color_dataset():
    global arvore_cores, nomes_cores
    print("Baixando dataset de cores do GitHub (865 cores)...")
    try:
        ssl._create_default_https_context = ssl._create_unverified_context
        
        url_dataset = "https://raw.githubusercontent.com/codebrainz/color-names/master/output/colors.csv"
        df_cores = pd.read_csv(url_dataset, names=['Nome', 'Hex', 'R', 'G', 'B'])
        
        valores_rgb = df_cores[['R', 'G', 'B']].values
        nomes_cores = df_cores['Nome'].values
        
        arvore_cores = KDTree(valores_rgb)
        
        print(f"Sucesso! {len(df_cores)} cores carregadas.")
        return True
    except Exception as e:
        print(f"Erro ao baixar ou processar o dataset: {e}")
        return False

# ==========================================
# PAINEL TKINTER
# ==========================================
class ResultPanel:
    def __init__(self, root):
        self.root = root
        self.panel = tk.Toplevel(self.root)
        self.panel.overrideredirect(True)
        self.panel.attributes('-topmost', True)
        self.panel.geometry("300x50+200+100") 
        self.panel.configure(bg="#282828")
        
        self.panel_drag_x = 0
        self.panel_drag_y = 0
        self.panel.bind("<ButtonPress-1>", self.on_panel_press)
        self.panel.bind("<B1-Motion>", self.on_panel_drag)

        self.colors_frame = tk.Frame(self.panel, bg="#282828")
        self.colors_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.reset_empty()
        self.panel.withdraw()

    def on_panel_press(self, event):
        self.panel_drag_x = event.x
        self.panel_drag_y = event.y

    def on_panel_drag(self, event):
        deltax = event.x - self.panel_drag_x
        deltay = event.y - self.panel_drag_y
        x = self.panel.winfo_x() + deltax
        y = self.panel.winfo_y() + deltay
        self.panel.geometry(f"+{x}+{y}")

    def show(self):
        self.panel.deiconify()

    def hide(self):
        self.panel.withdraw()
        self.reset_empty()

    def reset_empty(self):
        for widget in self.colors_frame.winfo_children():
            widget.destroy()
        lbl_vazio = tk.Label(self.colors_frame, text="Selecione uma área...", 
                             bg="#282828", fg="gray", font=("Arial", 11, "italic"))
        lbl_vazio.pack(pady=10)
        
        px = self.panel.winfo_x()
        py = self.panel.winfo_y()
        if px <= 0 and py <= 0:
            px, py = 200, 100
        self.panel.geometry(f"300x50+{px}+{py}")

    def update_colors(self, colors):
        for widget in self.colors_frame.winfo_children():
            widget.destroy()

        for c in colors:
            b, g, r = c["bgr"]
            hex_color = f"#{int(r):02x}{int(g):02x}{int(b):02x}"
            
            row = tk.Frame(self.colors_frame, bg="#282828")
            row.pack(fill=tk.X, pady=3)
            
            color_box = tk.Label(row, bg=hex_color, width=4, height=1)
            color_box.pack(side=tk.LEFT, padx=(0, 10))
            
            if len(colors) == 1:
                text = f"{c['label']}"
            else:
                text = f"{c['label']} - {c['pct']:.1f}%"
                
            color_label = tk.Label(row, text=text, bg="#282828", fg="white", font=("Arial", 10, "bold"))
            color_label.pack(side=tk.LEFT)

        nova_altura = 20 + (len(colors) * 32)
        px = self.panel.winfo_x()
        py = self.panel.winfo_y()
        self.panel.geometry(f"300x{nova_altura}+{px}+{py}")

    def destroy(self):
        self.panel.destroy()


# ==========================================
# LÓGICA DO OPENCV (CAMERA E TRACKING)
# ==========================================
# Variáveis globais para rastreamento
frame_atual = None
hsv_atual = None
limite_inferior_hsv = None
limite_superior_hsv = None
nome_cor_rastreada = None
cor_bgr_rastreada = None

def get_closest_color_name(r, g, b):
    global arvore_cores, nomes_cores
    distancia, indice = arvore_cores.query((r, g, b))
    nome = nomes_cores[indice]
    return traduzir_cor(nome)

def mouse_click(event, x, y, flags, param):
    global frame_atual, hsv_atual, limite_inferior_hsv, limite_superior_hsv
    global nome_cor_rastreada, cor_bgr_rastreada, painel_tk

    if event == cv2.EVENT_LBUTTONDOWN:
        if frame_atual is not None and hsv_atual is not None:
            # 1. Pega os valores do pixel exato (Forçando para int normal do Python)
            b, g, r = int(frame_atual[y, x][0]), int(frame_atual[y, x][1]), int(frame_atual[y, x][2])
            h, s, v = int(hsv_atual[y, x][0]), int(hsv_atual[y, x][1]), int(hsv_atual[y, x][2])
            
            # 2. Acha o nome da cor usando o dataset
            nome_cor_rastreada = get_closest_color_name(r, g, b)
            cor_bgr_rastreada = (b, g, r)

            # 3. Cria limites dinâmicos para o OpenCV rastrear o objeto
            # OpenCV HSV limits: H (0-179), S (0-255), V (0-255)
            h_tolerancia = 15
            sv_tolerancia = 50

            # 4. Força o tipo np.uint8 exigido pelo cv2.inRange
            limite_inferior_hsv = np.array([
                max(0, h - h_tolerancia), 
                max(50, s - sv_tolerancia), 
                max(50, v - sv_tolerancia)
            ], dtype=np.uint8)
            
            limite_superior_hsv = np.array([
                min(179, h + h_tolerancia), 
                min(255, s + sv_tolerancia), 
                min(255, v + sv_tolerancia)
            ], dtype=np.uint8)

            # 4. Atualiza o painel Tkinter
            painel_tk.update_colors([{
                "bgr": cor_bgr_rastreada, 
                "label": nome_cor_rastreada
            }])
            painel_tk.show()

def color_analyzer(camera, kernel):
    global frame_atual, hsv_atual, limite_inferior_hsv, limite_superior_hsv
    global nome_cor_rastreada, cor_bgr_rastreada, root_tk
    
    cv2.namedWindow("Frame RGB")
    cv2.setMouseCallback("Frame RGB", mouse_click)

    while True: 
        ret, frame = camera.read()
        if not ret:
            break

        frame = imutils.resize(frame, width=1000) 
        frame_atual = frame.copy()
        hsv_atual = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) 

        # Se alguma cor foi clicada, realiza o tracking
        if limite_inferior_hsv is not None and limite_superior_hsv is not None:
            mask = cv2.inRange(hsv_atual, limite_inferior_hsv, limite_superior_hsv)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel) 
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2] 

        cv2.imshow("Frame RGB", frame)
        
        # ATUALIZA O TKINTER JUNTO COM O OPENCV
        try:
            root_tk.update()
        except tk.TclError:
            pass # Ignora caso a janela do Tkinter seja forçadamente fechada
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

if __name__ == '__main__':
    # 1. Carrega o dataset
    sucesso = load_color_dataset()
    
    if sucesso:
        try:
            # 2. Inicializa o Tkinter (Root invisível, só o Painel aparece)
            root_tk = tk.Tk()
            root_tk.withdraw()
            painel_tk = ResultPanel(root_tk)

            # 3. Inicializa Câmera
            camera = cv2.VideoCapture(0) 
            kernel = np.ones((9, 9), np.uint8) 

            # 4. Roda o analisador
            color_analyzer(camera, kernel)

            # 5. Limpa memória ao sair
            camera.release()
            cv2.destroyAllWindows()
            root_tk.destroy()

        except Exception as error:
            if 'camera' in locals():
                camera.release()
            cv2.destroyAllWindows()
            print(f"Ocorreu um erro: {error}")