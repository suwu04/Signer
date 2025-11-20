# SignBridge (Streamlit App)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-ff4b4b)
![Status](https://img.shields.io/badge/Status-Active-success)

A web-based **Text-to-Sign** and **Voice-to-Sign** translator for Indian Sign Language (ISL), built with Python and Streamlit. This application bridges the communication gap by converting spoken or written language into visual sign language animations.

---

## Features

* **Real-time Animation:** Instantly translates input text into sign language image sequences.
* ** Voice Support:** Integrated microphone support to translate speech directly into sign language.
* ** Smart Fallback:** Automatically checks for whole-word signs; if unavailable, it seamlessly falls back to letter-by-letter fingerspelling.
* ** Modern UI:** A clean, user-friendly interface designed with Dark Mode support.

---
##Tech Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Frontend** | Streamlit | Web interface and state management |
| **Image Processing** | Pillow (PIL) | Handling and rendering image sequences |
| **Audio Processing** | SpeechRecognition | Converting speech to text |
| **Audio Input** | PyAudio | Microphone input handling |

---

## Setup & Installation

Follow these steps to set up the project locally.

### 1. Install Dependencies
Ensure you have Python installed. Open your terminal and install the required libraries:

```bash
pip install streamlit Pillow SpeechRecognition pyaudio
```
## Run streamlit app
```bash
streamlit run app.py
```
