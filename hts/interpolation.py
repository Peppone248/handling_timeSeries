import numpy as np

def sample_and_hold(t_in, y_in, t_out):
    t_in  = np.asarray(t_in,  dtype=float)
    y_in  = np.asarray(y_in,  dtype=float)
    t_out = np.asarray(t_out, dtype=float)

    idx = np.searchsorted(t_in, t_out, side="right")
    idx_clamped = np.clip(idx - 1, 0, len(y_in) - 1)  # avoid negative indexes or IndexOutOfBound
    out_val = y_in[idx_clamped]                         # vectorized indexes

    out_val[t_out < t_in[0]]  = np.nan                 # left threshold
    out_val[t_out >= t_in[-1]] = y_in[-1]              # right threshold

    return out_val


def nearest_neighbour(t_in, y_in, t_out):
    t_in  = np.asarray(t_in,  dtype=float)
    y_in  = np.asarray(y_in,  dtype=float)
    t_out = np.asarray(t_out, dtype=float)

    out_val = np.full(len(t_out), np.nan)
    idx = np.searchsorted(t_in, t_out, side="right")  # idx of the sample to the right

    for i in range(len(t_out)):
        current_time = t_out[i]

        if current_time < t_in[0] or current_time > t_in[-1]:
            pass  # already NaN
        else:
            i_right = idx[i]                # indice campione a destra
            i_left  = idx[i] - 1            # indice campione a sinistra
            mid     = (t_in[i_right] + t_in[i_left])/2  # midpoint tra t_in[i_left] e t_in[i_right]
            
            if current_time < mid:
                out_val[i] = y_in[i_left]   # prendi il campione a sinistra
            else:
                out_val[i] = y_in[i_right]  # prendi il campione a destra

    return out_val
        