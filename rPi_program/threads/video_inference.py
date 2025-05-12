import cv2
import json
import os
import numpy as np
import tflite_runtime.interpreter as tflite

def load_labels(label_path):
    with open(label_path, 'r') as f:
        return [line.strip() for line in f.readlines()]

def run_tflite_inference(video_file, day_folder, day, Name, replicate, ID, model_path='yolov8n-float32.tflite', label_path='coco_labels.txt'):
    try:
        # Load TFLite model
        interpreter = tflite.Interpreter(model_path=model_path)
        interpreter.allocate_tensors()

        # Get input and output details
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()
        
        # Load labels
        labels = load_labels(label_path)
        
        # Open video file
        cap = cv2.VideoCapture(video_file)
        frame_count = 0
        inference_data = []
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
                
            # Preprocess frame
            input_shape = input_details[0]['shape'][1:3]  # Expected [1, height, width, 3]
            processed_frame = cv2.resize(frame, input_shape)
            processed_frame = processed_frame.astype(np.float32) / 255.0
            processed_frame = np.expand_dims(processed_frame, axis=0)
            
            # Run inference
            interpreter.set_tensor(input_details[0]['index'], processed_frame)
            interpreter.invoke()
            
            # Get detection results
            boxes = interpreter.get_tensor(output_details[0]['index'])
            classes = interpreter.get_tensor(output_details[1]['index'])
            scores = interpreter.get_tensor(output_details[2]['index'])
            
            # Process results for this frame
            frame_data = {
                'frame': frame_count,
                'boxes': boxes[scores > 0.5].tolist(),
                'classes': [labels[int(i)] for i in classes[scores > 0.5]],
                'confidences': scores[scores > 0.5].tolist()
            }
            
            inference_data.append(frame_data)
            frame_count += 1
        
        cap.release()
        
        # Save results to JSON
        inference_file = os.path.join(day_folder, 
                                    f"{day}_{Name}_{replicate}_{ID}_yolo_results.json")
        
        with open(inference_file, 'w') as f:
            json.dump(inference_data, f)
            
        print(f"TFLite inference completed for {video_file}")
        
    except Exception as e:
        print(f"Error during TFLite inference: {e}")