from bisect import bisect_left
import time
t = list(range(0, 1000000))
a=time.time();x = [t[bisect_left(t,b)]==b for b in range(100234,101234)];print(time.time()-a)