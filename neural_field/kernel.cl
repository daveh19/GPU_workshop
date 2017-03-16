

float sq(float x){
 return x*x;
}

float w(float d)
{
  const float A=5.;
  const float a=.125;

  const float B=4.;
  const float b=.005;

  //const float p=1.;

  //return A*pow(a,p/(float)2.)*exp(-a*pow(d,(float)2.))-B*pow(b,p/(float)2.)*exp(-b*pow(d,(float)2.));

  return A*pow(a,(float)0.5)*exp(-a*pow(d,(float)2.))-B*pow(b,(float)0.5)*exp(-b*pow(d,(float)2.));
}


float dist(float x, float y)
{
 return x-y;
}
float F(float u)
{
  const float u_th=0.05;
  const float r=0.25;
  const float k=.26;


  float df0=r/4.;
  float f= 1./(1.+exp(-r*(u-u_th)));
  float f0 = 1./(1.+exp(r*u_th));

  return k*(f-f0)/df0; 

}

__kernel void mytest(
    __global const float *x_g,
    __global float *res_x_g
)
{
  int gid = get_global_id(0);
  res_x_g[gid]=w(x_g[gid]);
}

__kernel void pattern(
    __global const float *x_g,
    __global const float *u_g,
    __global const float *v_g,
    __global const float *I_g,    
    __global float *res_u_g,
    __global float *res_v_g,
   int nx
)
{

  const float alpha=0.1;
  const float beta=0.125;
  const float tau=1.;
  const float dt=0.1;

  int gid = get_global_id(0);
  float u =u_g[gid];
  float v =v_g[gid];
  float I =I_g[gid];


  
  float conv=0.;
  for(int i=0;i<nx; i++)
  {
    conv+=F(u_g[i])*w(dist(x_g[gid],x_g[i]));
  }   
  res_u_g[gid]=u+dt*(-u-beta*v+I+(M_PI_F*2/nx)*conv);
  res_v_g[gid]=v+dt*alpha*(u-v);

}