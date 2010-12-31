"""Worksheet Printer """

from printer import TemplatePrinter

class WorksheetPrinter (TemplatePrinter):
    """Basic FLAME worksheet printer class"""

    def __init__ (self, gen_obj, template="worksheet.mako", filename=None, **kws):
        TemplatePrinter.__init__(self, template, filename)
        self._gen_obj = gen_obj

    @property
    def template_dict(self):
        return {"outputs" : self._outputs,
                "sizes" : self._sizes,
                "operation" : self._operation,
                "precondition" : self._precondition,
                "postcondition" : self._postcondition,
                "partition" : self._partition,
                "partition_sizes" : self._partition_sizes,
                "repartition" : self._repartition,
                "repartition_sizes" : self._reparition_sizes,
                "fuse" : self._fuse,
                "guard" : self._guard,
                "invariant" : self._invariant,
                "before_update" : self._before_update,
                "after_update" : self._after_update,
                "update" : self._update,
                }

    @property
    def _after_update (self):
        return str(self._gen_obj.aft_eqns)

    @property
    def _before_update (self):
        return str(self._gen_obj.b4_eqns)

    @property
    def _invariant (self):
        return str(self._gen_obj.loop_inv)

    @property
    def _guard (self):
        return "" #str(self._gen_obj.guard)

    @property
    def _fuse (self):
        return ""

    @property
    def _operation (self):
        return ""

    @property
    def _outputs (self):
        return ", ".join(map(lambda x: str(x.obj), self._gen_obj.outputs))

    @property
    def _precondition (self):
        return ""

    @property
    def _postcondition (self):
        return ""

    @property
    def _partition (self):
        return ""

    @property
    def _partition_sizes (self):
        return ""

    @property
    def _repartition (self):
        return ""

    @property
    def _reparition_sizes (self):
        return ""

    @property
    def _sizes (self):
        return ", ".join(map(lambda x: str(x.obj.shape), self._gen_obj.outputs))

    @property
    def _update (self):
        return str(self._gen_obj.update)

class LatexWorksheetPrinter (WorksheetPrinter):

    def __init__ (self, gen_obj, filename=None):
        WorksheetPrinter.__init__(self, gen_obj, "flatex.mako", filename)

    @property
    def template_dict(self):
        td = super(LatexWorksheetPrinter, self).template_dict
        td["caption"] = "None"
        td["label"] = "none"
        return td



