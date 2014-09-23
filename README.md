tkvis
=========

## Screenshots

### Tk Visualiser

![Tk Visualiser](resources/images/label_visualiser.png)

The widget hierarchy for the hosted app is shown in a listbox, with the selected widget and its parent highlighted.

A visual indication of four key pack arguments (`side`, `anchor`, `fill`, and `expand`) is displayed below the listbox.

On the right, the actual position of the widget and its parent are shown.
In addition, any wasted space from the geometry manager is highlighted.
This is useful for detecting bugs which arise from, for example, mixing `side` arguments to pack.

### Hosted App

![Hosted App](resources/images/label_app.png)

The selected widget as well as its parent are highlighted.

## Usage

Copy the code you wish to visualise into the same directory as `tkvis.py` (or otherwise give it access to the module).

Replace all references to `Tkinter` with references to `tkvis`, eg:

    import Tkinter as tk  # -> import tkvis as tk
    from Tkinter import * # -> from tkvis import *

## Configuration

Configuration settings (including colour choices) are available in `config.py`.

## Notes

Only the pack geometry manager is supported.
