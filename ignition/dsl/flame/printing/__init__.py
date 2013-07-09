"""Module defining whole program printers for generator objects."""

import os

FLAME_TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")

from printer import get_printer, TemplatePrinter
from worksheet import LatexWorksheetPrinter, WorksheetPrinter
