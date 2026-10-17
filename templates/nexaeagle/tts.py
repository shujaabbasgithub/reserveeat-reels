import sys,json,soundfile as sf
from kokoro_onnx import Kokoro
k=Kokoro("kokoro-v1.0.onnx","voices-v1.0.bin")
v=sys.argv[2] if len(sys.argv)>2 else "am_michael"; sp=float(sys.argv[3]) if len(sys.argv)>3 else 1.15
print(sorted(k.get_voices())[:60])
d=[]
for i,t in enumerate(json.load(open(sys.argv[1]))):
    a,sr=k.create(t,voice=v,speed=sp,lang="en-us");sf.write(f"vo_{i}.wav",a,sr);d.append(round(len(a)/sr,2))
json.dump(d,open("durations.json","w"));print(d,sum(d))
