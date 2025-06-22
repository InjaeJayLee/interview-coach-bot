import shutil
import subprocess

def check_ffmpeg_installed():
    ffmpeg_path = shutil.which("ffmpeg")
    if ffmpeg_path:
        print(f"Good to go!\nffmpeg is installed at:\n\t{ffmpeg_path}")
        try:
            result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True).stdout.split('\n')[0]
            print(f"ffmpeg version info:\n\t{result}\n")
        except Exception as e:
            print(f"ffmpeg found but couldn't run:\n\t{e}\n")
    else:
        print("ffmpeg is NOT installed.")
        
check_ffmpeg_installed()
