import vapoursynth as vs
from vapoursynth import core
import adptvgrnMod as agm
from functools import partial
import math
from vsutil import plane, get_subsampling, get_depth, split, join, scale_value
from vsutil import depth as Depth
from rekt import rektlvl, rektlvls, rekt_fast
import awsmfunc as awf

def DebandReader(clip, csvfile, range=30, delimiter=' ', mask=None, luma_scaling=15):
    """
    DebandReader, read a csv file to apply a f3kdb filter for given strengths and frames. From awsmfunc.
    > Usage: DebandReader(clip, csvfile, grain, range)
      * csvfile is the path to a csv file containing in each row: <startframe> <endframe> <<strength_y>,**<strength_b>,**<strength_r>> <grain strength>
      * grain is passed as grainy and grainc in the adptvgrnMod filter
      * range is passed as range in the f3kdb filter
    """
    import csv

    filtered = clip if get_depth(clip) <= 16 else Depth(clip, 16)
    depth = get_depth(clip)

    with open(csvfile) as debandcsv:
        csvzones = csv.reader(debandcsv, delimiter=delimiter)
        for row in csvzones:
            strength = row[2].split(',')
            while len(strength) < 3:
                strength.append(strength[-1])
            grain_strength = float(row[3])
            db = core.f3kdb.Deband(clip, y=strength[0], cb=strength[1], cr=strength[2], grainy=0, grainc=0,
                                    range=range, output_depth=depth)
            db = agm.adptvgrnMod(db,luma_scaling=luma_scaling,strength=grain_strength)
            filtered = awf.ReplaceFrames(filtered, db, mappings="[" + row[0] + " " + row[1] + "]")

        if mask:
            filtered = core.std.MaskedMerge(clip, filtered, mask)

    return filtered

