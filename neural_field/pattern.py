import numpy as np
import pyopencl as cl

ctx = cl.create_some_context()
queue = cl.CommandQueue(ctx)

nx =1000
tmax=200

x=np.linspace(-np.pi,np.pi,nx,endpoint=False,dtype=np.float32)
u=np.ones(nx,dtype=np.float32)
v=np.ones(nx,dtype=np.float32)
I=np.zeros(nx,dtype=np.float32)
time=np.arange(tmax)

mf = cl.mem_flags

x_g = cl.Buffer(ctx, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=x)
u_g = cl.Buffer(ctx, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=u)
v_g = cl.Buffer(ctx, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=v)
I_g = cl.Buffer(ctx, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=I)

res_u_g = cl.Buffer(ctx, mf.READ_WRITE, u.nbytes)
res_v_g = cl.Buffer(ctx, mf.READ_WRITE, v.nbytes)

src_file = open('kernel.cl','r') 
src=src_file.read()
src_file.close()
prg = cl.Program(ctx,src).build()


u_mat=np.zeros((tmax,nx))
v_mat=np.zeros((tmax,nx))

for t in xrange(tmax):
  prg.pattern(queue, (nx,), None, x_g, u_g, v_g, I_g, res_u_g, res_v_g,np.int32(nx))

  cl.enqueue_copy(queue, u_g, res_u_g)
  cl.enqueue_copy(queue, v_g, res_v_g)

  cl.enqueue_copy(queue, u, res_u_g)
  cl.enqueue_copy(queue, v, res_v_g)


  u_mat[t,:]=u
  v_mat[t,:]=v
  
  
import pylab as pl
pl.figure()
pl.pcolormesh(x,time,u_mat)
pl.colorbar()
print u_mat.max()


res_x_g = cl.Buffer(ctx, mf.READ_WRITE, x.nbytes)

res_x=np.zeros_like(x)
prg.mytest(queue, (nx,), None, x_g, res_x_g)
cl.enqueue_copy(queue, res_x, res_x_g)


#pl.figure()
#pl.plot(x,res_x)
#
#mexfft=abs(np.fft.fft(res_x))
#freqs=np.fft.fftfreq(nx,2*np.pi/nx)
#
#pl.figure()
#pl.plot(freqs,mexfft)
#pl.xlim((-5,5))