import tkinter as tk
import tkinter.ttk as ttk
import random
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# =====================================================
# CLASSES ET FONCTIONS POUR LA VISUALISATION DES TRIS
# =====================================================

class SortingVisualizer:
    """
    Classe permettant d'afficher la partie théorique et pratique (animation) d'un algorithme de tri.
    """
    def __init__(self, master, algorithm_name, sort_func, theory_text):
        self.master = master
        self.algorithm_name = algorithm_name
        self.sort_func = sort_func
        self.theory_text = theory_text
        
        # Cadre principal de la section
        self.frame = tk.Frame(master, bg="#f0f0f0")
        self.frame.pack(fill="both", expand=True)
        
        # Cadre supérieur pour la partie théorique et les contrôles
        self.top_frame = tk.Frame(self.frame, bg="#f0f0f0")
        self.top_frame.pack(side=tk.TOP, fill="x")
        
        # Affichage du texte théorique
        self.theory_label = tk.Label(self.top_frame, text=self.theory_text, justify=tk.LEFT, wraplength=500, bg="#f0f0f0")
        self.theory_label.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Configure ttk style for rounded buttons
        self.style = ttk.Style()
        self.style.configure("Rounded.TButton",
                             font=("Arial", 10, "bold"),
                             foreground="#003366",
                             background="#f0f0f0",  # Transparent (matches parent background)
                             borderwidth=2,
                             relief="flat",
                             padding=10)
        self.style.map("Rounded.TButton", background=[("active", "#f0f0f0")])
        
        # Cadre des contrôles
        self.control_frame = tk.Frame(self.top_frame, bg="#f0f0f0")
        self.control_frame.pack(side=tk.RIGHT, padx=10)
        
        self.generate_button = ttk.Button(self.control_frame, text="Générer un tableau", command=self.generate_array, style="Rounded.TButton")
        self.generate_button.pack(pady=5)
        
        self.run_button = ttk.Button(self.control_frame, text="Lancer le tri", command=self.run_sort, style="Rounded.TButton")
        self.run_button.pack(pady=5)
        
        # Canevas pour l'animation - Bigger canvas
        self.canvas = tk.Canvas(self.frame, width=800, height=400, bg="white", highlightbackground="#707070")
        self.canvas.pack(padx=10, pady=10)
        
        self.array = []
        self.delay = 50  # délai en millisecondes pour l'animation
        
        self.generate_array()
    
    def generate_array(self):
        """Génère un tableau aléatoire et l'affiche."""
        self.array = [random.randint(10, 300) for _ in range(50)]
        self.draw_array()
    
    def draw_array(self, highlight_indices=None, swap_indices=None, sorted_index=None):
        """
        Dessine le tableau sous forme de barres verticales.
        - Par défaut, les barres sont en "#E0E0E0" avec une bordure "#004D99".
        - Les indices en cours de comparaison sont en "#CA6C0F" avec bordure "#732E00".
        - Les indices échangés s'affichent en rouge.
        - Les éléments triés sont en "#004D99" avec une bordure blanche.
        """
        self.canvas.delete("all")
        c_width = 800
        c_height = 400
        n = len(self.array)
        bar_width = c_width / n
        for i, val in enumerate(self.array):
            x0 = i * bar_width
            y0 = c_height - val
            x1 = (i + 1) * bar_width
            y1 = c_height
            
            color = "#E0E0E0"      # Couleur par défaut des barres
            border_color = "#004D99"  # Bordure par défaut
            
            if highlight_indices and i in highlight_indices:
                color = "#CA6C0F"  # Comparaison : orange foncé
                border_color = "#732E00"
            if swap_indices and i in swap_indices:
                color = "red"      # Indique un échange
            if sorted_index is not None and i <= sorted_index:
                color = "#004D99"  # Éléments triés en bleu foncé
                border_color = "#ffffff"
            
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline=border_color, width=2)
        self.master.update_idletasks()
    
    def run_sort(self):
        """Désactive les boutons puis lance l'algorithme de tri avec animation."""
        self.run_button.config(state="disabled")
        self.generate_button.config(state="disabled")
        self.sort_func(self.array, self.draw_array, self.delay)
        self.run_button.config(state="normal")
        self.generate_button.config(state="normal")

# ------------------------------
# Fonctions de tri avec animation
# ------------------------------

def selection_sort(arr, draw_callback, delay):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
            # Passer sorted_index = i-1 for already sorted portion
            draw_callback(highlight_indices=[i, j, min_idx], sorted_index=i-1)
            time.sleep(delay / 1000.0)
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        draw_callback(highlight_indices=[i, min_idx], sorted_index=i-1)
        time.sleep(delay / 1000.0)
        # Update the sorted portion (elements with indices <= i are sorted)
        draw_callback(sorted_index=i)
    draw_callback(sorted_index=n-1)

def insertion_sort(arr, draw_callback, delay):
    n = len(arr)
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            draw_callback(highlight_indices=[j, j + 1], sorted_index=i-1)
            time.sleep(delay / 1000.0)
            j -= 1
        arr[j + 1] = key
        draw_callback(highlight_indices=[j + 1], sorted_index=i)
        time.sleep(delay / 1000.0)

