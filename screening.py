import pandas as pd
PARAMETERS = ["ph","turbidity","tds","conductivity","hardness"]
# Illustrative configurable screening thresholds; confirm applicable standards before use.
THRESHOLDS = {
    "ph": (6.5, 8.5), "turbidity": (0, 5), "tds": (0, 500),
    "conductivity": (0, 1500), "hardness": (0, 200)
}
def screen_row(row):
    available = [p for p in PARAMETERS if p in row and pd.notna(row[p])]
    if not available:
        return {"status":"Insufficient data","flags":[],"count":0,
                "note":"No supported measurements supplied."}
    flags=[]
    for p in available:
        lo,hi=THRESHOLDS[p]
        if row[p] < lo or row[p] > hi:
            flags.append(p)
    if len(flags)>=2: status="Priority follow-up recommended"
    elif len(flags)==1: status="Further review recommended"
    else: status="No configured threshold exceeded"
    return {"status":status,"flags":flags,"count":len(flags),
            "note":"Screening thresholds are illustrative and are not a safety certification."}
