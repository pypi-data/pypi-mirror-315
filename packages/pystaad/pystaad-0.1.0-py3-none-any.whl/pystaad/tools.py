from numpy import deg2rad
def deg2node(degree,height,distance_from_start_to_mid):
    return float(round(height+deg2rad(degree)*distance_from_start_to_mid,2))
def maketrussooroof(**kwargs):
    pass
