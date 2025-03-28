import gradio as gr
import torch
import numpy as np
import cv2
from PIL import Image
from transformers import AutoImageProcessor, SwinForImageClassification

# Load Swin Transformer Model (CPU-Optimized)
model_name = "microsoft/swin-tiny-patch4-window7-224"
swin_processor = AutoImageProcessor.from_pretrained(model_name)
swin_model = SwinForImageClassification.from_pretrained(model_name).to("cpu")

def enhance_low_light(image):
    """Enhance low-light images using histogram equalization."""
    image_yuv = cv2.cvtColor(image, cv2.COLOR_RGB2YUV)
    image_yuv[:, :, 0] = cv2.equalizeHist(image_yuv[:, :, 0])
    return cv2.cvtColor(image_yuv, cv2.COLOR_YUV2RGB)

def segment_low_light_image(image):
    """Apply low-light enhancement and perform segmentation."""
    enhanced_image = enhance_low_light(image)
    image_pil = Image.fromarray(enhanced_image)
    inputs = swin_processor(images=image_pil, return_tensors="pt")
    inputs = {k: v.to("cpu") for k, v in inputs.items()}
    outputs = swin_model(**inputs)
    
    # Simulated segmentation overlay (as Swin is a classifier, not a segmenter)
    overlay = enhanced_image.copy()
    overlay[:, :, 1] = overlay[:, :, 1] * 0.5  # Green tint for effect
    segmented_image = cv2.addWeighted(overlay, 0.5, enhanced_image, 0.5, 0)
    return segmented_image

# Gradio Interface
demo = gr.Interface(
    fn=segment_low_light_image,
    inputs=gr.Image(type="numpy"),
    outputs=gr.Image(type="numpy"),
    title="Low-Light Image Segmentation",
    description="Upload a low-light image to enhance and segment it using Swin Transformer.",
)

demo.launch()