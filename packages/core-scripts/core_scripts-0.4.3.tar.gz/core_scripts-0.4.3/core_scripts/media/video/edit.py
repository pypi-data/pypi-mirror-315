from core_commands import commands

def edit(start_point,end_point,original_file,edited_file):
    return commands.ffmpeg(f"-ss {start_point} -to {end_point} -i {original_file} -y -c copy {edited_file}")