def quick_sort(arr, draw_callback, delay, low=0, high=None):
    if high is None:
        high = len(arr) - 1
    if low < high:
        pi = partition(arr, draw_callback, delay, low, high)
        quick_sort(arr, draw_callback, delay, low, pi - 1)
        quick_sort(arr, draw_callback, delay, pi + 1, high)

def partition(arr, draw_callback, delay, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
            draw_callback(highlight_indices=[i, j])
            time.sleep(delay / 1000.0)
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    draw_callback(highlight_indices=[i + 1, high])
    time.sleep(delay / 1000.0)
    return i + 1

def merge_sort(arr, draw_callback, delay, left=0, right=None):
    if right is None:
        right = len(arr) - 1
    if left < right:
        mid = (left + right) // 2
        merge_sort(arr, draw_callback, delay, left, mid)
        merge_sort(arr, draw_callback, delay, mid + 1, right)
        merge(arr, draw_callback, delay, left, mid, right)

def merge(arr, draw_callback, delay, left, mid, right):
    L = arr[left:mid + 1]
    R = arr[mid + 1:right + 1]
    i = j = 0
    k = left
    while i < len(L) and j < len(R):
        if L[i] < R[j]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        draw_callback(highlight_indices=[k])
        time.sleep(delay / 1000.0)
        k += 1
    while i < len(L):
        arr[k] = L[i]
        i += 1
        draw_callback(highlight_indices=[k])
        time.sleep(delay / 1000.0)
        k += 1
    while j < len(R):
        arr[k] = R[j]
        j += 1
        draw_callback(highlight_indices=[k])
        time.sleep(delay / 1000.0)
        k += 1

# =====================================================
# Textes Théoriques pour chaque Algorithme
# =====================================================

theory_texts = {
    "Selection Sort": "Selection Sort :\n\nPrincipe : Parcourir le tableau pour trouver l'élément minimum et le placer en première position, puis répéter pour le reste du tableau.\nComplexité : O(n²) dans le pire cas.",
    "Insertion Sort": "Insertion Sort :\n\nPrincipe : Construire progressivement une sous-liste triée en insérant chaque nouvel élément à sa position correcte.\nComplexité : O(n²) dans le pire cas.",
    "Quick Sort": "Quick Sort :\n\nPrincipe : Diviser le tableau autour d'un pivot et trier récursivement les sous-tableaux.\nComplexité : En moyenne O(n log n), mais O(n²) dans le pire cas.",
    "Merge Sort": "Merge Sort :\n\nPrincipe : Diviser le tableau en deux, trier récursivement les deux moitiés et fusionner les deux sous-tableaux triés.\nComplexité : O(n log n) dans tous les cas."
}

# =====================================================
# SECTION DE COMPARAISON (Benchmark et Graphique)
# =====================================================

def benchmark_algorithms():
    """
    Effectue un benchmark sur plusieurs tailles de tableaux et retourne une figure matplotlib.
    """
    sizes = [100, 500, 1000, 2000, 5000, 10000]
    algorithms = {
        "Selection Sort": selection_sort,
        "Insertion Sort": insertion_sort,
        # Pour le benchmark, on ne souhaite pas l'animation => délai 0 et fonction de dessin vide.
        "Quick Sort": lambda arr, draw, delay: quick_sort(arr, lambda cp: None, 0),
        "Merge Sort": lambda arr, draw, delay: merge_sort(arr, lambda cp: None, 0)
    }
    results = {name: [] for name in algorithms}
    for size in sizes:
        for name, func in algorithms.items():
            arr = [random.randint(1, size) for _ in range(size)]
            start = time.time()
            func(arr, lambda cp: None, 0)
            end = time.time()
            results[name].append(end - start)
    # Création du graphique avec une taille plus grande
    fig, ax = plt.subplots(figsize=(8, 6))
    for name, times in results.items():
        ax.plot(sizes, times, marker='o', label=name)
    ax.set_xlabel("Taille du tableau")
    ax.set_ylabel("Temps d'exécution (s)")
    ax.set_title("Comparaison des Algorithmes de Tri")
    ax.legend()
    return fig

class ComparisonFrame(tk.Frame):
    """
    Cadre pour afficher le benchmark et le graphique comparatif.
    """
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.info_label = tk.Label(self, text="Benchmark des algorithmes sur différentes tailles de tableaux", font=("Arial", 12))
        self.info_label.pack(pady=10)
        self.plot_button = tk.Button(self, text="Lancer le benchmark", command=self.run_benchmark)
        self.plot_button.pack(pady=5)
        self.canvas_frame = tk.Frame(self)
        self.canvas_frame.pack(fill="both", expand=True)
        self.canvas_widget = None
        
    def run_benchmark(self):
        fig = benchmark_algorithms()
        if self.canvas_widget:
            self.canvas_widget.get_tk_widget().destroy()
        self.canvas_widget = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        self.canvas_widget.draw()
        self.canvas_widget.get_tk_widget().pack(fill="both", expand=True)

# =====================================================
# SECTION QUIZ : Jeu pour tester les connaissances
# =====================================================

class QuizFrame(tk.Frame):
    """
    Cadre interactif pour un quiz sur les algorithmes de tri.
    """
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.questions = [
            {
                "question": "Quel est l'algorithme le plus efficace en moyenne ?",
                "options": ["Selection Sort", "Insertion Sort", "Quick Sort", "Merge Sort"],
                "answer": "Quick Sort"
            },
            {
                "question": "Quel algorithme utilise le principe de diviser pour régner ?",
                "options": ["Insertion Sort", "Quick Sort", "Selection Sort", "Bubble Sort"],
                "answer": "Quick Sort"
            }
        ]
        self.current_question = 0
        self.score = 0
        
        self.question_label = tk.Label(self, text="", font=("Arial", 12))
        self.question_label.pack(pady=10)
        self.options_var = tk.StringVar()
        self.options = []
        for i in range(4):
            rb = tk.Radiobutton(self, text="", variable=self.options_var, value="", font=("Arial", 10))
            rb.pack(anchor="w")
            self.options.append(rb)
        self.submit_button = tk.Button(self, text="Valider", command=self.check_answer)
        self.submit_button.pack(pady=5)
        self.feedback_label = tk.Label(self, text="", font=("Arial", 10))
        self.feedback_label.pack(pady=5)
        self.next_button = tk.Button(self, text="Question Suivante", command=self.next_question, state="disabled")
        self.next_button.pack(pady=5)
        
        self.load_question()
        
    def load_question(self):
        q = self.questions[self.current_question]
        self.question_label.config(text=q["question"])
        self.options_var.set(None)
        for i, option in enumerate(q["options"]):
            self.options[i].config(text=option, value=option)
        self.feedback_label.config(text="")
        self.next_button.config(state="disabled")
        self.submit_button.config(state="normal")
        
    def check_answer(self):
        selected = self.options_var.get()
        correct = self.questions[self.current_question]["answer"]
        if selected == correct:
            self.feedback_label.config(text="Bonne réponse !")
            self.score += 1
        else:
            self.feedback_label.config(text=f"Mauvaise réponse. La bonne réponse était : {correct}")
        self.submit_button.config(state="disabled")
        self.next_button.config(state="normal")
        
    def next_question(self):
        self.current_question += 1
        if self.current_question >= len(self.questions):
            self.question_label.config(text=f"Quiz terminé ! Votre score : {self.score}/{len(self.questions)}")
            for rb in self.options:
                rb.pack_forget()
            self.submit_button.pack_forget()
            self.next_button.pack_forget()
        else:
            self.load_question()

# =====================================================
# APPLICATION PRINCIPALE AVEC SIDEBAR
# =====================================================

class SortingApp:
    """
    Application principale : affiche une sidebar permettant de naviguer entre
    les différentes sections (chaque algorithme, comparaison et quiz).
    """
    def __init__(self, master):
        self.master = master
        master.title("Visualisation des Algorithmes de Tri")
        master.geometry("900x600")
        
        # Sidebar
        self.sidebar = tk.Frame(master, width=200, bg="#f0f0f0")
        self.sidebar.pack(side=tk.LEFT, fill="y")
        
        # Zone de contenu principale
        self.content_frame = tk.Frame(master)
        self.content_frame.pack(side=tk.RIGHT, fill="both", expand=True)
        
        # Boutons de navigation dans la sidebar
        self.buttons = {}
        sections = ["Selection Sort", "Insertion Sort", "Quick Sort", "Merge Sort", "Comparison", "Quiz"]
        for sec in sections:
            btn = tk.Button(self.sidebar, text=sec, command=lambda s=sec: self.show_section(s))
            btn.pack(fill="x", padx=10, pady=5)
            self.buttons[sec] = btn
        
        self.section_frame = None
        self.show_section("Selection Sort")
        
    def show_section(self, section):
        """Affiche la section sélectionnée en détruisant la précédente."""
        if self.section_frame:
            self.section_frame.destroy()
        if section in ["Selection Sort", "Insertion Sort", "Quick Sort", "Merge Sort"]:
            if section == "Selection Sort":
                vis = SortingVisualizer(self.content_frame, section, selection_sort, theory_texts[section])
            elif section == "Insertion Sort":
                vis = SortingVisualizer(self.content_frame, section, insertion_sort, theory_texts[section])
            elif section == "Quick Sort":
                vis = SortingVisualizer(self.content_frame, section, quick_sort, theory_texts[section])
            elif section == "Merge Sort":
                vis = SortingVisualizer(self.content_frame, section, merge_sort, theory_texts[section])
            self.section_frame = vis.frame
        elif section == "Comparison":
            self.section_frame = ComparisonFrame(self.content_frame)
        elif section == "Quiz":
            self.section_frame = QuizFrame(self.content_frame)

# =====================================================
# LANCEMENT DE L'APPLICATION
# =====================================================

if __name__ == "__main__":
    root = tk.Tk()
    app = SortingApp(root)
    root.mainloop()
