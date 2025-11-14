# 🌉 SignBridge: Text-to-Sign Language Translator (Web Demo)

This repository contains the **web-based, public-facing component** of the SignBridge translator, a project designed to **bridge the communication gap** by translating text and speech into Indian Sign Language (ISL) animations.

The live application is hosted for free using GitHub Pages.

---

## 🚀 Launch the Application

**[Click Here to Launch SignBridge (Live Web Demo)](YOUR_LIVE_GITHUB_PAGES_URL_HERE)**

*(Remember to replace the URL above with the actual link to your live GitHub Pages site.)*

---

## ✨ Web App Features (`index.html`)

The public web application focuses purely on translating **English input into ISL animations**. It is built using standard web technologies: **HTML**, **CSS (Tailwind)**, and **vanilla JavaScript**.

* ### 🎤 Speech-to-Text Input
    Users can click the microphone button to utilize their device's native **Web Speech API**, allowing for **direct voice input** of sentences.

* ### 🖼️ Text-to-Sign Animation
    The application **tokenizes** the input (from typing or speech), maps the resulting words, letters, and numbers to known sign language images, and plays them back in a sequential **animation**.

---

## 💻 Full Pipeline Implementation (Desktop Only)

The comprehensive sign language translation system is maintained separately in Python and is designed for a powerful desktop environment.

### 🖐️ Sign-to-Text Feature

The core functionality for **real-time sign recognition** (watching the user sign and converting it to text) is contained within the `app.py` script.

* **Technology Stack:** This pipeline utilizes **YOLOv8** (from Ultralytics) running on **PyTorch/OpenCV** for the necessary real-time object detection and classification of hand gestures.

### Running the Desktop Application

The full system requires specific Python dependencies and is designed to run locally on machines with access to the camera and sufficient processing power.

To run the full feature set (**Text-to-Sign AND Sign-to-Text**), execute the main application file locally:

```bash
python app.py
