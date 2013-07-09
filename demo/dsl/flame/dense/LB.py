"""Example for Rule B=L*B"""

from ignition.dsl.flame import *


class LBRule (OpRule):
    """The LB rule
    
    B = L * B where L is Lower Triangular
    
    For more information on creating operation rules see rules.OpRule
    """

    def __init__ (self):
        OpRule.__init__(self)

    part_size = "2x2"

    def PME (self, L, B):
        [[L_tl, _], \
         [L_bl, L_br]] = L
        [[B_tl, B_tr], \
         [B_bl, B_br]] = B
        return [[              L_tl * B_tl, L_tl * B_tr],
                [L_bl * B_tl + L_br * B_bl, L_bl * B_tr + L_br * B_br]]

    def inv_1 (self, L, B):
        [[L_tl, _], \
         [   _, _]] = L
        [[B_tl, B_tr], \
         [B_bl, B_br]] = B
        return [[L_tl * B_tl, B_tr],
                [B_bl       , B_br ]]

    apply = inv_1


class LBRule_1 (OpRule):

    def __init__ (self):
        OpRule.__init__(self)

    part_size = ["2x2", "2x1"]

    def PME (self, L, B):
        [[L_tl, _], \
         [L_bl, L_br]] = L
        [[B_t],
         [B_b]] = B
        return [[            L_tl * B_t],
                [L_bl * B_t + L_br * B_b]]

    def inv_1 (self, L, B):
#        print "LBRule_1:inv_1, L =", list(L)
#        print "LBRule_1:inv_1, B =", list(B)
        [[L_tl, _], \
         [   _, _]] = L
        [[B_t],
         [B_b]] = B
#        print "LBRule_1:inv_1, L_tl =", L_tl, type(L_tl)
#        print "LBRule_1:inv_1, B_t =", B_t
#        print "L_tl * B_t =", L_tl * B_t
#        print "B_b = ", B_b
        return [[L_tl * B_t],
                [B_b]]

    apply = inv_1

class LBRule_2 (OpRule):

    def __init__ (self):
        OpRule.__init__(self)

    part_size = ["2x1", "1x2"]

    def PME (self, L, B):
        [[L_t],
         [L_b]] = L
        [[B_l, B_r]] = B
        return [[L_t * B_l, L_t * B_r],
                [L_b * B_l, L_b * B_r]]

    def inv_1 (self, L, B):
        [[L_t], \
         [L_b]] = L
        [[B_l, B_r]] = B
        return [[L_t * B_l, L_t * B_r],
                [L_b * B_l, B_r]]

    apply = inv_1

def main ():
    """Main routine to drive example"""

    # Create the argument object, see Worksheet.worksheet_args
    L = worksheet_arg("L", "LowerTriangular", "BR")
    B = worksheet_arg("B", "BR", "Overwrite")

    # Create the Worksheet and generate run the automating scripts
    w = Worksheet(LBRule(), L, B)
    w.run()

#    print [list(i) for i in w.repart_b4]
#    print list(w.repart_aft)
#    print list(w.LHS_repart_b4)
#    print list(w.RHS_repart_b4)
#    print list(w.LHS_repart_aft)
#    print list(w.RHS_repart_aft)
    print w.updates
    # Print out worksheet to desired format (determined by suffix)
    #w.to_file("lu_worksheet.tex")
    #w.to_file("lu_worksheet.c")
    #w.to_file("lu_worksheet.m")

    # Create the Worksheet and generate run the automating scripts
    # Create the argument object, see Worksheet.worksheet_args
    L = worksheet_arg("L", "LowerTriangular", "BR", "2x2")
    B = worksheet_arg("B", "BOTTOM", "Overwrite", "2x1")
#    print B
    w_1 = Worksheet(LBRule_1(), L, B)
    w_1.run()
    print w_1.updates


#    L = worksheet_arg("L", "LowerTriangular", "BOTTOM", "2x1")
#    B = worksheet_arg("B", "RIGHT", "Overwrite", "1x2")
##    print B
#    w_2 = Worksheet(LBRule_2(), L, B)
#    w_2.run()
#    print w_2.updates

if __name__ == "__main__":
    main()
