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
[Joshi (2008)](https://fbe.unimelb.edu.au/__data/assets/pdf_file/0010/2591884/170.pdf) suggests
"replac[ing] the price at the second last layer of nodes with the
price given by the Black–Scholes formula. The idea being that since one is
allowing no exercise opportunities between steps and we are approximating
the Black–Scholes model, this ought to give a more accurate price. In
addition, the Black–Scholes formula should give a price that smoothly
varies and so this should make the price smoother as a function of steps."
He also finds that Richardson extrapolation of binomial tree prices using different
numbers of steps improves accuracy. I use the extrapolation `2*x(2n) - x(n)` where
`x` is the price using `n` steps.

Running `python xbinomial_tree_smooth.py`, which applies Black-Scholes smoothing and Richardson extrapolation, gives

```
        s0         k         r         q     sigma         t
  100.0000  100.0000    0.0500    0.0000    0.2000    1.0000

              call    put
# steps                  
20         10.4754 6.1081
21         10.4729 6.1047
40         10.4632 6.1004
41         10.4623 6.1009
1000       10.4511 6.0910
1001       10.4511 6.0910
avg 20:21  10.4742 6.1064
avg 40:41  10.4627 6.1006
Richardson 10.4513 6.0949
BS         10.4506 5.5735
```

One sees that Richardson extrapolation using 20 and 40 steps and 21 and 41 steps gives accurate results.
