import cv2
import numpy as np
import imutils
import tkinter as tk
import pandas as pd
from scipy.spatial import KDTree
import ssl

class ColorDataset:
    def __init__(self, url="https://raw.githubusercontent.com/codebrainz/color-names/master/output/colors.csv"):
        self.url = url
        self.tree = None
        self.names = None

    def load(self):
        try:
            ssl._create_default_https_context = ssl._create_unverified_context
            df = pd.read_csv(self.url, names=['Nome', 'Hex', 'R', 'G', 'B'])
            self.names = df['Nome'].values
            self.tree = KDTree(df[['R', 'G', 'B']].values)
            return True
        except Exception as e:
            print(f"Erro ao carregar dataset: {e}")
            return False

    def get_closest_color_name(self, r, g, b):
        if not self.tree:
            return "Desconhecido"
        _, index = self.tree.query((r, g, b))
        return self.names[index]

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
        
        px, py = self.panel.winfo_x(), self.panel.winfo_y()
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
            
            text = f"{c['label']}" if len(colors) == 1 else f"{c['label']} - {c['pct']:.1f}%"
                
            color_label = tk.Label(row, text=text, bg="#282828", fg="white", font=("Arial", 10, "bold"))
            color_label.pack(side=tk.LEFT)

        nova_altura = 20 + (len(colors) * 32)
        px, py = self.panel.winfo_x(), self.panel.winfo_y()
        self.panel.geometry(f"300x{nova_altura}+{px}+{py}")

    def destroy(self):
        self.panel.destroy()

class ColorAnalyzerApp:
    def __init__(self, dataset):
        self.dataset = dataset
        
        self.root_tk = tk.Tk()
        self.root_tk.withdraw()
        self.panel_tk = ResultPanel(self.root_tk)
        
        self.camera = cv2.VideoCapture(0)
        self.kernel = np.ones((9, 9), np.uint8)
        
        self.frame_atual = None
        self.hsv_atual = None
        self.limite_inferior_hsv = None
        self.limite_superior_hsv = None

        cv2.namedWindow("Frame RGB")
        cv2.setMouseCallback("Frame RGB", self.mouse_click)

    def mouse_click(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            if self.frame_atual is not None and self.hsv_atual is not None:
                b, g, r = int(self.frame_atual[y, x][0]), int(self.frame_atual[y, x][1]), int(self.frame_atual[y, x][2])
                h, s, v = int(self.hsv_atual[y, x][0]), int(self.hsv_atual[y, x][1]), int(self.hsv_atual[y, x][2])
                
                nome_cor_rastreada = self.dataset.get_closest_color_name(r, g, b)
                cor_bgr_rastreada = (b, g, r)

                h_tolerancia = 15
                sv_tolerancia = 50

                self.limite_inferior_hsv = np.array([
                    max(0, h - h_tolerancia), 
                    max(50, s - sv_tolerancia), 
                    max(50, v - sv_tolerancia)
                ], dtype=np.uint8)
                
                self.limite_superior_hsv = np.array([
                    min(179, h + h_tolerancia), 
                    min(255, s + sv_tolerancia), 
                    min(255, v + sv_tolerancia)
                ], dtype=np.uint8)

                self.panel_tk.update_colors([{
                    "bgr": cor_bgr_rastreada, 
                    "label": nome_cor_rastreada
                }])
                self.panel_tk.show()

    def run(self):
        while True:
            ret, frame = self.camera.read()
            if not ret:
                break

            frame = imutils.resize(frame, width=1000)
            self.frame_atual = frame.copy()
            self.hsv_atual = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            if self.limite_inferior_hsv is not None and self.limite_superior_hsv is not None:
                mask = cv2.inRange(self.hsv_atual, self.limite_inferior_hsv, self.limite_superior_hsv)
                mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, self.kernel)
                mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, self.kernel)
                _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

            cv2.imshow("Frame RGB", frame)
            
            try:
                self.root_tk.update()
            except tk.TclError:
                pass
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break

    def cleanup(self):
        self.camera.release()
        cv2.destroyAllWindows()
        self.root_tk.destroy()

if __name__ == '__main__':
    dataset = ColorDataset()
    if dataset.load():
        app = ColorAnalyzerApp(dataset)
        try:
            app.run()
        except Exception as error:
            print(f"Ocorreu um erro: {error}")
        finally:
            app.cleanup()