# BinomialTree

Binomial trees with n and n+1 steps to price American options have errors of opposite signs, so averaging
the values from trees with n and n+1 steps improves accuracy. Running `python xbinomial_tree.py` gives 
the results below. You can see that averaging the option prices using 100 and 101 steps gives prices close
to those from trees with 1000 or 1001 steps, even though a tree with 100 steps is about 10^2 times faster to compute
than one with 1000 steps.

```
        s0         k         r         q     sigma         t
  100.0000  100.0000    0.0500    0.0000    0.2000    1.0000

                 call    put
# steps                     
100           10.4306 6.0824
101           10.4680 6.1046
1000          10.4486 6.0896
1001          10.4523 6.0918
avg 100:101   10.4493 6.0935
avg 1000:1001 10.4505 6.0907
BS            10.4506 5.5735
```
