import tkinter as tk
from tkinter import ttk, messagebox
import random
import math
import time
import json
import os
from datetime import datetime

# ── Estructura: Categorías → Sub-niveles ─────────────────────────────────────
CATEGORIAS = {
    "Sumas": {
        "icono": "➕",
        "subniveles": [
            {"nombre": "1 dígito + 1 dígito",   "op": "+", "rango_a": (1,9),    "rango_b": (1,9)},
            {"nombre": "2 dígitos + 1 dígito",   "op": "+", "rango_a": (10,99),  "rango_b": (1,9)},
            {"nombre": "2 dígitos + 2 dígitos",  "op": "+", "rango_a": (10,99),  "rango_b": (10,99)},
            {"nombre": "3 dígitos + 1 dígito",   "op": "+", "rango_a": (100,999),"rango_b": (1,9)},
            {"nombre": "3 dígitos + 2 dígitos",  "op": "+", "rango_a": (100,999),"rango_b": (10,99)},
            {"nombre": "3 dígitos + 3 dígitos",  "op": "+", "rango_a": (100,999),"rango_b": (100,999)},
        ]
    },
    "Restas": {
        "icono": "➖",
        "subniveles": [
            {"nombre": "1 dígito - 1 dígito",    "op": "-", "rango_a": (1,9),    "rango_b": (1,9)},
            {"nombre": "2 dígitos - 1 dígito",   "op": "-", "rango_a": (10,99),  "rango_b": (1,9)},
            {"nombre": "2 dígitos - 2 dígitos",  "op": "-", "rango_a": (10,99),  "rango_b": (10,99)},
            {"nombre": "3 dígitos - 1 dígito",   "op": "-", "rango_a": (100,999),"rango_b": (1,9)},
            {"nombre": "3 dígitos - 2 dígitos",  "op": "-", "rango_a": (100,999),"rango_b": (10,99)},
            {"nombre": "3 dígitos - 3 dígitos",  "op": "-", "rango_a": (100,999),"rango_b": (100,999)},
        ]
    },
    "Multiplicación": {
        "icono": "✖️",
        "subniveles": [
            {"nombre": "1 dígito × 1 dígito",   "op": "×", "rango_a": (1,9),    "rango_b": (1,9)},
            {"nombre": "2 dígitos × 1 dígito",   "op": "×", "rango_a": (10,99),  "rango_b": (1,9)},
            {"nombre": "2 dígitos × 2 dígitos",  "op": "×", "rango_a": (10,99),  "rango_b": (10,99)},
            {"nombre": "3 dígitos × 1 dígito",   "op": "×", "rango_a": (100,999),"rango_b": (1,9)},
            {"nombre": "3 dígitos × 2 dígitos",  "op": "×", "rango_a": (100,999),"rango_b": (10,99)},
        ]
    },
    "División": {
        "icono": "➗",
        "subniveles": [
            {"nombre": "1 dígito ÷ 1 dígito",   "op": "÷", "rango_a": (1,9),    "rango_b": (1,9)},
            {"nombre": "2 dígitos ÷ 1 dígito",   "op": "÷", "rango_a": (10,99),  "rango_b": (1,9)},
            {"nombre": "2 dígitos ÷ 2 dígitos",  "op": "÷", "rango_a": (10,99),  "rango_b": (10,99)},
            {"nombre": "3 dígitos ÷ 2 dígitos",  "op": "÷", "rango_a": (100,999),"rango_b": (10,99)},
        ]
    },
    "Fracciones": {
        "icono": "½",
        "subniveles": [
            {"nombre": "Numerador/denominador 1 dígito", "op": "frac", "rango_a": (2,9),  "rango_b": (2,9)},
            {"nombre": "Numerador/denominador 2 dígitos","op": "frac", "rango_a": (10,99),"rango_b": (10,99)},
        ]
    },
    "Desafío Final": {
        "icono": "🏆",
        "subniveles": [
            {"nombre": "Mezcla básica  (+, -, ×)",          "op": "mix", "rango_a": (1,9),    "rango_b": (1,9),    "ops_mix": ["+","-","×"]},
            {"nombre": "Mezcla media   (+, -, ×, ÷)",       "op": "mix", "rango_a": (10,99),  "rango_b": (1,9),    "ops_mix": ["+","-","×","÷"]},
            {"nombre": "Mezcla avanzada (+, -, ×, ÷, frac)","op": "mix", "rango_a": (10,99),  "rango_b": (10,99),  "ops_mix": ["+","-","×","÷","frac"]},
        ]
    },
}

