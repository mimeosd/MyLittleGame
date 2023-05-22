import ffmpeg

input_file = 'bgmusic.mp4'
output_file = 'bgmusic.mp3'

ffmpeg.input(input_file).output(output_file).run()
