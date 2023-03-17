import math

options = {
    'bootstrap': 512,
    'conf': 0.05,
    'cliff': 0.4,
    'cohen': 0.35,
    'width': 40,
}

def erf(x):
    a1 =  0.254829592
    a2 = -0.284496736
    a3 =  1.421413741
    a4 = -1.453152027
    a5 =  1.061405429
    p  =  0.3275911
    sign = 1
    if x < 0:
        sign = -1
    x = math.abs(x)
    t = 1.0/(1.0 + p*x)
    y = 1.0 - (((((a5*t + a4)*t) + a3)*t + a2)*t + a1)*t*math.exp(-x*x)
    return sign*y

def gaussian(mu = None,sd = None):
  mu = 0 if mu == None else mu
  sd = 1 if sd == None else sd
  sq,pi,log,cos,r = math.sqrt,math.pi,math.log,math.cos,math.random
  return  mu + sd * sq(-2*log(r())) * cos(2*pi*r())

def samples(t,n = None):
  length = n if n != None else len(t)
  u = [0 for i in range(0, length)]
  for i in range(0, n if n != None else len(t)):
      u[i] = t[math.random(len(t))]
  return u

def cliffsDelta(ns1,ns2):
  n,gt,lt = 0,0,0
  if len(ns1) > 128:
      ns1 = samples(ns1,128)
  if len(ns2) > 128:
      ns2 = samples(ns2,128)
  for x in ns1:
      for y in ns2:
          n = n + 1
          if x > y:
              gt = gt + 1
          if x < y:
              lt = lt + 1
  return math.abs(lt - gt)/n <= options['cliff']

def add(i,x):
  i.n  = i.n+1
  d    = x-i.mu
  i.mu = i.mu + d/i.n
  i.m2 = i.m2 + d*(x-i.mu)
  i.sd = i.n<2 and 0 or (i.m2/(i.n - 1))^.5
  return i

def NUM(t=None):
  i = {'n': 0, 'mu': 0, 'm2': 0, 'sd': 0}
  for x in t if t != None else []:
      i = add(i, x)
  return i

def delta(i, other):
  e, y, z= 1E-32, i, other
  return math.abs(y.mu - z.mu) / ((e + y.sd^2/y.n + z.sd^2/z.n)^.5)

def bootstrap(y0,z0):
  n, x,y,z,xmu,ymu,zmu,yhat,zhat,tobs = None
  x, y, z, yhat, zhat = NUM(), NUM(), NUM(), [], []
  for y1 in y0:
      x = add(x, y1)
      y = add(y, y1)
  for z1 in z0:
      x = add(x, z1)
      z = add(z, z1)
  xmu, ymu, zmu = x.mu, y.mu, z.mu
  for y1 in y0:
      yhat.append(y1 - ymu + xmu)
  for z1 in z0:
      zhat.append(z1 - zmu + xmu)
  tobs = delta(y,z)
  n = 0
  for _ in range(0, options['bootstrap']):
      if delta(NUM(samples(yhat)), NUM(samples(zhat))) > tobs:
          n = n + 1
  return n / options['bootstrap'] >= options['conf']

def RX(t,s=None):
  sort(t)
  return {'name': "" if s == None else s, 'rank': 0, 'n': len(t), 'show': "", 'has': t}

def mid(t):
  try:
      t = t['has']
  except:
      t = t
  n = len(t)//2
  return len(t)%2==0 and (t[n] +t[n+1])/2 or t[n+1]

