"""
Textual tab allowing the editing of placeholder values.

The main goal of this tab is to allow the placeholder values
to be changed from that included within the user-provied `FileTree`.
These changes are immediately made into the `FileTree`.
"""
import numpy as np
from textual.app import App, ComposeResult
from textual.containers import Grid, Vertical
from textual.widgets import Button, Footer, Header, Input, Label

from .all_panes import AllPanes, PipelineSelector


class PlaceholderEditor(App):
    """
    GUI to view pipeline.

    There are two separate pages (visiblity set by `show_page`):
    - `placeholder_tab` allows the user to change the placeholder values.
    - `output_tab` allows the user to select the requested output files.
    """

    TITLE = "FSL pipeline"
    CSS_PATH = "css/placeholder.css"

    def __init__(self, selector: PipelineSelector):
        """Create the pipeline GUI."""
        super().__init__()
        self.selector = selector
        self.file_tree = selector.file_tree

    def compose(self) -> ComposeResult:
        """Build the pipeline GUI."""
        self.keys = [Label(k) for k in self.file_tree.placeholders.keys()]
        self.values = [
            Input(", ".join(v) if np.asarray(v).ndim == 1 else v)
            for v in self.file_tree.placeholders.values()
        ]

        table_parts = []
        for key, value in zip(self.keys, self.values):
            table_parts.append(key)
            table_parts.append(value)
        yield Header()
        yield Vertical(
            Label("step 1: optionally edit placeholder values"),
            Grid(Label("Placeholders"), Label("Values"), *table_parts, id="grid"),
            Button("Continue"),
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed):
        """Continue to the next app."""
        new_placeholders = {}
        for key, value in zip(self.keys, self.values):
            text = value.value
            if "," in text:
                new_value = [elem.strip() for elem in text.split(",")]
            else:
                new_value = text.strip()
            new_placeholders[str(key.renderable)] = new_value

        self.selector.update_placeholders(**new_placeholders)
        self.exit(AllPanes.SELECTOR)
