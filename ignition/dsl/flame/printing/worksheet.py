"""Worksheet printer class"""

from ..tensors.printers import latex_print

from .printer import TemplatePrinter

class WorksheetPrinter (TemplatePrinter):
    """Basic FLAME worksheet printer class"""

    _rule_print_attr = "_str"

    def __init__ (self, gen_obj, filename=None, template="worksheet.mako", **kws):
        print "WorksheetPrinter(gen_obj, " + template + ", " + str(filename) + ")"
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

    def _tensor_print(self, expr):
        return str(expr)

    def _list_ten_print (self, l_o_t):
        if isinstance(l_o_t, (list, tuple)):
            return "[ " + " and ".join(map(self._list_ten_print, l_o_t)) + " ]"
        else:
            return self._tensor_print(l_o_t)

    def _print_rules(self, part_dict, rule_dict, reverse=False):
        ret_str = ""
        for obj, part in part_dict.iteritems():
            p = rule_dict[obj].__getattribute__(self._rule_print_attr)
            if reverse:
                ret_str += "%s <- %s\n" % (self._tensor_print(obj), p(part))
            else:
                ret_str += "%s -> %s\n" % (self._tensor_print(obj), p(part))
        return ret_str

    @property
    def _after_update (self):
        return self._list_ten_print(self._gen_obj.aft_eqns)

    @property
    def _before_update (self):
        return self._list_ten_print(self._gen_obj.b4_eqns)

    @property
    def _invariant (self):
        return self._list_ten_print(self._gen_obj.loop_inv)

    @property
    def _guard (self):
        return " and ".join(map(self._tensor_print, self._gen_obj.guard)) + \
               " is/are not empty"

    @property
    def _fuse (self):
        return self._print_rules(self._gen_obj.partition,
                                 self._gen_obj.fuse_fun, reverse=True)

    @property
    def _operation (self):
        return str(self._gen_obj.op_applied)

    @property
    def _outputs (self):
        return ", ".join(map(lambda x: str(x.obj), self._gen_obj.outputs))

    @property
    def _precondition (self):
        return self._invariant

    @property
    def _postcondition (self):
        return self._invariant + " and " + self._guard

    @property
    def _partition (self):
        return self._print_rules(self._gen_obj.partition,
                                 self._gen_obj.part_fun)

    @property
    def _partition_sizes (self):
        return ""

    @property
    def _repartition (self):
        return self._print_rules(self._gen_obj.partition,
                                 self._gen_obj.repart_fun)

    @property
    def _reparition_sizes (self):
        return ""

    @property
    def _sizes (self):
        return ", ".join(map(lambda x: str(x.obj.shape), self._gen_obj.outputs))

    @property
    def _update (self):
        if self._gen_obj.update is None:
            return "UPDATES NOT DETERMINED."
        ret_str = ""
        for k, v in self._gen_obj.update.iteritems():
            ret_str += "%s = %s\n" % (self._tensor_print(k),
                                      self._tensor_print(v))
        return ret_str

class LatexWorksheetPrinter (WorksheetPrinter):

    _tensor_printer = latex_print
    _rule_print_attr = "_latex"


    def __init__ (self, gen_obj, filename=None):
        WorksheetPrinter.__init__(self, gen_obj, filename, "flatex.mako")

    @property
    def template_dict(self):
        td = super(LatexWorksheetPrinter, self).template_dict
        td["caption"] = "None"
        td["label"] = "none"
        return td

    def _tensor_print(self, expr):
        return latex_print(expr)

    def _print_rules(self, part_dict, rule_dict, reverse=False):
        ret_str = ""
        for obj, part in part_dict.iteritems():
            p = rule_dict[obj].__getattribute__(self._rule_print_attr)
            arrow = "\rightarrow"
            if reverse:
                arrow = "\leftarrow"
            ret_str += "%s %s %s\n" % (self._tensor_print(obj), arrow, p(part))
        return ret_str