def div(t):
  try:
      t = t['has']
  except:
      t = t
  return (t[len(t)*9//10 ] - t[len(t)*1//10 ])/2.56

def merge(rx1,rx2):
  rx3 = RX({}, rx1['name'])
  print("NOTE: THIS MIGHT NOT BE RIGHT - location -> merge function defn")
  for t in rx2['has']:
      for x in t:
          rx3['has'].append(x)
  sort(rx3['has'])
  rx3['n'] = len(rx3['has'])
  return rx3

def scottKnot(rxs):
    def merges(i,j):
        out = RX({},rxs[i]['name'])
        for k in range(i, j):
            out = merge(out, rxs[j])
        return out 
    def same(lo,cut,hi):
        l= merges(lo,cut)
        r= merges(cut+1,hi)
        return cliffsDelta(l['has'], r['has']) and bootstrap(l['has'], r['has']) 
    def recurse(lo,hi,rank):
        cut,best,l,l1,r,r1,now,b4 = None
        b4 = merges(lo,hi)
        best = 0
        for j in range(lo, hi):
            if j < hi:
                l   = merges(lo,  j)
                r   = merges(j+1, hi)
                now = (l.n*(mid(l) - mid(b4))^2 + r.n*(mid(r) - mid(b4))^2) / (l.n + r.n)
                if now > best:
                    if math.abs(mid(l) - mid(r)) >= cohen:
                        cut, best = j, now
            if cut and not same(lo,cut,hi):
                rank = recurse(lo,    cut, rank) + 1
                rank = recurse(cut+1, hi,  rank) 
            else:
                for i in range(lo, hi):
                    rxs[i]['rank'] = rank
        return rank 
    def cmp(x, y):
        return mid(x) < mid(y)
    rxs.sort(key=cmp)
    cohen = div(merges(1, len(rxs))) * options['cohen']
    recurse(1, len(rxs), 1)
    return rxs

def tiles(rxs):
  huge,min,max,floor = math.inf,math.min,math.max,math.floor
  lo,hi = huge, -huge
  for rx in rxs:
    lo,hi = min(lo,rx['has'][0]), max(hi, rx['has'][len(rx['has'])])
  for rx in rxs:
    t,u = rx['has'], []
    def of(x,most):
        return max(1, min(most, x))
    def at(x):
        return t[of(len(t)*x//1, len(t))]
    def pos(x):
        return floor(of(options['width']*(x-lo)/(hi-lo+1E-32)//1, options['width']))
    for i in range(0, the['width']):
        u.append(" ")
    a,b,c,d,e= at(.1), at(.3), at(.5), at(.7), at(.9) 
    A,B,C,D,E= pos(a), pos(b), pos(c), pos(d), pos(e)
    for i in range(A, B):
        u[i]="-"
    for i in range(D, E):
        u[i]="-"
    u[options['width']//2] = "|" 
    u[C] = "*"
    rx.show = ' '.join(u) + " {" + "{0:6.2f}".format(a)
    for x in [b,c,d,e]:
        rx['show'] = rx['show'] + ", " + "{0:6.2f}".format(x)
    rx['show'] = rx['show'] + "}"
  return rxs


def test_sample():
    for i in range(1, 10):
        print("", samples(["a","b","c","d","e"]))
    return True

def test_num():
  n=NUM([1,2,3,4,5,6,7,8,9,10])
  print("",n['n'], n['mu'], n['sd'])

def test_gauss():
  t,n =[], None
  for i in range(1, 1000):
      t.append(gaussian(10,2))
  n=NUM(t)
  print("",n['n'], n['mu'], n['sd'])

def test_bootmu():
    print("Convert bootmu")
    '''
  a,b={},{}
  for i=1,100 do a[1+#a]= gaussian(10,1) end
  print("","mu","sd","cliffs","boot","both")
  print("","--","--","------","----","----")
  for mu=10,11,.1 do
    b={}
    for i=1,100 do b[1+#b]= gaussian(mu,1) end
    cl=cliffsDelta(a,b)
    bs=bootstrap(a,b)
    print("",mu,1,cl,bs,cl and bs) end end
    '''

def test_basic():
    print("Convert basic")
    '''
  print("\t\ttruee", bootstrap( {8, 7, 6, 2, 5, 8, 7, 3}, 
                                {8, 7, 6, 2, 5, 8, 7, 3}),
              cliffsDelta( {8, 7, 6, 2, 5, 8, 7, 3}, 
                           {8, 7, 6, 2, 5, 8, 7, 3}))
  print("\t\tfalse", bootstrap(  {8, 7, 6, 2, 5, 8, 7, 3},  
                                 {9, 9, 7, 8, 10, 9, 6}),
             cliffsDelta( {8, 7, 6, 2, 5, 8, 7, 3},  
                          {9, 9, 7, 8, 10, 9, 6})) 
    print("\t\tfalse", 
                    bootstrap({0.34, 0.49, 0.51, 0.6,   .34,  .49,  .51, .6}, 
                               {0.6,  0.7,  0.8,  0.9,   .6,   .7,   .8,  .9}),
                  cliffsDelta({0.34, 0.49, 0.51, 0.6,   .34,  .49,  .51, .6}, 
                              {0.6,  0.7,  0.8,  0.9,   .6,   .7,   .8,  .9})
   ) end
   '''

def test_pre():
    print("Convert pre")
    '''
  print("\neg3")
  local d=1
  for i=1,10 do
    local t1,t2={},{}
    for j=1,32 do t1[1+#t1]=gaussian(10,1); t2[1+#t2]=gaussian(d*10,1) end
    print("\t",d,d<1.1 and "true" or "false",bootstrap(t1,t2),bootstrap(t1,t1))
    d=d+0.05 end end
    '''

def test_five():
    print("Convert five")
    '''
  for _,rx in pairs(tiles(scottKnot{
         RX({0.34,0.49,0.51,0.6,.34,.49,.51,.6},"rx1"),
         RX({0.6,0.7,0.8,0.9,.6,.7,.8,.9},"rx2"),
         RX({0.15,0.25,0.4,0.35,0.15,0.25,0.4,0.35},"rx3"),
         RX({0.6,0.7,0.8,0.9,0.6,0.7,0.8,0.9},"rx4"),
         RX({0.1,0.2,0.3,0.4,0.1,0.2,0.3,0.4},"rx5")})) do
    print(rx.name,rx.rank,rx.show) end end
    '''

def test_six():
    print("Convert six")
    '''
  for _,rx in pairs(tiles(scottKnot{
         RX({101,100,99,101,99.5,101,100,99,101,99.5},"rx1"),
         RX({101,100,99,101,100,101,100,99,101,100},"rx2"),
         RX({101,100,99.5,101,99,101,100,99.5,101,99},"rx3"),
         RX({101,100,99,101,100,101,100,99,101,100},"rx4")})) do
    print(rx.name,rx.rank,rx.show) end end
    '''

def test_tiles():
    print("Convert tiles")
    '''
  rxs,a,b,c,d,e,f,g,h,j,k={},{},{},{},{},{},{},{},{},{},{}
  for i=1,1000 do a[1+#a] = gaussian(10,1) end
  for i=1,1000 do b[1+#b] = gaussian(10.1,1) end
  for i=1,1000 do c[1+#c] = gaussian(20,1) end
  for i=1,1000 do d[1+#d] = gaussian(30,1) end
  for i=1,1000 do e[1+#e] = gaussian(30.1,1) end
  for i=1,1000 do f[1+#f] = gaussian(10,1) end
  for i=1,1000 do g[1+#g] = gaussian(10,1) end
  for i=1,1000 do h[1+#h] = gaussian(40,1) end
  for i=1,1000 do j[1+#j] = gaussian(40,3) end
  for i=1,1000 do k[1+#k] = gaussian(10,1) end
  for k,v in pairs{a,b,c,d,e,f,g,h,j,k} do rxs[k] =  RX(v,"rx"..k) end
  table.sort(rxs,function(a,b) return mid(a) < mid(b) end)
  for _,rx in pairs(tiles(rxs)) do
    print("",rx.name,rx.show) end end
    '''

def test_sk():
    print("Convert sk")
    '''
  rxs,a,b,c,d,e,f,g,h,j,k={},{},{},{},{},{},{},{},{},{},{}
  for i=1,1000 do a[1+#a] = gaussian(10,1) end
  for i=1,1000 do b[1+#b] = gaussian(10.1,1) end
  for i=1,1000 do c[1+#c] = gaussian(20,1) end
  for i=1,1000 do d[1+#d] = gaussian(30,1) end
  for i=1,1000 do e[1+#e] = gaussian(30.1,1) end
  for i=1,1000 do f[1+#f] = gaussian(10,1) end
  for i=1,1000 do g[1+#g] = gaussian(10,1) end
  for i=1,1000 do h[1+#h] = gaussian(40,1) end
  for i=1,1000 do j[1+#j] = gaussian(40,3) end
  for i=1,1000 do k[1+#k] = gaussian(10,1) end
  for k,v in pairs{a,b,c,d,e,f,g,h,j,k} do rxs[k] =  RX(v,"rx"..k) end
  for _,rx in pairs(tiles(scottKnot(rxs))) do
    print("",rx.rank,rx.name,rx.show) end end
    '''

def __main__():
    print("Running all tests")
    test_basic()
    test_gauss()
    test_bootmu()
    test_five()
    test_num()
    test_pre()
    test_sample()
    test_six()
    test_tiles()

__main__()
