import vapoursynth as vs
import whalefunc as whf
import awsmfunc as awf
import kagefunc as kgf
from vsutil import depth
# import adptvgrnMod as adp
import havsfunc as haf
import pterfunc as ptf

core = vs.core
# 1 Import Source And Crop
src = core.lsmas.LWLibavSource('').std.Crop(top=0,bottom=0,left=0,right=0)
encode = core.ffms2.Source('')
clip = depth(src, 16)

# 2 Resize
filtered = awf.zresize(clip, preset=720)
filtered = awf.CropResize(clip=filtered, preset=720)

# 3 Filtering

filtered = awf.FillBorders(clip=filtered, top=1, left=1,right=1)  # For 1080p only. If you're working on 720, Plaese consider using CropResize!
mask = core.std.Binarize(clip, 5000)
filtered = ptf.DebandReader(filtered, 'merged-banding-frames.txt', mask=mask)
filtered = depth(filtered, 8)

# 4 Sample Comparison
filtered = awf.FrameInfo(filtered,'Filtered')
extract = awf.SelectRangeEvery(clip=filtered, every=3000, length=50, offset=960)
folder = r'folder'
comparison = awf.InterleaveDir(folder=folder, PrintInfo=True, first=extract, repeat=True)

# 6 Source VS Encode
src = awf.FrameInfo(depth(clip, 8), 'Source')
filtered = awf.FrameInfo(filtered, 'Filtered')
encode = awf.FrameInfo(encode, 'Encode')
comparison = core.std.Interleave([src, filtered, encode])
