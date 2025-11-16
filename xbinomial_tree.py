from option_pricing_crr import bs, crr_binomial_option
import numpy as np
import pandas as pd

pd.options.display.float_format = '{:.4f}'.format
s0 = 100.0
k = 100.0
r = 0.05
q = 0.0
sigma = 0.20
t = 1.0
call_e = bs(s0, k, r, q, sigma, t, "call")
put_e = bs(s0, k, r, q, sigma, t, "put")
n_steps_vec = [100, 101, 1000, 1001]
nsv = len(n_steps_vec)
prices_mat = np.zeros([nsv+3, 2])

print("".join("%10s"%x for x in ["s0", "k", "r", "q", "sigma", "t"]))
print("".join("%10.4f"%x for x in [s0, k, r, q, sigma, t]))

for i, n_steps in enumerate(n_steps_vec):
    call_a = crr_binomial_option(s0, k, r, q, sigma, t, n_steps, "call",
        "american")
    put_a = crr_binomial_option(s0, k, r, q, sigma, t, n_steps, "put",
        "american")
    prices_mat[i, :] = [call_a, put_a]
    
prices_mat[nsv, :] = (prices_mat[0, :] + prices_mat[1, :])/2
prices_mat[nsv+1, :] = (prices_mat[2, :] + prices_mat[3, :])/2
prices_mat[-1, :] = [call_e, put_e]
indx = [str(x) for x in n_steps_vec]
indx = indx +  ["avg " + indx[0] + ":" + indx[1], "avg " + indx[2] + ":" + indx[3], "BS"]
df = pd.DataFrame(prices_mat, columns=["call", "put"], index=indx)
df.index.name = "# steps"
print("\n" + df.to_string())
