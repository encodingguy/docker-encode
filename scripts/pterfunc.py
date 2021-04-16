import vapoursynth as vs
from vapoursynth import core
import adptvgrnMod as agm
from functools import partial
import math
from vsutil import plane, get_subsampling, get_depth, split, join, scale_value
from vsutil import depth as Depth
from rekt import rektlvl, rektlvls, rekt_fast
import awsmfunc as awf
import havsfunc as haf


def solarcurve(clip, color='24'):
    """Add a solar curve filter to clip, default is 24 colorspace.From https://github.com/jack2game/solarcurve"""
    t = 5
    k = 5.5
    m = (k * math.pi - 128 / t)
    A = -1 / 4194304 * m
    B = 3 / 32768 * m
    C = 1 / t

    def solar(clip):
        if clip.format is None:
            raise vs.Error("Tweak: only clips with constant format are accepted.")

        if clip.format.color_family == vs.RGB:
            raise vs.Error("Tweak: RGB clips are not accepted.")

        output = core.resize.Spline36(clip=clip, format=vs.RGB24, matrix_in_s="709")
        output = core.std.Lut(clip=output, planes=[0], function=solar24r)
        output = core.std.Lut(clip=output, planes=[1], function=solar24g)
        output = core.std.Lut(clip=output, planes=[2], function=solar24b)
        return core.resize.Spline36(clip=output, format=clip.format, matrix_s="709")

    def solar48(clip):
        if clip.format is None:
            raise vs.Error("Tweak: only clips with constant format are accepted.")

        if clip.format.color_family == vs.RGB:
            raise vs.Error("Tweak: RGB clips are not accepted.")

        output = core.resize.Spline36(clip=clip, format=vs.RGB48, matrix_in_s="709")
        output = core.std.Lut(clip=output, planes=[0], function=solar48r)
        output = core.std.Lut(clip=output, planes=[1], function=solar48g)
        output = core.std.Lut(clip=output, planes=[2], function=solar48b)
        return core.resize.Spline36(clip=output, format=clip.format, matrix_s="709")

    def solar24r(x):
        return round(127.9999 * math.sin(A * (x) ** 3 + B * (x) ** 2 + C * (x) - math.pi / 2) + 127.5)

    def solar24g(x):
        return round(127.9999 * math.sin(A * (x - 5) ** 3 + B * (x - 5) ** 2 + C * (x - 5) - math.pi / 2) + 127.5)

    def solar24b(x):
        return round(127.9999 * math.sin(A * (x + 5) ** 3 + B * (x + 5) ** 2 + C * (x + 5) - math.pi / 2) + 127.5)

    def solar48r(x):
        return round((127.9999 * math.sin(A * (x / 65535 * 255) ** 3 + B * ((x / 65535 * 255)) ** 2 + C * (
        (x / 65535 * 255)) - math.pi / 2) + 127.5) ** 2)

    def solar48g(x):
        return round((127.9999 * math.sin(A * ((x / 65535 * 255) - 5) ** 3 + B * ((x / 65535 * 255) - 5) ** 2 + C * (
                    (x / 65535 * 255) - 5) - math.pi / 2) + 127.5) ** 2)

    def solar48b(x):
        return round((127.9999 * math.sin(A * ((x / 65535 * 255) + 5) ** 3 + B * ((x / 65535 * 255) + 5) ** 2 + C * (
                    (x / 65535 * 255) + 5) - math.pi / 2) + 127.5) ** 2)

    if color == '24':
        return solar(clip)
    elif color == '48':
        return solar48(clip)
    else:
        raise vs.Error('Only accepts 24 or 48 as parameter')


# def solarcurve(input,css='420'):
# '''Whalehu's solarcurve'''
#     core = vs.get_core()
#     clip = input

#     clip = mvf.ToRGB(clip,depth=8)
#     pi = math.pi
#     t = 5
#     k = 5.5
#     A = -1/4194304*(k*pi - 128/t)
#     B = 3/32768*(k*pi - 128/t)
#     C = 1/t
#     def curveR(x):
#         a=round(127.9999*math.sin(A*(x)**3 + B*(x)**2 + C**(x) ) + 127.5)
#         return a
#     def curveG(x):
#         a=round(127.9999*math.sin(A*(x-5)**3 + B*(x-5)**2 + C**(x-5)) + 127.5)
#         return a
#     def curveB(x):
#         a=round(127.9999*math.sin(A*(x+5)**3 + B*(x+5)**2 + C**(x+5)) + 127.5)
#         return a
#     clip = core.std.Lut(clip=clip, planes=[0], function=curveR)
#     clip = core.std.Lut(clip=clip, planes=[1], function=curveG)
#     clip = core.std.Lut(clip=clip, planes=[2], function=curveB)
#     clip = mvf.ToYUV(clip,depth=8,css=css)
#     return clip


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
            db = agm.adptvgrnMod(db, luma_scaling=luma_scaling, strength=grain_strength)
            filtered = awf.ReplaceFrames(filtered, db, mappings="[" + row[0] + " " + row[1] + "]")

        if mask:
            filtered = core.std.MaskedMerge(clip, filtered, mask)

    return filtered


