"""Base printer objects."""

import sys

from mako.lookup import TemplateLookup

from ignition.dsl.flame.printing import FLAME_TEMPLATE_DIR

class TemplatePrinter (object):
    """Abstract printer class for using a Mako Template"""

    def __init__ (self, template, filename=None, **kws):
        self.template = template
        self.filename = filename

    def write(self):
        mylookup = TemplateLookup(FLAME_TEMPLATE_DIR)
        template = mylookup.get_template(self.template)
        if self.filename is None:
            fp = sys.stdout
        else:
            fp = open(self.filename, 'w')
        fp.write(template.render(**self.template_dict))
        if self.filename is not None:
            fp.close()

    @property
    def template_dict(self):
        return {}


def get_printer (gen_obj, filename=None, filetype=None):
    """Return printer based on file name extension"""
    if filename is None and filetype is None:
        return WorksheetPrinter(gen_obj)
    if filename:
        ext = filename[filename.rfind('.') + 1:]
    else:
        ext = None
    if filetype == "latex" or ext == "tex":
        return LatexWorksheetPrinter(gen_obj, filename)
    elif filetype == "text" or ext == "txt":
        return WorksheetPrinter(gen_obj, filename)

    raise ValueError, "Unable to determine file type from extension\n"\
                      "  given: %s" % filename

from worksheet import LatexWorksheetPrinter, WorksheetPrinter
