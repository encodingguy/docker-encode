import vapoursynth as vs
import mvsfunc as mvf
import fvsfunc as fvf
import math
from functools import partial
core=vs.get_core()
def ReplaceFrames(clipa, clipb, mappings=None, filename=None):
    """
    ReplaceFramesSimple wrapper that attempts to use the plugin version with a fallback to fvsfunc.
    https://github.com/Irrational-Encoding-Wizardry/Vapoursynth-RemapFrames
    :param clipa: Main clip.
    :param clipb: Filtered clip to splice into main clip.
    :param mappings: String of frames to be replaced, e.g. "[0 500] [1000 1500]".
    :param filename: File with frames to be replaced.
    :return: clipa with clipb spliced in according to specified frames.
    """
    try:
        return core.remap.Rfs(baseclip=clipa, sourceclip=clipb, mappings=mappings, filename=filename)
    except AttributeError:
        return fvf.rfs(clipa, clipb, mappings, filename)
def solarcurve(input):
    core = vs.get_core()
    clip=input
    funcName = 'solarcurve'

    clip=mvf.ToRGB(clip,depth=8)
    pi=math.pi
    t = 5
    k = 5.5
    A = -1/4194304*(k*pi - 128/t)
    B = 3/32768*(k*pi - 128/t)
    C = 1/t
    def curveR(x):
        a=round(127.9999*math.sin(A*(x)**3 + B*(x)**2 + C**(x) ) + 127.5)
        return a
    def curveG(x):
        a=round(127.9999*math.sin(A*(x-5)**3 + B*(x-5)**2 + C**(x-5)) + 127.5)
        return a
    def curveB(x):
        a=round(127.9999*math.sin(A*(x+5)**3 + B*(x+5)**2 + C**(x+5)) + 127.5)
        return a
    clip = core.std.Lut(clip=clip, planes=[0], function=curveR)
    clip = core.std.Lut(clip=clip, planes=[1], function=curveG)
    clip = core.std.Lut(clip=clip, planes=[2], function=curveB)
    clip=mvf.ToYUV(clip,depth=8)
    return clip
def FrameInfo(clip, title,
              style="sans-serif,20,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,0,7,10,10,10,1"):
    """
    FrameInfo. From sgvsfunc, with additional style option.
    > Usage: FrameInfo(clip, title)
      * Print the frame number, the picture type and a title on each frame
    """
    core = vs.get_core()
    def FrameProps(n, clip):
        if "_PictType" in clip.get_frame(n).props:
            clip = core.sub.Subtitle(clip, "Frame " + str(n) + " of " + str(
                clip.num_frames) + "\nPicture type: " + clip.get_frame(n).props._PictType.decode(), style=style)
        else:
            clip = core.sub.Subtitle(clip, "Frame " + str(n) + " of " + str(clip.num_frames) + "\nPicture type: N/A",
                                     style=style)

        return clip

    clip = core.std.FrameEval(clip, partial(FrameProps, clip=clip))
    clip = core.sub.Subtitle(clip, text=['\n \n' + title], style=style)
    return clip
def readbanding(clip,filepaht,delimiter=' '):
    import csv
    bandclip=FrameInfo(clip,'Band')
    with open(filepaht) as debandcsv:
        csvzones = csv.reader(debandcsv, delimiter=delimiter)
        for row in csvzones:
            clip = ReplaceFrames(clip, bandclip, mappings="[" + row[0] + " " + row[1] + "]")
    return clip
def readrpf(clip,fixlist,filepaht,delimiter=' '):
    import csv
    with open(filepaht) as debandcsv:
        csvzones = csv.reader(debandcsv, delimiter=delimiter)
        for row in csvzones:
            fl=fixlist[int(row[2])-1]
            clip = ReplaceFrames(clip, fl, mappings="[" + row[0] + " " + row[1] + "]")
    return clip



