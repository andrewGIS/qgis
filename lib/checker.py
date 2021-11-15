class Checker:
    def __init__(self, layer="river"):
        self.layer = layer

    def check_geometry(self, geometry) -> bool:
        if geometry.area() > 10000:
            return False
        return True
