import vapoursynth as vs

core = vs.core
from awsmfunc import banddtct

video_file = ''

src = core.lsmas.LWLibavSource(video_file)
banddtct(src)
