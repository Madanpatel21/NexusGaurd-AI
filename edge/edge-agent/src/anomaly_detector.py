import numpy as np
from tensorflow.lite import Interpreter

class AnomalyDetector:
    def __init__(self, model_path):
        self.interpreter = Interpreter(model_path)
        self.interpreter.allocate_tensors()

    def detect(self, vibration, temp):
        input_data = np.array([vibration, temp], dtype=np.float32)
        self.interpreter.set_tensor(0, input_data)
        self.interpreter.invoke()
        return self.interpreter.get_tensor(0)[0] > 0.8
