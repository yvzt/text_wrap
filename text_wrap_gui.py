# tex_wrap_gui.py
# A tiny LaTeX wrapper utility:
# - Select text in the big box
# - Click a rule (e.g., \textcolor{<cursor>}{<selection>})
# - The selection gets wrapped and cursor jumps to where you type the parameter

import tkinter as tk
from tkinter import ttk

# Optional: ttkbootstrap for a nicer modern theme (falls back to plain ttk if missing)
try:
  import ttkbootstrap as tb
  from ttkbootstrap.constants import *
  BOOTSTRAP = True
except Exception:
  BOOTSTRAP = False


CURSOR = "<CURSOR>"
SEL = "<SEL>"


DEFAULT_RULES = [
  # You said you'll populate this list. Add/edit freely.
  # Template must contain <SEL>. <CURSOR> marks where the caret should end up.
  ("textcolor", r"\textcolor{" + CURSOR + r"}{" + SEL + r"}"),
  ("textbf", r"\textbf{" + SEL + r"}"),
  ("emph", r"\emph{" + SEL + r"}"),
  ("underline", r"\underline{" + SEL + r"}"),
  ("mathrm", r"\mathrm{" + SEL + r"}"),
  ("colorbox", r"\colorbox{" + CURSOR + r"}{" + SEL + r"}"),
]


class TexWrapApp:
  def __init__(self, root):
    self.root = root
    self.root.title("LaTeX Wrapper Utility")

    self.rules = DEFAULT_RULES[:]  # you can load these from file later if needed

    self._build_ui()
    self._populate_rules()

  def _build_ui(self):
    self.root.columnconfigure(0, weight=1)
    self.root.rowconfigure(0, weight=1)

    main = ttk.Frame(self.root, padding=10)
    main.grid(row=0, column=0, sticky="nsew")
    main.columnconfigure(0, weight=4)
    main.columnconfigure(1, weight=1)
    main.rowconfigure(1, weight=1)

    # Header row
    title = ttk.Label(main, text="Select text, then click a rule to wrap it.")
    title.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))

    # Left: big text box + scrollbar
    left = ttk.Frame(main)
    left.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
    left.columnconfigure(0, weight=1)
    left.rowconfigure(0, weight=1)

    self.text = tk.Text(
      left,
      wrap="word",          # vertical scroll only, wraps long lines
      undo=True,
      height=24
    )
    self.text.grid(row=0, column=0, sticky="nsew")

    yscroll = ttk.Scrollbar(left, orient="vertical", command=self.text.yview)
    yscroll.grid(row=0, column=1, sticky="ns")
    self.text.configure(yscrollcommand=yscroll.set)

    # Right: rules list + buttons
    right = ttk.Frame(main)
    right.grid(row=1, column=1, sticky="nsew")
    right.columnconfigure(0, weight=1)
    right.rowconfigure(1, weight=1)

    ttk.Label(right, text="Rules").grid(row=0, column=0, sticky="w")

    self.rule_list = tk.Listbox(right, height=14)
    self.rule_list.grid(row=1, column=0, sticky="nsew", pady=(6, 8))

    # Double-click applies, single-click + button also works
    self.rule_list.bind("<Double-Button-1>", self.apply_selected_rule)

    btns = ttk.Frame(right)
    btns.grid(row=2, column=0, sticky="ew")
    btns.columnconfigure(0, weight=1)
    btns.columnconfigure(1, weight=1)

    apply_btn = ttk.Button(btns, text="Apply", command=self.apply_selected_rule)
    apply_btn.grid(row=0, column=0, sticky="ew", padx=(0, 6))

    clear_btn = ttk.Button(btns, text="Clear", command=self.clear_text)
    clear_btn.grid(row=0, column=1, sticky="ew")

    # Hint block
    hint = ttk.Label(
      right,
      text="Tip: If nothing is selected,\nrule skeleton is inserted.\nCursor jumps to <CURSOR>.",
      justify="left"
    )
    hint.grid(row=3, column=0, sticky="w", pady=(10, 0))

  def _populate_rules(self):
    self.rule_list.delete(0, tk.END)
    for name, _tmpl in self.rules:
      self.rule_list.insert(tk.END, name)
    if self.rules:
      self.rule_list.selection_set(0)

  def clear_text(self):
    self.text.delete("1.0", tk.END)
    self.text.focus_set()

  def _get_current_rule(self):
    sel = self.rule_list.curselection()
    if not sel:
      return None
    idx = int(sel[0])
    return self.rules[idx]

  def apply_selected_rule(self, _event=None):
    rule = self._get_current_rule()
    if rule is None:
      return

    name, template = rule

    # Determine selection (if any)
    has_selection = False
    try:
      sel_start = self.text.index("sel.first")
      sel_end = self.text.index("sel.last")
      selected_text = self.text.get(sel_start, sel_end)
      has_selection = True
    except tk.TclError:
      selected_text = ""

    # Build insertion text
    insertion = template.replace(SEL, selected_text)

    # Where should cursor land?
    cursor_pos_in_insertion = insertion.find(CURSOR)
    if cursor_pos_in_insertion == -1:
      # No <CURSOR> marker -> put cursor at end of inserted text
      cursor_pos_in_insertion = len(insertion)
      insertion_clean = insertion
    else:
      insertion_clean = insertion.replace(CURSOR, "")

    self.text.edit_separator()

    if has_selection:
      # Replace selected text with wrapped text
      self.text.delete(sel_start, sel_end)
      insert_at = sel_start
      self.text.insert(insert_at, insertion_clean)
    else:
      # Insert at current caret
      insert_at = self.text.index("insert")
      self.text.insert(insert_at, insertion_clean)

    # Move caret to the intended cursor location
    # Compute target index by adding character offset from insert_at
    target = f"{insert_at}+{cursor_pos_in_insertion}c"
    self.text.mark_set("insert", target)
    self.text.see("insert")
    self.text.focus_set()

    self.text.edit_separator()


def main():
  if BOOTSTRAP:
    root = tb.Window(themename="flatly")
  else:
    root = tk.Tk()
    # basic ttk theme (best effort)
    try:
      ttk.Style().theme_use("clam")
    except Exception:
      pass

  app = TexWrapApp(root)
  root.minsize(850, 500)
  root.mainloop()


if __name__ == "__main__":
  main()
