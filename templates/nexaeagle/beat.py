import numpy as np, soundfile as sf, sys
sr=48000; T=float(sys.argv[1]); bpm=118; n=int(sr*T); out=np.zeros(n)
b=60/bpm; t=np.arange(int(sr*0.4))/sr
kick=np.sin(2*np.pi*(50+90*np.exp(-t*30))*t)*np.exp(-t*9)
hat=np.random.RandomState(1).randn(int(sr*0.05))*np.exp(-np.arange(int(sr*0.05))/sr*90)*0.35
bass_t=np.arange(int(sr*b/2))/sr
notes=[55,55,65.4,49]
def add(sig,pos):
    i=int(pos*sr); e=min(n,i+len(sig)); 
    if i<n: out[i:e]+=sig[:e-i]
k=0;p=0.0
while p<T:
    add(kick,p); add(hat,p+b/2)
    f=notes[(k//4)%4]; add(0.25*np.sin(2*np.pi*f*bass_t)*np.exp(-bass_t*4),p+b/2)
    if k%4==2: add(np.random.RandomState(k).randn(int(sr*.12))*np.exp(-np.arange(int(sr*.12))/sr*30)*.3,p)
    p+=b;k+=1
fade=np.ones(n); fl=int(sr*1.5); fade[-fl:]=np.linspace(1,0,fl)
out=out*fade; out/=np.abs(out).max(); sf.write('beat.wav',out*0.9,sr)