PREGUNTAS_POR_SESION = 10
TIEMPO_POR_SESION = {
    "Sumas":          [60, 75, 90, 100, 110, 120],
    "Restas":         [60, 75, 90, 100, 110, 120],
    "Multiplicación": [75, 90, 110, 130, 150],
    "División":       [75, 90, 110, 150],
    "Fracciones":     [120, 180],
    "Desafío Final":  [120, 150, 180],
}

ARCHIVO_HISTORIAL = os.path.join(os.path.expanduser("~"), "math4u_historial.json")
ARCHIVO_PROGRESO  = os.path.join(os.path.expanduser("~"), "math4u_progreso.json")

C = {
    "bg":      "#0D1117",
    "surface": "#161B22",
    "card":    "#1C2330",
    "accent":  "#F7B731",
    "accent2": "#26A65B",
    "danger":  "#E74C3C",
    "text":    "#E6EDF3",
    "muted":   "#8B949E",
    "border":  "#30363D",
}

# ── Persistencia ──────────────────────────────────────────────────────────────
def cargar_json(path, default):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return default

def guardar_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def progreso_inicial():
    return {cat: 0 for cat in CATEGORIAS}

# ── Generación de preguntas ───────────────────────────────────────────────────
def simplificar(num, den):
    g = math.gcd(abs(num), abs(den))
    return num // g, den // g

