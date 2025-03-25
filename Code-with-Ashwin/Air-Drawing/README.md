# **🔥 Gesture-Controlled Magic Wand Effect – Like Harry Potter! 🪄✨**

## developed by Ashwin Mehta
## **📌 Project Overview**
This project allows you to **draw in the air** using hand gestures, creating **glowing fire trails** just like in Harry Potter! It uses **AI-powered hand tracking** to detect your finger movements and displays **real-time fire effects** following your hand.

---

## **🛠️ Technologies Used**
✅ **Python** 🐍  
✅ **OpenCV + Mediapipe** (Hand Tracking) 🖐  
✅ **NumPy** (Efficient Image Processing) 📊  
✅ **Pygame** (Fire & Particle Effects) 🔥  
✅ **Conda Environment** (For package management)  

---

## **📂 Project Folder Structure**
```
📂 Magic_Wand_Effect
│── 📂 utils
│   ├── hand_tracking.py          # Hand tracking module
│
│── main.py                 # Main magic drawing script
│── requirements.txt               # Dependencies
│── README.md                      # Documentation
```

---

## **📥 Installation & Setup**
### **1️⃣ Create a Conda Environment**
```bash
conda create --name magicwand python=3.9 -y
conda activate magicwand
```

### **2️⃣ Install Dependencies**
Run the following command to install all required packages:
```bash
pip install -r requirements.txt
```

---

## **🚀 How to Run the Project**
### **3️⃣ Run the Magic Wand Program**
```bash
python magic_wand.py
```

---

## **🎮 Controls & Features**
🖐 **Move Your Index Finger** → Draw glowing magic trails  
🔥 **Fire Particles Follow Finger Movement**  
🧹 **Touch Thumb & Index Finger** → **Clear Screen**  
🛑 **Press 'Q' to Exit**  

---

## **💡 Why is This Innovative?**
🔹 **Touchless Interaction** – Control visuals with hand gestures  
🔹 **AI-Powered** – Uses real-time computer vision  
🔹 **Augmented Reality Ready** – Can be integrated into VR/AR apps  

Would love to hear your feedback! What **other magical features** would you add? 🪄✨  

---

## **🛑 Troubleshooting**
❌ **Error: ModuleNotFoundError** → Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```
❌ **Webcam Not Working?** → Ensure your camera is accessible and not being used by another app.  
❌ **Laggy Performance?** → Reduce resolution in `cv2.VideoCapture(0)`.  

---

## **📜 License**
This project is **open-source**. Feel free to modify and enhance it!

