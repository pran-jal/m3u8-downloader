import ffmpeg

def downloader(download_file_name, dir_name = None):
    output_path = f"{download_file_name}.mp4"
    if dir_name:
        output_path = f"{dir_name}\\{output_path}"
    ffmpeg.input(f"http://localhost:8000/fake.m3u8").output(output_path, vcodec="copy", acodec="copy").overwrite_output().run()