def InterleaveDir(folder, PrintInfo=False, DelProp=False, first=None, repeat=False, tonemap=False, solar_curve=False):
    """
    InterleaveDir, load all mkv files located in a directory and interleave them. From awsmfunc,add a solar curve option.
    > Usage: InterleaveDir(folder, PrintInfo, DelProp, first, repeat)
      * folder is the folder path
      * PrintInfo = True prints the frame number, picture type and file name on each frame
      * DelProp = True means deleting primaries, matrix and transfer characteristics
      * first is an optional clip to append in first position of the interleaving list
      * repeat = True means that the appended clip is repeated between each loaded clip from the folder
      * tonemap = True tonemaps each clip before applying FrameInfo
      * solar_curve = True if you want to usr a solar curve fliter to those clips
    """
    import os

    files = sorted(os.listdir(folder))
    first = first if solar_curve is False else solarcurve(first)
    if first != None:
        sources = [first]
        j = 0
    else:
        sources = []
        j = -1

    for i in range(len(files)):

        if files[i].endswith('.mkv'):

            j = j + 1
            sources.append(0)
            sources[j] = core.ffms2.Source(folder + '/' + files[i])

            if first != None:
                sources[j] = core.std.AssumeFPS(clip=sources[j], src=first)

            if tonemap:
                sources[j] = awf.DynamicTonemap(sources[j], libplacebo=False)

            if solar_curve is True:
                sources[j] = solarcurve(sources[j])

            if PrintInfo == True:
                sources[j] = awf.FrameInfo(clip=sources[j], title=files[i])
            elif PrintInfo != False:
                raise TypeError('InterleaveDir: PrintInfo must be a boolean.')

            if DelProp == True:
                sources[j] = awf.DelFrameProp(sources[j])
            elif DelProp != False:
                raise TypeError('InterleaveDir: DelProp must be a boolean.')

            if first != None and repeat == True:
                j = j + 1
                sources.append(0)
                sources[j] = first
            elif first != None and repeat != False:
                raise TypeError('InterleaveDir: repeat must be a boolean.')

    return core.std.Interleave(sources)


def debandmask(clip, lo=6144, hi=12288, lothr=320, hithr=384, mrad=2):
    """A luma adraptive mask from https://pastebin.com/SHQZjVJ5
     meant as a faster version of the retinex-type deband mask
     lo and hi are the cutoffs for luma
     lothr and hithr are the Binarize thresholds of the mask at lo/hi luma levels
     luma values falling between lo and hi are scaled linearly from lothr to hithr"""
    f = clip.format
    bits = f.bits_per_sample
    isINT = f.sample_type == vs.INTEGER

    peak = (1 << bits) - 1 if isINT else 1
    clip = clip.std.ShufflePlanes(0, vs.GRAY)

    ma = haf.mt_expand_multi(clip, mode='ellipse', sw=mrad, sh=mrad)
    mi = haf.mt_inpand_multi(clip, mode='ellipse', sw=mrad, sh=mrad)

    rmask = core.std.Expr([ma, mi], 'x y -')

    mexpr = 'x {lo} < y {lothr} >= {peak} 0 ? x {hi} > y {hithr} >= {peak} 0 ? y x {lo} - {r} / {tr} * {lothr} + >= {peak} 0 ? ? ?'.format(
        lo=lo, hi=hi, lothr=lothr, hithr=hithr, peak=peak, r=hi - lo, tr=hithr - lothr)

    return core.std.Expr([clip, rmask], mexpr)


def multy(img, multy):
    '''A simple tool to help generate screenshots, return a list need to take screenshots. Useful for comparison'''
    out = img.copy()
    for i in img:
        a = 0
        while a <= multy - 1:
            if a == 0:
                out.remove(i)
            out.append(i * multy + a)
            a += 1
    out.sort()
    return (out)
