import vapoursynth as vs
import awsmfunc as awf
import kagefunc as kgf
from vsutil import *
import adptvgrnMod as adp
import havsfunc as haf
import pterfunc as ptf
import vardefunc as vaf

core = vs.core

# 0 Encode Flag
source_clip_path = r''  # The path of source clip
encode_clip_path = r''  # The path of encode clip
target_clip_path = [r'Target', '']  # First is The path of target clip and the second is the target clip's name
target_clips_path = {}  # For multiple clips,keys is the encode group and value is the path {"Handjob":r"/root/H.mkv"}
test_folder = r''  # The path of the test encodes
sample_extract = False  # True if you want to extract sample clip
sample_comparison = False  # True if you want to compare sample clip
encode_comparison = False  # True if you want to make a source vs encode

# 0 Init
if target_clip_path[1]:
    target_clips_path[target_clip_path[0]] = target_clip_path[1]

# 1 Import Source And Crop
if source_clip_path.endswith('.dgi'):
    src = core.dgdecodenv.DGSource(source_clip_path)
else:
    src = core.lsmas.LWLibavSource(source_clip_path)

if encode_comparison:
    if encode_clip_path.endswith('.dgi'):
        encode = core.dgdecodenv.DGSource(encode_clip_path)
    else:
        encode = core.lsmas.LWLibavSource(encode_clip_path)
else:
    encode = False

if encode_comparison and target_clips_path:
    target = [[i, core.dgdecodenv.DGSource(target_clips_path[i]) if target_clips_path[i].endswith('.dgi') else core.lsmas.LWLibavSource(target_clips_path[i])] for i in
              target_clips_path.keys()]
else:
    target = False

src = core.std.Crop(clip=src, top=0, bottom=0, left=0, right=0)  # Modify it with the even pixels to crop!
clip = depth(src, 16)

# 2 Filtering

# 2.1 Dirty lines & Borders
fix_borders = False
if fix_borders:
    fixed = awf.FixBrightnessProtect2(clip, row=[], adj_row=[], column=[], adj_column=[])
    fixed = awf.FillBorders(clip=clip, top=0, left=0,
                            right=0,
                            bottom=0)  # For 1080p only. If you're working on 720, please consider using CropResize!
    fixed = awf.bbmod(clip, top=0, bottom=0, left=0, right=0, thresh=0, blur=0)
else:
    fixed = clip

# 2.2 Resized
resize = False
if resize:
    resized = awf.CropResize(clip=fixed, preset=720)  # Resize the cilp and fill borders
    resized = awf.zresize(fixed, preset=720)
else:
    resized = fixed

# 2.3 Deband & Deblock
deband = False
if deband:
    mask = core.std.Binarize(resized, 5000)
    filtered = ptf.DebandReader(resized, 'merged-banding-frames.txt', mask=mask)
else:
    filtered = resized

# 2.4 Out!
test = False
if test:
    '''Any test here'''
    # Gama test area
    gama = awf.autogma(filtered)
    gama.set_output()
    filtered.set_output(index=1)

    # Upscale check
    downscale = awf.zresize(filtered, preset=720)
    rescale = awf.zresize(downscale, preset=1080)
    rescale = awf.FrameInfo(rescale, 'upscale')
    com = core.std.Interleave([rescale, filtered])
    com.set_output()
else:
    filtered = depth(filtered, 8)
    if sample_extract is False and encode_comparison is False:
        filtered.set_output()

# 3 Sample Extract & Comparison
if sample_extract:
    filtered = awf.FrameInfo(filtered,
                             'Filtered') if sample_comparison else filtered  # Tag original frameinfo if compare sample
    extract = awf.SelectRangeEvery(filtered, every=3000, length=50, offset=960) + ptf.banding_extract(filtered, 'csvfile')  # Modify it with the length to extract!
    if sample_comparison:
        comparison = ptf.InterleaveDir(folder=test_folder, PrintInfo=True, first=[extract], repeat=True)
        depth(comparison, 8).set_output()
    else:
        depth(extract, 8).set_output()

# 4 Source VS Encode
if encode_comparison:
    src = awf.FrameInfo(src, 'Source') if not resize else awf.FrameInfo(depth(awf.zresize(clip, preset=720), 8),
                                                                        'Source')
    filtered = awf.FrameInfo(filtered, 'Filtered')
    encode = awf.FrameInfo(encode, 'Encode')
    comparison_list = [src, filtered, encode]
    if target:
        target = [awf.FrameInfo(i[1], i[0]) for i in target]
        comparison_list.extend(target)
    comparison = core.std.Interleave(comparison_list)
    # awf.ScreenGen(comparison, r'comparsion\The.Peanut.Butter.Falcon.2019', 'a',ptf.multy([3412,92539],4)) # take screenshots
    comparison.set_output()
