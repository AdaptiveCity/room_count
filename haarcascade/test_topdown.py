import topdown
import numpy as np

class FakeArgs:
    def __init__(self):
        self.three_d = True
        self.focallength_mm = 7.0
        self.sensor_width_mm = 6.7
        self.sensor_height_mm = 5.6
        self.elevation_m = 1.8
        self.tilt_deg = 81
        self.heading_deg = -21
        self.roll_deg = -5
        self.pos_x_m = 5
        self.pos_y_m = -2


if __name__ == "__main__":
    args = FakeArgs()
    td = topdown.Topdown(args, (4032, 2268), scalefactors=4)
    print('Topdown is ready.')
    assert(td.ready())
    icoords = np.array([(2739.0, 1214), (2455.5, 1568), (2325.0, 1333), (2734.0, 1114), (3029.0, 1233), (3573.0, 1049), (2056.0, 1577)])
    scoords = td.topdownFromImage(icoords)
    print('topdownFromImage({}) => {}'.format(icoords,scoords))
    scoords_trans = scoords + np.array([310,0])
    scoords_int = scoords_trans.astype(np.int32)
    print('scoords+[310,0].to_int => {}'.format(scoords_int))
    #scoords_expected=np.array([[307, 17.07473937] ,[306, 5.36322805] ,[309, 12.31253464] ,[308, 22.46429601] ,[304, 15.97947542] ,[300, 25.01766182] ,[309, 5.04083794]])
    scoords_int_expected=np.array([[307,  17], [306,   5], [309,  12], [308,  22], [304,  15], [300,  25], [309,   5]])
    assert(np.array_equal(scoords_int, scoords_int_expected))
    icoords2 = td.imageFromTopdown(scoords)
    print('imageFromTopdown({}) => {}'.format(scoords, icoords2))
    assert(np.allclose(icoords, icoords2))
