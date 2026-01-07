# LaTeX Inline Wrapper Utility (Python GUI)

A small, focused Python GUI tool for wrapping selected LaTeX text with common inline commands
(e.g. `\textcolor{}`, `\textbf{}`, `\emph{}`, or custom macros) in a fast, repeatable, and editor-agnostic way.

This tool is designed primarily for **teaching material preparation** (Beamer slides, lecture notes,
worked examples), where frequent inline emphasis is required and manual typing becomes error-prone
or cognitively disruptive.

The application provides:
- A large, scrollable text workspace
- A user-defined list of LaTeX wrapper rules
- One-click wrapping of selected text
- Automatic cursor placement at the intended parameter location (e.g. colour name)

The philosophy is deliberately simple:
**no LaTeX parsing, no document structure awareness, no automation beyond text wrapping.**

---

## Key Features

- Large text box with:
  - Vertical scrolling
  - Horizontal word wrapping (no horizontal scroll)
- Rule-based wrapping:
  - Select text → click a rule → text is wrapped
- Explicit cursor control:
  - Cursor jumps to the parameter position (e.g. inside `{}` for colour name)
- Fully editable rule list:
  - You define the LaTeX commands and templates
- Lightweight and portable:
  - Pure Python
  - Uses Tkinter (optionally ttkbootstrap for styling)

---

## Intended Use Cases

- Beamer slide preparation
- Lecture notes with heavy inline notation
- Educational figures with colour-coded text references
- Any workflow where LaTeX is written **outside** the editor’s macro system

This tool intentionally does **not**:
- Parse LaTeX syntax
- Understand environments or math mode
- Replace proper editor macros

It complements editors like **TeXstudio**, not replaces them.

---

## Contents

- `tex_wrap_gui.py` — main application file

---

## Installation

### Requirements
- Python 3.8+
- Standard library only (Tkinter is included with Python)

Optional (recommended for nicer UI):
- `ttkbootstrap`

Install ttkbootstrap (optional):

```bash
pip install ttkbootstrap
