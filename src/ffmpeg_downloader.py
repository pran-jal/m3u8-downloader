import ffmpeg

def downloader(download_file_name):
    ffmpeg.input(f"http://localhost:8000/fake.m3u8").output(f"{download_file_name}.mp4", vcodec="copy", acodec="copy").overwrite_output().run()
