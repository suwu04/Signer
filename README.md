# 🌉 SignBridge: Text-to-Sign Language Translator (Web Demo)

This repository contains the **web-based, public-facing component** of the SignBridge translator, a project designed to **bridge the communication gap** by translating text and speech into Indian Sign Language (ISL) animations.

---

## ✨ Web App Features (`index.html`)

The live web application focuses purely on translating **English input into ISL animations**. It is built using standard web technologies: **HTML**, **CSS (Tailwind)**, and **vanilla JavaScript**.

* ### 🎤 Speech-to-Text Input
    Users can click the microphone button to utilize their device's native **Web Speech API**, allowing for **direct voice input** of sentences.

* ### 🖼️ Text-to-Sign Animation
    The application **tokenizes** the input, maps the resulting words, letters, and numbers to known sign language images, and plays them back in a sequential **animation**.

---

## 💻 Full Pipeline Implementation (Desktop Only)

The comprehensive sign language translation system is maintained in **Python** and includes the high-performance real-time detection component, which is too large to host in this web repository.

### 🖐️ Sign-to-Text Feature

The core functionality for **real-time sign recognition** (watching the user sign and converting it to text) is contained within the `app.py` script.

* **Technology Stack:** This pipeline utilizes **YOLOv8** (from Ultralytics) running on **PyTorch/OpenCV** for the real-time object detection and classification of hand gestures.

### 🛠️ Required Local Directory Structure

To run the full feature set (**Sign-to-Text AND Text-to-Sign**) using `app.py`, you must arrange the following files and folders relative to your main project directory. The structure must match the configuration in your Python script.

| Path | Contents | Purpose |
| :--- | :--- | :--- |
| `app.py` | (Your main executable script) | Starts the dual-mode application. |
| `Words/` | (Contains `Dataset_for_words/` folder) | Required by the Python script to find word data and models. |
| `Letters/` | (Contains `runs/` folder for letters model) | Required by the Python script to find letter data and models. |
| `Words/.../isl_yolo_words/weights/best.pt` | (Your trained model weights) | Crucial. Used for live **Word detection**. |
| `Letters/.../isl_yolo_det2/weights/best.pt` | (Your trained model weights) | Crucial. Used for live **Letter detection** (fallback). |
| `WORDS_EXAMPLES_DIR` | (e.g., `Words/.../examples_per_class`) | Static images for the **Text-to-Sign** feature. |
| `LETTERS_EXAMPLES_DIR` | (e.g., `Letters/.../examples_per_class_l`) | Static images for the **Text-to-Sign** feature. |

### Running the Desktop Application

The full system requires specific Python dependencies (likely `ultralytics`, `torch`, `opencv-python`, `pillow`, `tkinter`). Install them and ensure your directory structure matches the configuration in `app.py`.

To run the full feature set locally:

```bash
python app.py

:)
