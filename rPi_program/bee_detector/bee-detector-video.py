import ncnn
import cv2
import numpy as np
import time
from pathlib import Path

class BeeDetector:
    def __init__(self, param_path, bin_path, conf_thresh=0.25):
        """Initialize the bee detector"""
        self.net = ncnn.Net()
        self.net.load_param(param_path)
        self.net.load_model(bin_path)
        
        # Print model info to find layer names
        print("Model input names:", self.net.input_names())
        print("Model output names:", self.net.output_names())
        
        # Store the actual input/output names
        self.input_name = self.net.input_names()[0]  # Usually 'in0'
        self.output_name = self.net.output_names()[0]  # Usually 'out0'
        
        self.conf_thresh = conf_thresh
        self.class_names = ['bee', 'feeder']
        self.colors = [(0, 255, 0), (0, 0, 255)]  # Green for bees, Red for feeders
        
    def preprocess_image(self, img):
        """Preprocess image for inference"""
        # Save original dimensions for scaling back
        self.orig_h, self.orig_w = img.shape[:2]
        
        # Resize to model input size
        img = cv2.resize(img, (640, 640))
        # Convert to RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Normalize pixel values
        img = img.astype(np.float32) / 255.0
        
        return img
        
    def detect(self, img):
        """Run detection on preprocessed image"""
        # Convert to NCNN format
        blob = ncnn.Mat(img)
        
        # Create extractor
        ex = self.net.create_extractor()
        ex.input(self.input_name, blob)
        
        # Get output
        _, out = ex.extract(self.output_name)
        
        return self.process_output(out)
    
    def process_output(self, output):
        """Process NCNN output to bounding boxes"""
        detections = []
        
        # Convert NCNN Mat to numpy array
        out_array = np.array(output)
        
        # Process each detection
        for detection in out_array:
            confidence = detection[4]
            
            if confidence >= self.conf_thresh:
                class_id = int(detection[5])
                x1 = detection[0] * self.orig_w / 640
                y1 = detection[1] * self.orig_h / 640
                x2 = detection[2] * self.orig_w / 640
                y2 = detection[3] * self.orig_h / 640
                
                detections.append({
                    'class': self.class_names[class_id],
                    'confidence': confidence,
                    'bbox': [int(x1), int(y1), int(x2), int(y2)]
                })
        
        return detections

def process_video(input_path, output_path, detector):
    """Process video file and save output"""
    # Open video file
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file {input_path}")
        return
    
    # Get video properties
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Create video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    frame_count = 0
    processing_times = []
    
    print("Processing video...")
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        # Process frame
        start_time = time.time()
        
        try:
            # Preprocess
            processed_frame = detector.preprocess_image(frame)
            
            # Detect
            detections = detector.detect(processed_frame)
            
            # Draw detections
            for det in detections:
                x1, y1, x2, y2 = det['bbox']
                class_name = det['class']
                conf = det['confidence']
                color = detector.colors[detector.class_names.index(class_name)]
                
                # Draw box
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                
                # Draw label
                label = f"{class_name} {conf:.2f}"
                cv2.putText(frame, label, (x1, y1-10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        except Exception as e:
            print(f"Error processing frame {frame_count}: {str(e)}")
            continue
            
        # Calculate FPS
        process_time = time.time() - start_time
        processing_times.append(process_time)
        fps_text = f"FPS: {1/process_time:.1f}"
        cv2.putText(frame, fps_text, (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Write frame
        out.write(frame)
        
        # Progress
        frame_count += 1
        if frame_count % 30 == 0:
            print(f"Processed {frame_count}/{total_frames} frames")
    
    # Clean up
    cap.release()
    out.release()
    
    # Print statistics
    if processing_times:
        avg_fps = 1.0 / np.mean(processing_times)
        print(f"\nProcessing complete!")
        print(f"Average FPS: {avg_fps:.1f}")
        print(f"Output saved to: {output_path}")

if __name__ == "__main__":
    # Paths
    model_param = "model.ncnn.param"
    model_bin = "model.ncnn.bin"
    input_video = "input.mp4"
    output_video = "output.mp4"
    
    # Create detector
    detector = BeeDetector(model_param, model_bin, conf_thresh=0.25)
    
    # Process video
    process_video(input_video, output_video, detector)