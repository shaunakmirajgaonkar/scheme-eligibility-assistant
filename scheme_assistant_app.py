"""
Government-Scheme Eligibility Assistant
100% local, offline Tkinter desktop app.
No internet connection, no API keys, no external services required.

Run:
    python scheme_assistant_app.py
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

from schemes_data import SCHEMES, OCCUPATIONS, LOCATIONS, GENDERS
from eligibility_engine import check_eligibility

HISTORY_FILE = "eligibility_history.json"

# ---------- Color palette (high contrast, all text clearly visible) ----------
COLORS = {
    "bg_main": "#0f172a",        # deep navy
    "bg_panel": "#1e293b",       # slate panel
    "bg_card": "#ffffff",        # white cards for readability
    "accent_blue": "#3b82f6",
    "accent_green": "#22c55e",
    "accent_amber": "#f59e0b",
    "accent_red": "#ef4444",
    "accent_purple": "#a855f7",
    "text_light": "#f8fafc",
    "text_dark": "#0f172a",
    "text_muted": "#64748b",
    "border": "#334155",
}

FONT_TITLE = ("Segoe UI", 22, "bold")
FONT_SUBTITLE = ("Segoe UI", 11)
FONT_SECTION = ("Segoe UI", 14, "bold")
FONT_LABEL = ("Segoe UI", 10, "bold")
FONT_BODY = ("Segoe UI", 10)
FONT_SMALL = ("Segoe UI", 9)
FONT_BTN = ("Segoe UI", 11, "bold")


class SchemeAssistantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Government-Scheme Eligibility Assistant")
        self.root.geometry("1180x760")
        self.root.minsize(1000, 650)
        self.root.configure(bg=COLORS["bg_main"])

        self.user_data = {}
        self.results = []

        self._build_header()
        self._build_tabs()

    # ------------------------------------------------------------------ UI
    def _build_header(self):
        header = tk.Frame(self.root, bg=COLORS["bg_panel"], height=90)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        title_frame = tk.Frame(header, bg=COLORS["bg_panel"])
        title_frame.pack(side="left", padx=25, pady=10)

        tk.Label(
            title_frame, text="\U0001F3DB Government-Scheme Eligibility Assistant",
            font=FONT_TITLE, bg=COLORS["bg_panel"], fg=COLORS["text_light"]
        ).pack(anchor="w")

        tk.Label(
            title_frame,
            text="100% Local & Offline  \u2022  No Internet Required  \u2022  Your data never leaves this device",
            font=FONT_SUBTITLE, bg=COLORS["bg_panel"], fg=COLORS["accent_green"]
        ).pack(anchor="w")

        badge = tk.Label(
            header, text="\u25CF OFFLINE MODE", font=("Segoe UI", 10, "bold"),
            bg=COLORS["accent_green"], fg="#ffffff", padx=14, pady=6
        )
        badge.pack(side="right", padx=25)

    def _build_tabs(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("TNotebook", background=COLORS["bg_main"], borderwidth=0)
        style.configure(
            "TNotebook.Tab", background=COLORS["bg_panel"], foreground=COLORS["text_light"],
            padding=[18, 10], font=FONT_LABEL
        )
        style.map(
            "TNotebook.Tab",
            background=[("selected", COLORS["accent_blue"])],
            foreground=[("selected", "#ffffff")]
        )

        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=15, pady=15)

        self.tab_form = tk.Frame(notebook, bg=COLORS["bg_main"])
        self.tab_results = tk.Frame(notebook, bg=COLORS["bg_main"])
        self.tab_browse = tk.Frame(notebook, bg=COLORS["bg_main"])
        self.tab_history = tk.Frame(notebook, bg=COLORS["bg_main"])

        notebook.add(self.tab_form, text="  \U0001F4DD Check Eligibility  ")
        notebook.add(self.tab_results, text="  \u2705 Results  ")
        notebook.add(self.tab_browse, text="  \U0001F4DA Browse All Schemes  ")
        notebook.add(self.tab_history, text="  \U0001F553 History  ")

        self.notebook = notebook
        self._build_form_tab()
        self._build_browse_tab()
        self._build_history_tab()
        self._refresh_history()

    # ------------------------------------------------------------ FORM TAB
    def _build_form_tab(self):
        canvas = tk.Canvas(self.tab_form, bg=COLORS["bg_main"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.tab_form, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=COLORS["bg_main"])

        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw", width=1130)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        card = tk.Frame(scroll_frame, bg=COLORS["bg_card"], padx=30, pady=25)
        card.pack(fill="x", padx=10, pady=10)

        tk.Label(
            card, text="Tell us about yourself", font=FONT_SECTION,
            bg=COLORS["bg_card"], fg=COLORS["text_dark"]
        ).grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 15))

        self.vars = {}
        r = 1

        # Age
        self._add_label(card, "Age *", r, 0)
        self.vars["age"] = tk.StringVar()
        tk.Entry(card, textvariable=self.vars["age"], font=FONT_BODY, width=15,
                  bg="#f1f5f9", fg=COLORS["text_dark"]).grid(row=r, column=1, sticky="w", padx=10, pady=8)

        # Gender
        self._add_label(card, "Gender *", r, 2)
        self.vars["gender"] = tk.StringVar(value=GENDERS[0])
        ttk.Combobox(card, textvariable=self.vars["gender"], values=GENDERS,
                     state="readonly", font=FONT_BODY, width=18).grid(row=r, column=3, sticky="w", padx=10, pady=8)
        r += 1

        # Occupation
        self._add_label(card, "Occupation *", r, 0)
        self.vars["occupation"] = tk.StringVar(value=OCCUPATIONS[0])
        ttk.Combobox(card, textvariable=self.vars["occupation"], values=OCCUPATIONS,
                     state="readonly", font=FONT_BODY, width=18).grid(row=r, column=1, sticky="w", padx=10, pady=8)

        # Location
        self._add_label(card, "Location *", r, 2)
        self.vars["location"] = tk.StringVar(value=LOCATIONS[0])
        ttk.Combobox(card, textvariable=self.vars["location"], values=LOCATIONS,
                     state="readonly", font=FONT_BODY, width=18).grid(row=r, column=3, sticky="w", padx=10, pady=8)
        r += 1

        # Annual income
        self._add_label(card, "Annual Family Income (Rs.) *", r, 0)
        self.vars["annual_income"] = tk.StringVar()
        tk.Entry(card, textvariable=self.vars["annual_income"], font=FONT_BODY, width=15,
                  bg="#f1f5f9", fg=COLORS["text_dark"]).grid(row=r, column=1, sticky="w", padx=10, pady=8)

        # Has bank account
        self._add_label(card, "Has Bank Account?", r, 2)
        self.vars["has_bank_account"] = tk.BooleanVar(value=True)
        tk.Checkbutton(card, variable=self.vars["has_bank_account"], bg=COLORS["bg_card"],
                        activebackground=COLORS["bg_card"]).grid(row=r, column=3, sticky="w", padx=10, pady=8)
        r += 1

        # Checkboxes row
        self._add_label(card, "Additional Details", r, 0)
        r += 1
        checks = [
            ("land_owner", "Owns Agricultural Land"),
            ("bpl_card", "Has BPL / Below-Poverty-Line Card"),
            ("owns_pucca_house", "Owns a Pucca (concrete) House"),
            ("is_student", "Currently a Student"),
            ("is_pregnant_or_lactating", "Pregnant / Lactating Mother"),
        ]
        col = 0
        for key, label in checks:
            self.vars[key] = tk.BooleanVar(value=False)
            tk.Checkbutton(
                card, text=label, variable=self.vars[key], font=FONT_BODY,
                bg=COLORS["bg_card"], fg=COLORS["text_dark"], activebackground=COLORS["bg_card"],
                selectcolor="#e2e8f0"
            ).grid(row=r, column=col, columnspan=2, sticky="w", padx=10, pady=6)
            col += 2
            if col >= 4:
                col = 0
                r += 1
        r += 1

        # Submit button
        btn_frame = tk.Frame(card, bg=COLORS["bg_card"])
        btn_frame.grid(row=r, column=0, columnspan=4, pady=20, sticky="w")

        tk.Button(
            btn_frame, text="\U0001F50D  Check My Eligibility", font=FONT_BTN,
            bg=COLORS["accent_blue"], fg="#ffffff", activebackground="#2563eb",
            activeforeground="#ffffff", relief="flat", padx=25, pady=12, cursor="hand2",
            command=self.run_check
        ).pack(side="left", padx=(0, 10))

        tk.Button(
            btn_frame, text="\u21BB  Clear Form", font=FONT_BTN,
            bg=COLORS["text_muted"], fg="#ffffff", activebackground="#475569",
            activeforeground="#ffffff", relief="flat", padx=20, pady=12, cursor="hand2",
            command=self.clear_form
        ).pack(side="left")

        note = tk.Label(
            scroll_frame,
            text="\u2139 All fields marked * are required. Your details are only used locally to match scheme rules and are never uploaded anywhere.",
            font=FONT_SMALL, bg=COLORS["bg_main"], fg=COLORS["text_muted"], wraplength=1000, justify="left"
        )
        note.pack(fill="x", padx=20, pady=(0, 20))

    def _add_label(self, parent, text, row, col):
        tk.Label(
            parent, text=text, font=FONT_LABEL, bg=COLORS["bg_card"], fg=COLORS["text_dark"]
        ).grid(row=row, column=col, sticky="w", padx=10, pady=8)

    def clear_form(self):
        self.vars["age"].set("")
        self.vars["annual_income"].set("")
        self.vars["gender"].set(GENDERS[0])
        self.vars["occupation"].set(OCCUPATIONS[0])
        self.vars["location"].set(LOCATIONS[0])
        self.vars["has_bank_account"].set(True)
        for key in ["land_owner", "bpl_card", "owns_pucca_house", "is_student", "is_pregnant_or_lactating"]:
            self.vars[key].set(False)

    # ------------------------------------------------------------- ACTIONS
    def run_check(self):
        try:
            age = int(self.vars["age"].get())
            income = float(self.vars["annual_income"].get())
        except (ValueError, TypeError):
            messagebox.showerror("Missing Information", "Please enter a valid Age and Annual Income (numbers only).")
            return

        if age <= 0 or age > 120:
            messagebox.showerror("Invalid Age", "Please enter a realistic age.")
            return

        user = {
            "age": age,
            "annual_income": income,
            "gender": self.vars["gender"].get(),
            "occupation": self.vars["occupation"].get(),
            "location": self.vars["location"].get(),
            "has_bank_account": self.vars["has_bank_account"].get(),
            "land_owner": self.vars["land_owner"].get(),
            "bpl_card": self.vars["bpl_card"].get(),
            "owns_pucca_house": self.vars["owns_pucca_house"].get(),
            "is_student": self.vars["is_student"].get(),
            "is_pregnant_or_lactating": self.vars["is_pregnant_or_lactating"].get(),
        }

        self.user_data = user
        self.results = check_eligibility(user)
        self._render_results()
        self._save_history(user, self.results)
        self._refresh_history()
        self.notebook.select(self.tab_results)

    # ---------------------------------------------------------- RESULTS TAB
    def _build_results_placeholder(self, parent):
        for w in parent.winfo_children():
            w.destroy()
        tk.Label(
            parent, text="Fill the 'Check Eligibility' form and click 'Check My Eligibility'\nto see your matched schemes here.",
            font=FONT_SECTION, bg=COLORS["bg_main"], fg=COLORS["text_muted"], justify="center"
        ).pack(expand=True, pady=100)

    def _render_results(self):
        parent = self.tab_results
        for w in parent.winfo_children():
            w.destroy()

        canvas = tk.Canvas(parent, bg=COLORS["bg_main"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=COLORS["bg_main"])

        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw", width=1130)
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        likely = [r for r in self.results if r["status"] == "Likely Eligible"]
        possible = [r for r in self.results if r["status"] == "Possibly Eligible"]

        summary = tk.Frame(scroll_frame, bg=COLORS["bg_panel"], padx=20, pady=15)
        summary.pack(fill="x", padx=10, pady=10)
        tk.Label(
            summary, text=f"\U0001F3AF {len(likely)} Likely Eligible   \u2022   {len(possible)} Possibly Eligible   \u2022   {len(self.results)} Schemes Checked",
            font=FONT_SECTION, bg=COLORS["bg_panel"], fg=COLORS["text_light"]
        ).pack(anchor="w")

        for r in self.results:
            self._build_result_card(scroll_frame, r)

    def _build_result_card(self, parent, r):
        status = r["status"]
        color_map = {
            "Likely Eligible": COLORS["accent_green"],
            "Possibly Eligible": COLORS["accent_amber"],
            "Unlikely Eligible": COLORS["accent_red"],
        }
        badge_color = color_map.get(status, COLORS["text_muted"])
        scheme = r["scheme"]

        card = tk.Frame(parent, bg=COLORS["bg_card"], padx=20, pady=16)
        card.pack(fill="x", padx=10, pady=8)

        top = tk.Frame(card, bg=COLORS["bg_card"])
        top.pack(fill="x")

        tk.Label(
            top, text=scheme["name"], font=("Segoe UI", 13, "bold"),
            bg=COLORS["bg_card"], fg=COLORS["text_dark"], wraplength=750, justify="left"
        ).pack(side="left", anchor="w")

        badge = tk.Label(
            top, text=f"{status}  ({r['match_pct']}%)", font=("Segoe UI", 9, "bold"),
            bg=badge_color, fg="#ffffff", padx=10, pady=4
        )
        badge.pack(side="right")

        tk.Label(
            card, text=f"Category: {scheme['category']}", font=FONT_SMALL,
            bg=COLORS["bg_card"], fg=COLORS["accent_blue"]
        ).pack(anchor="w", pady=(6, 2))

        tk.Label(
            card, text=scheme["description"], font=FONT_BODY, bg=COLORS["bg_card"],
            fg=COLORS["text_dark"], wraplength=1050, justify="left"
        ).pack(anchor="w", pady=(2, 8))

        tk.Label(
            card, text=f"\U0001F4B0 Benefit: {scheme['benefit']}", font=FONT_BODY,
            bg=COLORS["bg_card"], fg=COLORS["text_dark"], wraplength=1050, justify="left"
        ).pack(anchor="w", pady=2)

        docs_text = "\U0001F4C4 Documents Required: " + ", ".join(scheme["documents"])
        tk.Label(
            card, text=docs_text, font=FONT_BODY, bg=COLORS["bg_card"],
            fg=COLORS["text_dark"], wraplength=1050, justify="left"
        ).pack(anchor="w", pady=2)

        tk.Label(
            card, text=f"\U0001F5A5 How to Apply: {scheme['apply_mode']}", font=FONT_BODY,
            bg=COLORS["bg_card"], fg=COLORS["text_dark"], wraplength=1050, justify="left"
        ).pack(anchor="w", pady=2)

        if r["reasons"]:
            reasons_text = "\u26A0 Gaps to address: " + " | ".join(r["reasons"])
            tk.Label(
                card, text=reasons_text, font=FONT_SMALL, bg=COLORS["bg_card"],
                fg=COLORS["accent_red"], wraplength=1050, justify="left"
            ).pack(anchor="w", pady=(6, 0))

    # ------------------------------------------------------------ BROWSE TAB
    def _build_browse_tab(self):
        canvas = tk.Canvas(self.tab_browse, bg=COLORS["bg_main"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.tab_browse, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=COLORS["bg_main"])

        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw", width=1130)
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        tk.Label(
            scroll_frame, text=f"\U0001F4DA All {len(SCHEMES)} Schemes in Local Database",
            font=FONT_SECTION, bg=COLORS["bg_main"], fg=COLORS["text_light"]
        ).pack(anchor="w", padx=15, pady=15)

        for scheme in SCHEMES:
            card = tk.Frame(scroll_frame, bg=COLORS["bg_card"], padx=20, pady=14)
            card.pack(fill="x", padx=10, pady=6)

            tk.Label(
                card, text=scheme["name"], font=("Segoe UI", 12, "bold"),
                bg=COLORS["bg_card"], fg=COLORS["text_dark"], wraplength=1050, justify="left"
            ).pack(anchor="w")

            tk.Label(
                card, text=f"Category: {scheme['category']}", font=FONT_SMALL,
                bg=COLORS["bg_card"], fg=COLORS["accent_purple"]
            ).pack(anchor="w", pady=(4, 2))

            tk.Label(
                card, text=scheme["description"], font=FONT_BODY, bg=COLORS["bg_card"],
                fg=COLORS["text_dark"], wraplength=1050, justify="left"
            ).pack(anchor="w", pady=2)

    # ----------------------------------------------------------- HISTORY TAB
    def _build_history_tab(self):
        top = tk.Frame(self.tab_history, bg=COLORS["bg_main"])
        top.pack(fill="x", padx=15, pady=15)

        tk.Label(
            top, text="\U0001F553 Your Past Eligibility Checks (stored locally)",
            font=FONT_SECTION, bg=COLORS["bg_main"], fg=COLORS["text_light"]
        ).pack(side="left")

        tk.Button(
            top, text="Clear History", font=FONT_SMALL, bg=COLORS["accent_red"], fg="#ffffff",
            relief="flat", padx=12, pady=6, cursor="hand2", command=self._clear_history
        ).pack(side="right")

        container = tk.Frame(self.tab_history, bg=COLORS["bg_main"])
        container.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        canvas = tk.Canvas(container, bg=COLORS["bg_main"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        self.history_frame = tk.Frame(canvas, bg=COLORS["bg_main"])

        self.history_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.history_frame, anchor="nw", width=1115)
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def _save_history(self, user, results):
        entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "age": user["age"],
            "occupation": user["occupation"],
            "annual_income": user["annual_income"],
            "likely_eligible_count": len([r for r in results if r["status"] == "Likely Eligible"]),
            "top_matches": [r["scheme"]["name"] for r in results[:3] if r["status"] != "Unlikely Eligible"],
        }
        history = self._load_history()
        history.append(entry)
        try:
            with open(HISTORY_FILE, "w", encoding="utf-8") as f:
                json.dump(history, f, indent=2)
        except Exception as e:
            print(f"Could not save history: {e}")

    def _load_history(self):
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return []
        return []

    def _clear_history(self):
        if messagebox.askyesno("Clear History", "Delete all locally stored eligibility check history?"):
            try:
                if os.path.exists(HISTORY_FILE):
                    os.remove(HISTORY_FILE)
            except Exception as e:
                print(f"Could not clear history: {e}")
            self._refresh_history()

    def _refresh_history(self):
        for w in self.history_frame.winfo_children():
            w.destroy()

        history = self._load_history()
        if not history:
            tk.Label(
                self.history_frame, text="No history yet. Run an eligibility check to see it logged here.",
                font=FONT_BODY, bg=COLORS["bg_main"], fg=COLORS["text_muted"]
            ).pack(pady=40)
            return

        for entry in reversed(history[-30:]):
            card = tk.Frame(self.history_frame, bg=COLORS["bg_card"], padx=18, pady=12)
            card.pack(fill="x", pady=6)

            tk.Label(
                card, text=entry["timestamp"], font=("Segoe UI", 9, "bold"),
                bg=COLORS["bg_card"], fg=COLORS["accent_blue"]
            ).pack(anchor="w")

            tk.Label(
                card,
                text=f"Age {entry['age']}  \u2022  {entry['occupation']}  \u2022  Income Rs. {entry['annual_income']:,.0f}  \u2022  {entry['likely_eligible_count']} likely-eligible schemes",
                font=FONT_BODY, bg=COLORS["bg_card"], fg=COLORS["text_dark"]
            ).pack(anchor="w", pady=(4, 0))

            if entry["top_matches"]:
                tk.Label(
                    card, text="Top matches: " + ", ".join(entry["top_matches"]),
                    font=FONT_SMALL, bg=COLORS["bg_card"], fg=COLORS["text_muted"],
                    wraplength=1050, justify="left"
                ).pack(anchor="w", pady=(4, 0))


def main():
    root = tk.Tk()
    app = SchemeAssistantApp(root)
    app._build_results_placeholder(app.tab_results)
    root.mainloop()


if __name__ == "__main__":
    main()
