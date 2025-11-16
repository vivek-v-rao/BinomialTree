from option_pricing import bs, crr_binomial_option_bs_smooth
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
n_steps_vec = [20, 21, 40, 41, 1000, 1001]
nsv = len(n_steps_vec)
prices_mat = np.zeros([nsv+4, 2])

print("".join("%10s"%x for x in ["s0", "k", "r", "q", "sigma", "t"]))
print("".join("%10.4f"%x for x in [s0, k, r, q, sigma, t]))

for i, n_steps in enumerate(n_steps_vec):
    call_a = crr_binomial_option_bs_smooth(s0, k, r, q, sigma, t, n_steps, "call",
        "american")
    put_a = crr_binomial_option_bs_smooth(s0, k, r, q, sigma, t, n_steps, "put",
        "american")
    prices_mat[i, :] = [call_a, put_a]
    
prices_mat[nsv, :] = (prices_mat[0, :] + prices_mat[1, :])/2
prices_mat[nsv+1, :] = (prices_mat[2, :] + prices_mat[3, :])/2
prices_mat[-2, :] = 2*prices_mat[nsv+1, :] - prices_mat[nsv, :]
prices_mat[-1, :] = [call_e, put_e]
indx = [str(x) for x in n_steps_vec]
indx = indx +  ["avg " + indx[0] + ":" + indx[1], "avg " + indx[2] + ":" + indx[3], "Richardson", "BS"]
df = pd.DataFrame(prices_mat, columns=["call", "put"], index=indx)
df.index.name = "# steps"
print("\n" + df.to_string())
