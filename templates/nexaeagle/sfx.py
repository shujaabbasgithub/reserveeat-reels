import numpy as np, soundfile as sf
sr=48000;T=25;n=sr*T;out=np.zeros(n)
def add(sig,t):
    i=int(t*sr);e=min(n,i+len(sig));out[i:e]+=sig[:e-i]
tick=np.sin(2*np.pi*2400*np.arange(int(sr*.02))/sr)*np.exp(-np.arange(int(sr*.02))/sr*300)*0.5
# ticks speed up then slow, like a stopwatch near impact
t=0.0;gap=0.32
while t<7.15:
    add(tick,t); t+=gap; gap=max(0.12,gap*0.97)
# rising drone 0-7.2
tt=np.arange(int(sr*7.2))/sr; drone=0.12*np.sin(2*np.pi*(55+40*tt/7.2)*tt)*(tt/7.2); add(drone,0)
# whoosh/impact at 9.85
w=np.random.RandomState(3).randn(int(sr*.5))*np.linspace(1,0,int(sr*.5))**2*0.35; add(w,9.8)
sf.write('sfx.wav',out/np.abs(out).max()*0.8,sr)
