import os, math
import subprocess

dirname = os.getcwd()   #if mp4 files dir not current dir, change this line
split_time = '00:02:50'
split_minute = 16

def video_duration(filename):
    num = 0
    result = subprocess.Popen(["ffmpeg","-i", filename], stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
    for x in result.stdout.readlines():
        if "Duration" in str(x):
            d =[i for i in str(x).split(',') if "Duration" in i] 
            l = 0
            #print(d)
            for i in str(d).split(':'):
                s = i.translate(str.maketrans('','',' ]"'))
                if s.translate(str.maketrans('','','.')).isdigit():
                    num += float(s) * (60 ** (2 - l))
                    l += 1
    return num

def convert(mp4name, time_start, mp3name):
    mp3name = str(mp3name) + ".mp3"
    '''
    i = "ffmpeg -ss {} -t {} -i {} -vn -acodec libmp3lame {}".format(time_start, time_end, mp4name, mp3name)
    t = subprocess.Popen(i,shell=True)
    a = t.wait()
'''
    command = ["ffmpeg", "-ss", time_start, "-t", split_time,
                    "-y", "-i", mp4name,
                    "-loglevel", "error", mp3name]
    use_shell = True if os.name == "nt" else False
    subprocess.run(command, stdin=open(os.devnull), shell=use_shell)

def mp4_to_mp3(mp4namelist):
    mp3num = 0
    for mp4name in mp4namelist:
        vd = video_duration(mp4name)
        print("Process {}, duration: {}s divided {} MP3 files...".format(mp4name, vd, math.ceil((vd - 10) / 160)), end = "")
        for i in range(math.ceil((vd - 10) / 160)):
            if i * split_minute // 6 < 10:
                start_time = "00:0{}:{}0".format(i * split_minute // 6, i * split_minute % 6)
            elif i * split_minute // 6 >= 10:
                start_time = "00:{}:{}0".format(i * split_minute // 6, i * split_minute % 6)
            convert(mp4name, start_time, mp3num)
            print(" {}.mp3".format(mp3num), end = "")
            mp3num += 1
        print("")
    return mp3num

def filenamelist():
    filelist = os.listdir(dirname)
    namelist = []
    for name in filelist:
        if ".mp4" in name:
            namelist.append(name)
    return sorted(namelist)

def main():
    namelist = filenamelist()
    print("Scaned {} MP4 files: {}".format(len(namelist),namelist))
    mp3num = mp4_to_mp3(namelist)
    print("All {} MP3 files Converted".format(mp3num))

if __name__ == "__main__":
    main()