def generar_pregunta(subnivel_cfg, usadas=None):
    if usadas is None:
        usadas = set()

    # Modo mezcla: elegir operación al azar entre las disponibles
    if subnivel_cfg["op"] == "mix":
        op_elegida = random.choice(subnivel_cfg["ops_mix"])
        cfg_temporal = dict(subnivel_cfg)
        cfg_temporal["op"] = op_elegida
        # Para fracciones en mix, usar rango como denominador
        if op_elegida == "frac":
            lo, hi = subnivel_cfg["rango_a"]
            cfg_temporal["rango_a"] = (max(2, lo), max(9, hi // 2))
            cfg_temporal["rango_b"] = (max(2, lo), max(9, hi // 2))
        return generar_pregunta(cfg_temporal, usadas)

    op   = subnivel_cfg["op"]
    lo_a, hi_a = subnivel_cfg["rango_a"]
    lo_b, hi_b = subnivel_cfg["rango_b"]

    intentos = 0
    while True:
        intentos += 1

        if op == "frac":
            den_a = random.randint(lo_a, hi_a)
            den_b = random.randint(lo_b, hi_b)
            while den_b == den_a:
                den_b = random.randint(lo_b, hi_b)
            num_a = random.randint(1, den_a - 1)
            num_b = random.randint(1, den_b - 1)
            clave = (min((num_a, den_a), (num_b, den_b)), "frac",
                     max((num_a, den_a), (num_b, den_b)))
            if clave not in usadas or intentos > 50:
                usadas.add(clave)
                den_comun = den_a * den_b // math.gcd(den_a, den_b)
                num_res = num_a * (den_comun // den_a) + num_b * (den_comun // den_b)
                num_res, den_comun = simplificar(num_res, den_comun)
                return ("frac", num_a, den_a, num_b, den_b), (num_res, den_comun)
            continue

        a = random.randint(lo_a, hi_a)
        b = random.randint(lo_b, hi_b)

        if op == "-":
            if a < b:
                a, b = b, a
        elif op == "÷":
            b = random.randint(max(1, lo_b), hi_b)
            factor = random.randint(1, max(1, hi_a // b))
            a = b * factor

        if op in ("+", "×"):
            clave = (min(a, b), op, max(a, b))
        else:
            clave = (a, op, b)

        if clave not in usadas or intentos > 50:
            usadas.add(clave)
            break

    if op == "+":   respuesta = a + b
    elif op == "-": respuesta = a - b
    elif op == "×": respuesta = a * b
    elif op == "÷": respuesta = a // b

    return (a, op, b), respuesta

# ── App ───────────────────────────────────────────────────────────────────────
class Math4UApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Math4U – Simulador de Matemáticas")
        self.geometry("760x600")
        self.resizable(False, False)
        self.configure(bg=C["bg"])

        self.historial = cargar_json(ARCHIVO_HISTORIAL, [])
        self.progreso  = cargar_json(ARCHIVO_PROGRESO, progreso_inicial())
        for cat in CATEGORIAS:
            if cat not in self.progreso:
                self.progreso[cat] = 0

        self.categoria_actual = None
        self.subnivel_actual  = 0
        self._build_ui()
        self.mostrar_menu()

    def _build_ui(self):
        hdr = tk.Frame(self, bg=C["surface"], height=60)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        tk.Label(hdr, text="✏  Math4U", font=("Courier New", 18, "bold"),
                 fg=C["accent"], bg=C["surface"]).pack(side="left", padx=20, pady=12)
        self.lbl_hdr = tk.Label(hdr, text="", font=("Courier New", 11),
                                fg=C["muted"], bg=C["surface"])
        self.lbl_hdr.pack(side="right", padx=20)
        self.frame_main = tk.Frame(self, bg=C["bg"])
        self.frame_main.pack(fill="both", expand=True, padx=30, pady=20)

    def _limpiar(self):
        for w in self.frame_main.winfo_children():
            w.destroy()

    # ── MENÚ PRINCIPAL ────────────────────────────────────────────────────────
    def mostrar_menu(self):
        self._limpiar()
        self.lbl_hdr.config(text="")
        f = self.frame_main

        tk.Label(f, text="Selecciona una opción", font=("Courier New", 13),
                 fg=C["muted"], bg=C["bg"]).pack(pady=(0, 16))

        for txt, cmd in [
            ("▶  Practicar",         self.mostrar_categorias),
            ("📊  Historial",         self.mostrar_historial),
            ("🗑  Limpiar historial", self.confirmar_limpiar),
        ]:
            tk.Button(f, text=txt, font=("Courier New", 12, "bold"),
                      fg=C["bg"], bg=C["accent"], activebackground="#e0a520",
                      relief="flat", cursor="hand2", pady=11,
                      command=cmd).pack(fill="x", pady=5)

        tk.Label(f, text="Progreso por categoría", font=("Courier New", 10),
                 fg=C["muted"], bg=C["bg"]).pack(pady=(20, 8))

        for cat, cfg in CATEGORIAS.items():
            total        = len(cfg["subniveles"])
            desbloqueado = min(self.progreso.get(cat, 0) + 1, total)
            row = tk.Frame(f, bg=C["bg"])
            row.pack(fill="x", pady=2)
            tk.Label(row, text=f"{cfg['icono']} {cat}",
                     font=("Courier New", 9), fg=C["text"], bg=C["bg"],
                     width=18, anchor="w").pack(side="left")
            ttk.Progressbar(row, maximum=total, value=desbloqueado,
                            length=320).pack(side="left", padx=6)
            tk.Label(row, text=f"{desbloqueado}/{total}",
                     font=("Courier New", 9), fg=C["muted"], bg=C["bg"]).pack(side="left")

    # ── SELECTOR DE CATEGORÍA ─────────────────────────────────────────────────
    def mostrar_categorias(self):
        self._limpiar()
        self.lbl_hdr.config(text="")
        f = self.frame_main

        tk.Label(f, text="¿Qué quieres practicar?", font=("Courier New", 14, "bold"),
                 fg=C["text"], bg=C["bg"]).pack(pady=(0, 20))

        grid = tk.Frame(f, bg=C["bg"])
        grid.pack()

        for i, (cat, cfg) in enumerate(CATEGORIAS.items()):
            total        = len(cfg["subniveles"])
            desbloqueado = min(self.progreso.get(cat, 0) + 1, total)
            tk.Button(grid,
                      text=f"{cfg['icono']}\n{cat}\n{desbloqueado}/{total} sub-niveles",
                      font=("Courier New", 10, "bold"),
                      fg=C["text"], bg=C["card"],
                      activebackground=C["surface"],
                      relief="flat", cursor="hand2",
                      width=14, height=4,
                      command=lambda c=cat: self.mostrar_subniveles(c)
                      ).grid(row=i // 3, column=i % 3, padx=8, pady=8)

        tk.Button(f, text="← Volver", font=("Courier New", 10),
                  fg=C["muted"], bg=C["bg"], relief="flat", cursor="hand2",
                  command=self.mostrar_menu).pack(pady=16)

    # ── SELECTOR DE SUB-NIVEL ─────────────────────────────────────────────────
    def mostrar_subniveles(self, categoria):
        self._limpiar()
        self.categoria_actual = categoria
        cfg = CATEGORIAS[categoria]
        f   = self.frame_main
        self.lbl_hdr.config(text=categoria)

        tk.Label(f, text=f"{cfg['icono']}  {categoria} – Elige un sub-nivel",
                 font=("Courier New", 13, "bold"), fg=C["text"], bg=C["bg"]).pack(pady=(0, 16))

        desbloqueado_idx = self.progreso.get(categoria, 0)

        for i, sub in enumerate(cfg["subniveles"]):
            bloqueado = i > desbloqueado_idx
            bg    = C["card"]    if not bloqueado else C["surface"]
            fg    = C["text"]    if not bloqueado else C["border"]
            sym   = f"  {i+1}. " if not bloqueado else "🔒 "
            state = "normal"     if not bloqueado else "disabled"
            tk.Button(f, text=f"{sym}{sub['nombre']}",
                      font=("Courier New", 11), fg=fg, bg=bg,
                      relief="flat", cursor="hand2" if not bloqueado else "arrow",
                      state=state, anchor="w", padx=16, pady=9,
                      command=lambda idx=i: self.iniciar_sesion(idx)
                      ).pack(fill="x", pady=3)

        tk.Button(f, text="← Volver", font=("Courier New", 10),
                  fg=C["muted"], bg=C["bg"], relief="flat", cursor="hand2",
                  command=self.mostrar_categorias).pack(pady=14)

    # ── SESIÓN DE EJERCICIOS ──────────────────────────────────────────────────
    def iniciar_sesion(self, subnivel_idx):
        self.subnivel_actual = subnivel_idx
        cat    = self.categoria_actual
        sub    = CATEGORIAS[cat]["subniveles"][subnivel_idx]
        tiempos = TIEMPO_POR_SESION[cat]
        tiempo  = tiempos[min(subnivel_idx, len(tiempos) - 1)]

        self.lbl_hdr.config(text=f"{cat}  ›  {sub['nombre']}")
        self._limpiar()
        f = self.frame_main

        self.preguntas_total   = PREGUNTAS_POR_SESION
        self.pregunta_actual   = 0
        self.correctas         = 0
        self.tiempo_inicio     = time.time()
        self.tiempo_limite     = tiempo
        self.tiempos_respuesta = []
        self._preguntas_usadas = set()
        self._es_fraccion      = False
        self._timer_activo     = True
        self._sub_cfg          = sub

        self.lbl_prog = tk.Label(f, text="", font=("Courier New", 10),
                                  fg=C["muted"], bg=C["bg"])
        self.lbl_prog.pack(anchor="e")

        self.lbl_crono = tk.Label(f, text="", font=("Courier New", 22, "bold"),
                                   fg=C["accent"], bg=C["bg"])
        self.lbl_crono.pack(pady=(2, 0))

        self.frame_op = tk.Frame(f, bg=C["bg"])
        self.frame_op.pack(pady=14)

        self.lbl_num_a = tk.Label(self.frame_op, text="",
                                   font=("Courier New", 44, "bold"),
                                   fg=C["text"], bg=C["bg"], anchor="e", width=8)
        self.lbl_num_a.grid(row=0, column=0, columnspan=2, sticky="e")

        self.lbl_op = tk.Label(self.frame_op, text="",
                                font=("Courier New", 44, "bold"),
                                fg=C["accent"], bg=C["bg"], anchor="w", width=2)
        self.lbl_op.grid(row=1, column=0, sticky="w")

        self.lbl_num_b = tk.Label(self.frame_op, text="",
                                   font=("Courier New", 44, "bold"),
                                   fg=C["text"], bg=C["bg"], anchor="e", width=7)
        self.lbl_num_b.grid(row=1, column=1, sticky="e")

        self.lbl_linea = tk.Label(self.frame_op, text="──────────",
                                   font=("Courier New", 18), fg=C["muted"], bg=C["bg"])
        self.lbl_linea.grid(row=2, column=0, columnspan=2, sticky="e")

        self.lbl_hint = tk.Label(f, text="", font=("Courier New", 9),
                                  fg=C["muted"], bg=C["bg"])
        self.lbl_hint.pack()

        self.entry = tk.Entry(f, font=("Courier New", 26), width=10,
                              justify="center", bg=C["card"], fg=C["text"],
                              insertbackground=C["accent"], relief="flat", bd=8)
        self.entry.pack(pady=6)
        self.entry.focus()
        self.entry.bind("<Return>", lambda e: self.verificar_respuesta())

        self.lbl_feedback = tk.Label(f, text="", font=("Courier New", 12), bg=C["bg"])
        self.lbl_feedback.pack(pady=4)

        tk.Button(f, text="Confirmar  ↵", font=("Courier New", 11, "bold"),
                  fg=C["bg"], bg=C["accent2"], activebackground="#1e8a48",
                  relief="flat", cursor="hand2", pady=8, padx=20,
                  command=self.verificar_respuesta).pack()

        self._siguiente_pregunta()
        self._actualizar_crono()

    def _siguiente_pregunta(self):
        self.pregunta_actual += 1
        self.lbl_prog.config(text=f"Pregunta {self.pregunta_actual} / {self.preguntas_total}")

        datos, self.respuesta_correcta = generar_pregunta(self._sub_cfg, self._preguntas_usadas)

        if datos[0] == "frac":
            _, num_a, den_a, num_b, den_b = datos
            self._es_fraccion = True
            self.lbl_num_a.config(text=f"{num_a}/{den_a}")
            self.lbl_op.config(text="+")
            self.lbl_num_b.config(text=f"{num_b}/{den_b}")
            self.lbl_hint.config(text="Escribe la respuesta como: numerador/denominador (simplificada)")
        else:
            self._es_fraccion = False
            a, op, b = datos
            self.lbl_num_a.config(text=str(a))
            self.lbl_op.config(text=op)
            self.lbl_num_b.config(text=str(b))
            self.lbl_hint.config(text="")

        self.lbl_feedback.config(text="", fg=C["text"])
        self.entry.delete(0, "end")
        self.entry.focus()
        self._t_inicio_preg = time.time()

    def verificar_respuesta(self):
        raw = self.entry.get().strip()
        if not raw:
            return

        elapsed = time.time() - self._t_inicio_preg
        self.tiempos_respuesta.append(round(elapsed, 2))

        if self._es_fraccion:
            if "/" not in raw:
                self.lbl_feedback.config(
                    text="⚠ Escribe como numerador/denominador  ej: 7/12", fg=C["accent"])
                self.tiempos_respuesta.pop()
                return
            try:
                num_r, den_r = map(int, raw.split("/"))
            except ValueError:
                self.lbl_feedback.config(text="⚠ Formato inválido. Ej: 7/12", fg=C["accent"])
                self.tiempos_respuesta.pop()
                return
            g = math.gcd(abs(num_r), abs(den_r))
            resp = (num_r // g, den_r // g)
        else:
            try:
                resp = int(raw)
            except ValueError:
                self.lbl_feedback.config(text="⚠ Escribe un número entero.", fg=C["accent"])
                self.tiempos_respuesta.pop()
                return

        if resp == self.respuesta_correcta:
            self.correctas += 1
            self.lbl_feedback.config(text="✓ ¡Correcto!", fg=C["accent2"])
        else:
            if self._es_fraccion:
                n, d = self.respuesta_correcta
                self.lbl_feedback.config(
                    text=f"✗ Incorrecto. Respuesta: {n}/{d}", fg=C["danger"])
            else:
                self.lbl_feedback.config(
                    text=f"✗ Incorrecto. Respuesta: {self.respuesta_correcta}", fg=C["danger"])

        self.after(900, self._avanzar)

    def _avanzar(self):
        if self.pregunta_actual < self.preguntas_total:
            self._siguiente_pregunta()
        else:
            self._timer_activo = False
            self.mostrar_resultado()

    def _actualizar_crono(self):
        if not self._timer_activo:
            return
        restante = self.tiempo_limite - int(time.time() - self.tiempo_inicio)
        if restante <= 0:
            self._timer_activo = False
            self.mostrar_resultado(tiempo_agotado=True)
            return
        self.lbl_crono.config(text=f"⏱  {restante}s",
                               fg=C["danger"] if restante <= 10 else C["accent"])
        self.after(500, self._actualizar_crono)

    # ── RESULTADO ─────────────────────────────────────────────────────────────
    def mostrar_resultado(self, tiempo_agotado=False):
        self._limpiar()
        f   = self.frame_main
        cat = self.categoria_actual
        sub = CATEGORIAS[cat]["subniveles"][self.subnivel_actual]

        total_t  = round(time.time() - self.tiempo_inicio, 1)
        pct      = round(self.correctas / self.preguntas_total * 100)
        aprobado = pct >= 80
        prom_t   = round(sum(self.tiempos_respuesta) / len(self.tiempos_respuesta), 1) \
                   if self.tiempos_respuesta else 0

        entrada = {
            "fecha":     datetime.now().strftime("%d/%m/%Y %H:%M"),
            "categoria": cat,
            "subnivel":  sub["nombre"],
            "correctas": self.correctas,
            "total":     self.preguntas_total,
            "pct":       pct,
            "tiempo_s":  total_t,
            "prom_seg":  prom_t,
            "aprobado":  aprobado,
        }
        self.historial.append(entrada)
        guardar_json(ARCHIVO_HISTORIAL, self.historial)

        if aprobado:
            idx_actual       = self.subnivel_actual
            max_desbloq      = self.progreso.get(cat, 0)
            total_subniveles = len(CATEGORIAS[cat]["subniveles"])
            if idx_actual == max_desbloq and idx_actual + 1 < total_subniveles:
                self.progreso[cat] = idx_actual + 1
                guardar_json(ARCHIVO_PROGRESO, self.progreso)

        emoji = "🏆" if aprobado else "📚"
        msg   = "¡Aprobado!" if aprobado else "Sigue practicando"
        color = C["accent2"] if aprobado else C["danger"]

        tk.Label(f, text=emoji, font=("Courier New", 46), bg=C["bg"]).pack(pady=(6, 0))
        tk.Label(f, text=msg, font=("Courier New", 19, "bold"),
                 fg=color, bg=C["bg"]).pack()

        if tiempo_agotado:
            tk.Label(f, text="⏱ Se agotó el tiempo", font=("Courier New", 10),
                     fg=C["danger"], bg=C["bg"]).pack()

        if aprobado and self.subnivel_actual + 1 < len(CATEGORIAS[cat]["subniveles"]):
            siguiente = CATEGORIAS[cat]["subniveles"][self.subnivel_actual + 1]["nombre"]
            tk.Label(f, text=f"🔓 Desbloqueado: {siguiente}",
                     font=("Courier New", 9), fg=C["accent2"], bg=C["bg"]).pack(pady=(2, 0))

        card = tk.Frame(f, bg=C["card"], padx=20, pady=14)
        card.pack(pady=12, padx=40, fill="x")
        for lbl, val in [
            ("Categoría",         cat),
            ("Sub-nivel",         sub["nombre"]),
            ("Correctas",         f"{self.correctas} / {self.preguntas_total}"),
            ("Porcentaje",        f"{pct}%"),
            ("Tiempo total",      f"{total_t}s"),
            ("Promedio/pregunta", f"{prom_t}s"),
        ]:
            row = tk.Frame(card, bg=C["card"])
            row.pack(fill="x", pady=1)
            tk.Label(row, text=lbl, font=("Courier New", 9),
                     fg=C["muted"], bg=C["card"]).pack(side="left")
            tk.Label(row, text=val, font=("Courier New", 9, "bold"),
                     fg=C["text"], bg=C["card"]).pack(side="right")

        btns = tk.Frame(f, bg=C["bg"])
        btns.pack(pady=8)
        for txt, cmd, bg in [
            ("🔄 Reintentar",  lambda: self.iniciar_sesion(self.subnivel_actual), C["accent"]),
            ("📋 Sub-niveles", lambda: self.mostrar_subniveles(cat),              C["card"]),
            ("🏠 Menú",        self.mostrar_menu,                                 C["card"]),
        ]:
            tk.Button(btns, text=txt, font=("Courier New", 10, "bold"),
                      fg=C["bg"] if bg == C["accent"] else C["text"],
                      bg=bg, relief="flat", cursor="hand2",
                      padx=10, pady=7, command=cmd).pack(side="left", padx=5)

    # ── HISTORIAL ─────────────────────────────────────────────────────────────
    def mostrar_historial(self):
        self._limpiar()
        f = self.frame_main
        tk.Label(f, text="📊 Historial de puntajes", font=("Courier New", 13, "bold"),
                 fg=C["text"], bg=C["bg"]).pack(pady=(0, 10))

        cols = ("Fecha", "Categoría", "Sub-nivel", "Resultado", "Tiempo")
        tree = ttk.Treeview(f, columns=cols, show="headings", height=13)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background=C["card"], foreground=C["text"],
                        fieldbackground=C["card"], rowheight=24, font=("Courier New", 8))
        style.configure("Treeview.Heading", background=C["surface"],
                        foreground=C["accent"], font=("Courier New", 8, "bold"))
        style.map("Treeview", background=[("selected", C["accent"])])

        for c, a in zip(cols, [100, 90, 170, 80, 60]):
            tree.heading(c, text=c)
            tree.column(c, width=a, anchor="center")

        for e in reversed(self.historial[-60:]):
            res = f"{e['correctas']}/{e['total']} ({e['pct']}%)"
            tag = "ok" if e["aprobado"] else "fail"
            tree.insert("", "end",
                        values=(e["fecha"], e.get("categoria", "–"),
                                e.get("subnivel", "–"), res, f"{e['tiempo_s']}s"),
                        tags=(tag,))

        tree.tag_configure("ok",   foreground=C["accent2"])
        tree.tag_configure("fail", foreground=C["danger"])
        tree.pack(fill="both", expand=True)

        tk.Button(f, text="← Volver", font=("Courier New", 10),
                  fg=C["muted"], bg=C["bg"], relief="flat", cursor="hand2",
                  command=self.mostrar_menu).pack(pady=8)

    def confirmar_limpiar(self):
        if messagebox.askyesno("Confirmar", "¿Eliminar todo el historial?"):
            self.historial = []
            guardar_json(ARCHIVO_HISTORIAL, self.historial)
            messagebox.showinfo("Listo", "Historial eliminado.")

# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = Math4UApp()
    app.mainloop()