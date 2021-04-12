import vapoursynth as vs
import whalefunc as whf
import awsmfunc as awf
import kagefunc as kgf
from vsutil import depth
import adptvgrnMod as adp
import havsfunc as haf
import pterfunc as ptf

core = vs.core

# 0 Encode Flag
source_clip_path = r''  # The path of source clip
encode_clip_path = r''  # The path of encode clip
target_clip_path = [r'','Target']  # First is The path of target clip and the second is the target clip's name
test_folder = r''  # The path of the test encodes
sample_extract = False  # True if you want to extract sample clip
sample_comparison = False  # True if you want to comparison sample clip
encode_comparison = False  # True if you want to make a source vs encode

# 1 Import Source And Crop
src = core.lsmas.LWLibavSource(source_clip_path).std.Crop(top=0, bottom=0, left=0,
                                                          right=0)  # Modify it with the pixels to crop!
encode = core.lsmas.LWLibavSource(encode_clip_path) if encode_comparison else False
target = core.lsmas.LWLibavSource(target_clip_path[0]) if encode_comparison else False
clip = depth(src, 16)

# 2 Filtering

# 2.1 Dirty lines & Borders
fix_borders = False
if fix_borders:
    filtered = awf.FillBorders(clip=clip, top=0, left=0,
                               right=0,bottom=0)  # For 1080p only. If you're working on 720, please consider using CropResize!
    filtered = awf.CropResize(clip=clip, preset=720) # Resize the cilp and fill borders
else:
    filtered = clip

# 2.2 Resized
resize = False
if resize:
    resized = awf.zresize(filtered, preset=720)
else:
    resized = filtered

# 2.3 Deband & Deblock
deband = False
if deband:
    mask = core.std.Binarize(resized, 5000)
    filtered = ptf.DebandReader(resized, 'merged-banding-frames.txt', mask=mask)
else:
    filtered = resized
    
# 2.4 Out!
    filtered = depth(filtered, 8)
    if sample_extract is False and encode_comparison is False:
        filtered.set_output()

# 3 Sample Extract & Comparison
if sample_extract:
    extract = awf.SelectRangeEvery(clip=filtered, every=3000, length=50,
                                   offset=960)  # Modify it with the length to extract!
    if sample_comparison:
        extract = awf.FrameInfo(extract, 'Filtered')
        comparison = awf.InterleaveDir(folder=test_folder, PrintInfo=True, first=extract, repeat=True)
        depth(comparison, 8).set_output()
    else:
        depth(extract, 8).set_output()

# 4 Source VS Encode
if encode_comparison:
    src = awf.FrameInfo(src, 'Source') if not resize else awf.FrameInfo(depth(awf.zresize(filtered, preset=720),8), 'Source')
    filtered = awf.FrameInfo(filtered, 'Filtered')
    encode = awf.FrameInfo(encode, 'Encode')
    comparison_list = [src, encode]
    if target_clip_path[0]:
        target = awf.FrameInfo(target, target_clip_path[1])
        comparison_list.append(target)
    comparison = core.std.Interleave(comparison_list)
    comparison.set_output()
