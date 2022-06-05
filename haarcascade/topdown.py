import numpy as np
import cameratransform as ct
import cv2

def add_arguments(ap):
    ap.add_argument('--focallength-mm', help='Focal length in mm', default=None, metavar='MM',type=float)
    ap.add_argument('--sensor-width-mm', help='Sensor width in mm', default=None, metavar='MM',type=float)
    ap.add_argument('--sensor-height-mm', help='Sensor height in mm', default=None, metavar='MM',type=float)
    ap.add_argument('--pos-x-m', help='Camera position in m', default=0, metavar='M',type=float)
    ap.add_argument('--pos-y-m', help='Camera position in m', default=0, metavar='M',type=float)
    ap.add_argument('--elevation-m', help='Elevation of camera in m', default=None, metavar='M',type=float)
    ap.add_argument('--tilt-deg', help='Camera tilt (straight down is 0 degrees)', default=None, metavar='DEG',type=float)
    ap.add_argument('--roll-deg', help='Camera roll (horizontal is 0 degrees)', default=0.0, metavar='DEG',type=float)
    ap.add_argument('--heading-deg', help='Camera heading ("north" is 0 degrees)', default=0.0, metavar='DEG',type=float)
    ap.add_argument('--topdownview-size-m', help='X,Y in metres describing top-down view of area covered by camera.', default=None, metavar='X,Y')
    ap.add_argument('--3d', help='Toggle 3-D perspective unprojection transformation', default=False, action='store_true',dest='three_d')

class Topdown():
    def __init__(self, args, imagewxh, extent=np.array([-10,10,0,20]), scalefactors=np.array([1,1])):
        self.cam = None
        if isinstance(imagewxh, (list, tuple, np.ndarray)):
            self.imagewxh = np.array(imagewxh)[:2]
        else:
            return
        if isinstance(scalefactors, (list, tuple, np.ndarray)):
            self.topdown_scalefactors = np.array(scalefactors)[:2]
        elif isinstance(scalefactors, (int, np.int, float, np.float)):
            self.topdown_scalefactors = np.array([scalefactors, scalefactors])
        else:
            return
        if isinstance(extent, (list, tuple, np.ndarray)):
            self.topdown_extent = np.array(extent)[:4]
        else:
            return
        self.topdown_scalefactors *= np.array([-1,1]) # mirror topdown coords in output
        self.topdown_translation = np.array([-extent[0], -extent[2]]) # put (0,0) in corner

        if args.three_d and args.focallength_mm is not None and\
           args.sensor_width_mm is not None and args.sensor_height_mm is not None and\
           args.elevation_m is not None and args.tilt_deg is not None:
            self.cam = ct.Camera(ct.RectilinearProjection(focallength_mm=args.focallength_mm,
                                                          sensor_width_mm=args.sensor_width_mm,
                                                          sensor_height_mm=args.sensor_height_mm,
                                                          image_width_px=imagewxh[0],
                                                          image_height_px=imagewxh[1]),
                                 ct.SpatialOrientation(elevation_m=args.elevation_m,
                                                       pos_x_m=args.pos_x_m,
                                                       pos_y_m=-args.pos_x_m,
                                                       tilt_deg=args.tilt_deg,
                                                       heading_deg=args.heading_deg,
                                                       roll_deg=args.roll_deg))
    def ready(self):
        return self.cam is not None

    def topdownFromImage(self, imagecoords, filter_nans=True, **kwargs):
        if not self.ready(): return None
        imagecoords = np.array(imagecoords)
        tdcoords = self.cam.spaceFromImage(imagecoords, **kwargs)[...,:2] * self.topdown_scalefactors + self.topdown_translation
        if filter_nans: tdcoords = tdcoords[~np.isnan(tdcoords).any(axis=1)]
        return tdcoords

    def imageFromTopdown(self, topdowncoords, filter_nans=True, **kwargs):
        if not self.ready(): return None
        topdowncoords = np.array(topdowncoords)
        tdcoords3 = addZeroColumn((topdowncoords - self.topdown_translation)/self.topdown_scalefactors)
        icoords = self.cam.imageFromSpace(tdcoords3, **kwargs)
        if filter_nans: icoords = icoords[~np.isnan(icoords).any(axis=1)]
        return icoords

    def getTopViewofImage(image, **kwargs):
        if not self.ready(): return None
        return self.cam.getTopViewofImage(image, extent=self.topdown_extent, **kwargs)

def addZeroColumn(a):
    return np.hstack((a, np.zeros((a.shape[0], 1), dtype=a.dtype)))
