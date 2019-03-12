#!/usr/bin/python3
import subprocess, shlex, json
import sched, time

s = sched.scheduler(time.time, time.sleep)

def findts():
    cmd = "ffprobe -show_packets -select_streams v -print_format json rtmp://192.168.137.152:1935/live/plane"
    args = shlex.split(cmd)
    #args.append(videoUrl)

    ffprobeOutput = subprocess.check_output(args).decode('utf-8')
    ffprobeOutput = json.load(ffprobeOutput)

    import pprint
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(ffprobeOutput)

    #s.enter(2, 1, findts())

if __name__ == '__main__':

    #s.enter(2, 1, findts())
    findts()