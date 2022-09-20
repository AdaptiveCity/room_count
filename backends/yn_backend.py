import cv2

class YNBackend:
  def __init__(self, score_threshold=0.8):
    model = 'backends/face_detection_yunet_2022mar.onnx'
    self.detector = cv2.FaceDetectorYN_create(model, '', (0, 0), score_threshold=score_threshold)

  def run(self, img):
    h,w = img.shape[:2]
    self.detector.setInputSize((w,h))
    _, faces = self.detector.detect(img)
    out = []
    for f in faces:
      out.append({'confidence': f[-1],
                  'x': f[0], 'y': f[1], 'w': f[2], 'h': f[3]})
    return out
