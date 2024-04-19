import ffmpeg

stream1 = ffmpeg.input("COSTA RICA IN 4K 60fps HDR (ULTRA HD).webm", ss=0)
stream2 = ffmpeg.input("COSTA RICA IN 4K 60fps HDR (ULTRA HD).mp4", ss=0)

stream = ffmpeg.output(stream1, stream2, "output.mp4", vcodec="copy", acodec="copy")
ffmpeg.run(stream)
