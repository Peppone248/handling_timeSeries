import numpy as np

def sample_and_hold(t_in, y_in, t_out):
    t_in  = np.asarray(t_in,  dtype=float)
    y_in  = np.asarray(y_in,  dtype=float)
    t_out = np.asarray(t_out, dtype=float)

    idx     = np.searchsorted(t_in, t_out, side="right")
    idx_clamped = np.clip(idx - 1, 0, len(y_in) - 1)  # avoid negative indexes or IndexOutOfBound
    out_val = y_in[idx_clamped]                         # vectorized indexes

    out_val[t_out < t_in[0]]  = np.nan                 # left threshold
    out_val[t_out >= t_in[-1]] = y_in[-1]              # right threshold

    return out_val
        