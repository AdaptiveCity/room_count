import sys
import argparse
import re
import cv2
import json
import cameratransform as ct
import numpy as np

verbose = False
def V(s):
  global verbose
  if verbose:
    print(s)

def quoted_split(s):
    def strip_quotes(s):
        if s and (s[0] == '"' or s[0] == "'") and s[0] == s[-1]:
            return s[1:-1]
        return s
    return [strip_quotes(p).replace('\\"', '"').replace("\\'", "'") \
            for p in re.findall(r'(?:[^"\s]*"(?:\\.|[^"])*"[^"\s]*)+|(?:[^\'\s]*\'(?:\\.|[^\'])*\'[^\'\s]*)+|[^\s]+', s)]

def main():
  global verbose

  optfileparser = argparse.ArgumentParser(add_help=False)
  optfileparser.add_argument('--options-file', help="Read some command-line options from file also.",
                             metavar='FILE', action='append', default=None)
  argv = sys.argv[1:]
  optfiles = []
  while True:
      (optfileargs, argv2) = optfileparser.parse_known_args(args=argv)
      if optfileargs.options_file:
          argv1 = []
          for n in optfileargs.options_file:
              if n not in optfiles: # prevent infinite loops of includes
                  optfiles.append(n)
                  with open(n) as f:
                      lines = [quoted_split(l) for l in f.readlines() if l.strip()[0] != '#']
                  for l in lines:
                      argv1.extend(l)
          argv1.extend(argv2)
          argv = argv1
      else:
          argv = argv2
          break

  parser = argparse.ArgumentParser()
  parser.add_argument('input', type=str, help='image input file')
  parser.add_argument('--verbose', help='Verbose output', default=False, action='store_true')
  parser.add_argument('--backend', type=str, help='detection library: yunet or mtcnn', default='yunet')
  parser.add_argument('--detections-json-in', type=str, help='Read detections from given JSON file instead of computing them', default=None)
  parser.add_argument('--detections-json-out', type=str, help='Output JSON file with detections data', default=None)
  parser.add_argument('--detections-out', type=str, help='Output image showing detections', default=None)
  parser.add_argument('--detections-box-thickness', type=int, help='Line thickness for boxes outlining detections', default=2)
  parser.add_argument('--topdown-out', type=str, help='Output image showing topdown view', default=None)
  parser.add_argument('--topdown-image-size', type=int, nargs=2, help='Output image WIDTH HEIGHT in pixels', default=[32, 32], metavar='N')
  parser.add_argument('--score-threshold', type=float, help='scoring threshold for face detection confidence', default=0.7)
  parser.add_argument('--focallength-mm', help='Focal length in mm', metavar='MM',type=float, required=True)
  parser.add_argument('--sensor-width-mm', help='Sensor width in mm', metavar='MM',type=float, required=True)
  parser.add_argument('--sensor-height-mm', help='Sensor height in mm', metavar='MM',type=float, required=True)
  parser.add_argument('--elevation-m', help='Elevation of camera in m', default=0.0, metavar='M',type=float)
  parser.add_argument('--tilt-deg', help='Camera tilt (straight down is 0 degrees)', default=0.0, metavar='DEG',type=float)
  parser.add_argument('--roll-deg', help='Camera roll (horizontal is 0 degrees)', default=0.0, metavar='DEG',type=float)
  parser.add_argument('--heading-deg', help='Camera heading (straight ahead is 0 degrees)', default=0.0, metavar='DEG',type=float)
  parser.add_argument('--pos-x-m', help='Camera X position in m', default=0.0, metavar='M',type=float)
  parser.add_argument('--pos-y-m', help='Camera Y position in m', default=0.0, metavar='M',type=float)
  parser.add_argument('--lens-distortion', help='Supply the 3 Brown Lens Distortion model parameters: K1 K2 K3', default=None, nargs=3, metavar='N',type=float)
  # dummy entry for --help output, but any such options should be swallowed up by optfileparser.
  parser.add_argument('--options-file', help="Read some command-line options from file also.",
                      metavar='FILE', action='append', default=None)
  args = parser.parse_args(args=argv)

  verbose = args.verbose

  img = cv2.imread(args.input)

  img_h, img_w, _ = img.shape

  projparams = {'focallength_mm':args.focallength_mm,
                'sensor_width_mm':args.sensor_width_mm,
                'sensor_height_mm':args.sensor_height_mm,
                'image_width_px':img_w,
                'image_height_px':img_h}

  spatparams = {'elevation_m':args.elevation_m,
                'pos_x_m':args.pos_x_m,
                'pos_y_m':args.pos_y_m,
                'tilt_deg':args.tilt_deg,
                'heading_deg':args.heading_deg,
                'roll_deg':args.roll_deg}

  V(f'Rectilinear Projection Parameters\n{json.dumps(projparams)}')
  V(f'Spatial Orientation Parameters\n{json.dumps(spatparams)}')

  dis = None
  if args.lens_distortion:
    k1, k2, k3 = args.lens_distortion
    V(f'Brown Lens Distortion Parameters\nk1={k1} k2={k2} k3={k3}')
    dis = ct.BrownLensDistortion(k1, k2, k3)
  cam = ct.Camera(ct.RectilinearProjection(**projparams), ct.SpatialOrientation(**spatparams), dis)


  if args.detections_json_in:
    with open(args.detections_json_in, 'r') as f:
      res = json.load(f)
  else:
    if args.backend == 'mtcnn':
      from backends.mtcnn_backend import MTCNNBackend
      d = MTCNNBackend(score_threshold=args.score_threshold)
    else:
      from backends.yn_backend import YNBackend
      d = YNBackend(score_threshold=args.score_threshold)
    res = d.run(img)

  if args.detections_json_out:
    with open(args.detections_json_out, 'w') as f:
      json.dump(res, f, sort_keys=True, indent=4)

  pts = []
  if args.detections_out:
    det_img = np.copy(img)
  for r in res:
    x=r['x']
    y=r['y']
    w=r['w']
    h=r['h']

    bottomCentre = np.array([x + w / 2.0, y + h])
    pt = cam.spaceFromImage(bottomCentre)[:2]
    V(f"xywh=[{x} {y} {w} {h}] bc={bottomCentre} pt={pt}")
    pts.append(pt)

    if args.detections_out:
      cv2.rectangle(det_img, (x, y), (x+w, y+h), (0, 255, 0), args.detections_box_thickness)

  if args.detections_out:
    cv2.imwrite(args.detections_out, det_img)

  # normalised pts
  npts=np.array(pts)
  npts-=np.average(npts,axis=0)
  npts/=np.max(2*np.abs(npts),axis=0)
  npts+=[0.5,0.5] 

  if verbose:
    # output a matrix version of topdown
    outw=20
    outh=20
    m=np.copy(npts)
    m*=[outw-1,outh-1]
    out = np.zeros((outw, outh), dtype=np.uint8)
    m=m.astype(np.uint)
    out[m[:,0],m[:,1]]=1
    with np.printoptions(threshold=np.inf):
      V(out)

  if args.topdown_out:
    outw, outh = args.topdown_image_size
    m=np.copy(npts)
    m*=[outw-1, outh-1]
    out_img = np.zeros((outh, outw, 3), dtype=np.uint8)
    m=m.astype(np.uint)
    out_img[m[:,1],m[:,0]]=(0,255,0)
    cv2.imwrite(args.topdown_out, np.flipud(out_img))

if __name__=="__main__":
  main()

