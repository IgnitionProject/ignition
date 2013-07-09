from ..pobj import PObj
from ..tensors import Tensor
import iterative_prules

PART_SUFFIX_DEFAULT = "3x3"

def get_part_suffix(fun):
    name = str(fun.__class__).split('.')[-1].strip("'>")
    idx = name.find('_')
    if idx < 0:
        raise ValueError("Unable to determine part suffix from: %s" % fun)
    return name[idx + 1:]

def iterative_arg(name, rank, *args, **kws):
    ten = Tensor(name, rank)
    arg_src = kws.get("arg_src", PObj.ARG_SRC["Input"])
    if type(arg_src) is str:
        arg_src = PObj.ARG_SRC[arg_src]
    part_suffix = kws.get("part_suffix", None)
    part_fun = kws.get("part_fun", None)
    repart_fun = kws.get("repart_fun", None)
    fuse_fun = kws.get("fuse_fun", None)
    if part_suffix is None:
        part_suffix = PART_SUFFIX_DEFAULT
        if part_fun is not None:
            part_suffix = get_part_suffix(part_fun.__name__)
        elif repart_fun is not None:
            part_suffix = get_part_suffix(repart_fun.__name__)
        elif fuse_fun is not None:
            part_suffix = get_part_suffix(fuse_fun.__name__)
    if part_fun is None:
        try:
            part_fun = getattr(iterative_prules, "Part_" + part_suffix)()
        except AttributeError:
            raise ValueError("Unable to find partition function for argument.")
    if repart_fun is None:
        try:
            repart_fun = getattr(iterative_prules, "Repart_" + part_suffix)()
        except AttributeError:
            raise ValueError("Unable to find repartition function for argument.")
    if fuse_fun is None:
        try:
            fuse_fun = getattr(iterative_prules, "Fuse_" + part_suffix)()
        except AttributeError:
            raise ValueError("Unable to find fuse function for argument.")
    return PObj(ten, part_fun=part_fun, repart_fun=repart_fun,
                fuse_fun=fuse_fun, arg_src=arg_src)

