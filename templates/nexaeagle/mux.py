# usage: python3 -I mux.py <silent.mp4> <total_seconds> <out.mp4> start0 start1 ...   (start time in seconds of each vo_i.wav)
import sys,subprocess
src,tot,out,*st=sys.argv[1:];st=[float(x) for x in st];n=len(st)
ins=sum([["-i",f"vo_{i}.wav"] for i in range(n)],[])
fl=";".join(f"[{i}]adelay={int(st[i]*1000)}|{int(st[i]*1000)}[a{i}]" for i in range(n))+";"+"".join(f"[a{i}]" for i in range(n))+f"amix=inputs={n}:normalize=0,apad,atrim=0:{tot},loudnorm=I=-16:TP=-1.5[o]"
subprocess.run(["ffmpeg","-y","-v","error",*ins,"-filter_complex",fl,"-map","[o]","-ar","48000","vo.wav"],check=True)
subprocess.run(["ffmpeg","-y","-v","error","-i",src,"-i","vo.wav","-c:v","copy","-c:a","aac","-b:a","192k","-shortest","-movflags","+faststart",out],check=True)
