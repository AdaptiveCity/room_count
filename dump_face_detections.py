from pathlib import Path
import argparse
import cv2
import json

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('input', type=str, nargs='+', help='image input file(s)')
  parser.add_argument('--backend', type=str, help='detection library: yunet or mtcnn', default='yunet')
  parser.add_argument('--score-threshold', type=float, help='scoring threshold for face detection confidence', default=0.7)
  parser.add_argument('--verbose', default=False, help='Verbose output (not suitable for a detections file)', action='store_true')
  parser.add_argument('--default-output', '-d', default=False, help='Write JSON output to <input image name>.det file(s).', action='store_true')
  args = parser.parse_args()
  if isinstance(args.input,str): args.input=[args.input]

  if args.backend == 'mtcnn':
    from backends.mtcnn_backend import MTCNNBackend
    d = MTCNNBackend(score_threshold=args.score_threshold)
  else:
    from backends.yn_backend import YNBackend
    d = YNBackend(score_threshold=args.score_threshold)

  for inpfile in args.input:
    img = cv2.imread(inpfile)
    res = d.run(img)

    if args.verbose:
      print(json.dumps({ 'n_results': len(res), 'detections': res }, sort_keys=True, indent=4))

    if args.default_output:
      outfile = Path(inpfile).with_suffix('.det')
      with open(outfile, 'w') as f:
        json.dump(res, f)
        print(f'Wrote JSON to {outfile}')
    elif not args.verbose:
      print(json.dumps(res, sort_keys=True, indent=4))


if __name__=="__main__":
  main()

