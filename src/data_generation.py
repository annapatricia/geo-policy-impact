import numpy as np
import pandas as pd

def generate_policy_data(
    n: int = 1200,
    center: tuple = (-22.9068, -43.1729),
    spread_before: float = 0.018,
    spread_after: float = 0.030,
    seed: int = 42
):
    """
    Synthetic geolocated events BEFORE vs AFTER a public policy intervention.
    Before: more concentrated around 'center'
    After: more dispersed (simulating reduction of hotspots and redistribution)
    """
    rng = np.random.default_rng(seed)

    lat_before = rng.normal(center[0], spread_before, n)
    lon_before = rng.normal(center[1], spread_before, n)

    lat_after = rng.normal(center[0], spread_after, n)
    lon_after = rng.normal(center[1], spread_after, n)

    before = pd.DataFrame({"lat": lat_before, "lon": lon_before, "period": "Before"})
    after  = pd.DataFrame({"lat": lat_after,  "lon": lon_after,  "period": "After"})

    return before, after
