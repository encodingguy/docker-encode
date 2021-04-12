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

# 2 Resize
filtered = awf.zresize(clip, preset=720)
filtered = awf.CropResize(clip=filtered, preset=720)

# 3 Filtering
filtered = awf.FillBorders(clip=filtered, top=1, left=1,
                           right=1)  # For 1080p only. If you're working on 720, please consider using CropResize!
mask = core.std.Binarize(clip, 5000)
filtered = ptf.DebandReader(filtered, 'merged-banding-frames.txt', mask=mask)
filtered = depth(filtered, 8)
if sample_extract + encode_comparison is False:
    filtered.set_output()

# 4 Sample Extract & Comparison
if sample_extract:
    extract = awf.SelectRangeEvery(clip=filtered, every=3000, length=50,
                                   offset=960)  # Modify it with the length to extract!
    if sample_comparison:
        filtered = awf.FrameInfo(filtered, 'Filtered')
        comparison = awf.InterleaveDir(folder=test_folder, PrintInfo=True, first=extract, repeat=True)
        depth(comparison, 8).set_output()
    else:
        depth(extract, 8).set_output()

# 6 Source VS Encode
if encode_comparison:
    src = awf.FrameInfo(src, 'Source')
    filtered = awf.FrameInfo(filtered, 'Filtered')
    encode = awf.FrameInfo(encode, 'Encode')
    comparison_list = [src, encode]
    if target_clip_path[0]:
        target = awf.FrameInfo(target, target_clip_path[1])
        comparison_list.append(target)
    comparison = core.std.Interleave(comparison_list)
    comparison.set_output()
