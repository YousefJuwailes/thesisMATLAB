import numpy as np

def cw():
    # First attempt with rectangular plate and sphere
    c = np.random.uniform(0, 1)

    # Second attempt with hemispherical convex and concave sides
    # c = random.uniform(0.34, 1.33)

    if c < 0.5:
        return 0.47
    else:
        return 2.05