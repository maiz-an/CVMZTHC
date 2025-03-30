# Cartoon Image Matcher

This is a deep learning-based image similarity detection tool using **VGG16** and **cosine similarity**. It allows users to upload an image and find the closest match from a dataset stored in Google Drive.

## Features
- Uses **VGG16** for feature extraction.
- Compares images using **cosine similarity**.
- Supports **Google Drive integration**.
- Interactive **Gradio UI** for easy use.

## Installation
```bash
pip install tensorflow numpy opencv-python-headless gradio pillow scikit-learn
```

## Usage
1. **Mount Google Drive:**
   ```python
   from google.colab import drive
   drive.mount('/content/drive')
   ```
2. **Set your dataset folder path:**
   ```python
   FOLDER_PATH = "/content/drive/MyDrive/cartoons"  # Change this to your folder path
   ```
3. **Run the script:**
   ```python
   python app.py
   ```
4. **Access the Gradio UI** and upload an image to find the best match.

## File Structure
```
📂 Cartoon-Image-Matcher
├── 📜 app.py              # Main Python script
├── 📜 README.md          # Project documentation
├── 📂 cartoons           # Dataset folder (inside Google Drive)
```

## Contributing
Pull requests are welcome! If you find any issues, feel free to report them.

## License
This project is licensed under the **MIT License**.

---
✨ Developed with ❤️ using TensorFlow & Gradio
