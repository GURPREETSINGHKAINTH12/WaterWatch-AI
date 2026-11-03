import sys, os
sys.path.insert(0,os.path.dirname(os.path.dirname(__file__)))
from src.screening import screen_row
def test_normal_sample():
    r=screen_row({"ph":7.0,"turbidity":1.0,"tds":250,"conductivity":500,"hardness":100})
    assert r["count"]==0
def test_flagged_sample():
    r=screen_row({"ph":9.2,"turbidity":8.0,"tds":250,"conductivity":500,"hardness":100})
    assert r["count"]==2
def test_empty_sample():
    assert screen_row({})["status"]=="Insufficient data"
