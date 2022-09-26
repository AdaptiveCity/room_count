import argparse
import cv2
import json

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('input', type=str, help='image input file')
  parser.add_argument('--backend', type=str, help='detection library: yunet or mtcnn', default='yunet')
  parser.add_argument('--score-threshold', type=float, help='scoring threshold for face detection confidence', default=0.7)
  parser.add_argument('--verbose', default=False, help='Verbose output (not suitable for a detections file)', action='store_true')
  args = parser.parse_args()

  img = cv2.imread(args.input)

  if args.backend == 'mtcnn':
    from backends.mtcnn_backend import MTCNNBackend
    d = MTCNNBackend(score_threshold=args.score_threshold)
  else:
    from backends.yn_backend import YNBackend
    d = YNBackend(score_threshold=args.score_threshold)

  res = d.run(img)

  if args.verbose:
    j = { 'n_results': len(res), 'detections': res }
  else:
    j = res
  print(json.dumps(j, sort_keys=True, indent=4))


if __name__=="__main__":
  main()

