#!/usr/bin/env python3
"""
YOLO webcam app + Text->Sign integrated.

- Live detection uses two YOLO models (words first, letters fallback)
- Text->Sign uses static example images for words and letters and animates them in the image panel
"""

import os
import cv2
import glob
import time
import base64
import threading
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont
from threading import Thread, Event
from ultralytics import YOLO
import torch
from typing import List, Tuple, Dict, Optional

# ---------- CONFIG (edit paths as needed) ----------
WORDS_MODEL_PATH = "Words/Dataset_for_words/runs/isl_yolo_words/weights/best.pt"
LETTERS_MODEL_PATH = "Letters/runs/isl_yolo_det2/weights/best.pt"

# example-image folders used for Text -> Sign (these must contain images like "00_Father.jpg" and "A.jpg")
WORDS_EXAMPLES_DIR = "C:\\Users\\HP\\Desktop\\signbridge\\Words\\Dataset_for_words"

LETTERS_EXAMPLES_DIR = "C:\\Users\\HP\\Desktop\\signbridge\\Letters\\Dataset_for_letters\\examples_per_class_l"

# animation params
FRAME_DURATION = 0.9    # seconds per token when playing text->sign
FPS = 12

# display target size
DISPLAY_W = 640
DISPLAY_H = 480

DEVICE = "cuda:0" if torch.cuda.is_available() else "cpu"

# font for placeholders
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# ---------------------------------------------------

def normalize_classname(s: str) -> str:
    return s.strip().lower().replace(" ", "").replace("-", "").replace("_","")

def load_examples_map(examples_dir: str) -> Dict[str,str]:
    mp = {}
    if not os.path.isdir(examples_dir):
        return mp
    for p in sorted(glob.glob(os.path.join(examples_dir, "*"))):
        name = os.path.basename(p)
        # allow "00_Father.jpg" or "Father.jpg" or "A.jpg"
        parts = name.split("_", 1)
        if len(parts) == 2:
            cls_name = os.path.splitext(parts[1])[0]
        else:
            cls_name = os.path.splitext(name)[0]
        key = normalize_classname(cls_name)
        mp[key] = p
    return mp

# helper to create placeholder frame (PIL Image)
def make_placeholder_image(text: str, size=(DISPLAY_W, DISPLAY_H)) -> Image.Image:
    w, h = size
    bg = Image.new("RGB", (w,h), (0,0,0))
    draw = ImageDraw.Draw(bg)
    try:
        font = ImageFont.truetype(FONT_PATH, 28)
    except Exception:
        font = ImageFont.load_default()
    # measure text
    try:
        bbox = draw.textbbox((0,0), text, font=font)
        tw = bbox[2]-bbox[0]; th = bbox[3]-bbox[1]
    except Exception:
        tw, th = draw.textsize(text, font=font)
    draw.text(((w-tw)//2, (h-th)//2), text, font=font, fill=(255,255,255))
    return bg

class YOLOTkAppCam:
    def __init__(self, master):
        self.master = master
        master.title("YOLO Words+Letters GUI with Text→Sign (Tkinter)")

        # Load YOLO models (detect)
        print("Loading models on device:", DEVICE)
        self.words_model = YOLO(WORDS_MODEL_PATH)
        self.letters_model = YOLO(LETTERS_MODEL_PATH)
        self.words_model.to(DEVICE); self.letters_model.to(DEVICE)
        try:
            self.words_model.fuse(); self.letters_model.fuse()
        except Exception:
            pass
        print("Models loaded.")

        # Load example maps for Text->Sign
        self.WORDS_MAP = load_examples_map(WORDS_EXAMPLES_DIR)
        self.LETTERS_MAP = load_examples_map(LETTERS_EXAMPLES_DIR)
        print(f"Loaded {len(self.WORDS_MAP)} word examples, {len(self.LETTERS_MAP)} letter examples")

        # UI layout
        self.image_panel = tk.Label(master)
        self.image_panel.pack(side=tk.LEFT, padx=10, pady=10)

        right_frame = tk.Frame(master)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Camera controls
        self.btn_start = tk.Button(right_frame, text="Start Camera", command=self.start_camera)
        self.btn_start.pack(pady=3)
        self.btn_stop = tk.Button(right_frame, text="Stop Camera", command=self.stop_camera, state=tk.DISABLED)
        self.btn_stop.pack(pady=3)

        # Confidence slider
        self.lbl_conf = tk.Label(right_frame, text="Confidence: 0.35")
        self.lbl_conf.pack(pady=3)
        self.conf_scale = tk.Scale(right_frame, from_=0.05, to=0.9, resolution=0.01, orient=tk.HORIZONTAL,
                                   label="Confidence Threshold", command=self.update_conf)
        self.conf_scale.set(0.35)
        self.conf_scale.pack(fill=tk.X, pady=3)

        # Text -> Sign UI
        tk.Label(right_frame, text="Text → Sign:").pack(anchor="w", pady=(10,0))
        self.text_entry = tk.Entry(right_frame, width=36)
        self.text_entry.pack(anchor="w", pady=3)
        tk.Button(right_frame, text="Convert Text → Sign", command=self.on_convert_text).pack(anchor="w", pady=3)

        # Output text box
        self.txt_output = tk.Text(right_frame, height=12, wrap=tk.NONE)
        self.txt_output.pack(fill=tk.BOTH, expand=True, pady=5)

        self.fps_label = tk.Label(right_frame, text="FPS: 0")
        self.fps_label.pack(pady=3)

        # camera state
        self.cap = None
        self.running = False
        self.thread = None
        self.stop_event = Event()

        # for animating text->sign
        self.playing = False
        self.play_frames: List[Image.Image] = []
        self.play_index = 0
        self.play_after_id = None

        # show a placeholder initially
        self.display_placeholder()

    def update_conf(self, val):
        self.lbl_conf.config(text=f"Confidence: {float(val):.2f}")

    def display_placeholder(self):
        img = make_placeholder_image("No camera / idle", (DISPLAY_W, DISPLAY_H))
        self.display_image(img)

    def display_image(self, pil_img: Image.Image):
        # resize if too wide
        w, h = pil_img.size
        if w > DISPLAY_W:
            ratio = DISPLAY_W / float(w)
            pil_img = pil_img.resize((DISPLAY_W, int(h * ratio)), Image.ANTIALIAS)
        tk_img = ImageTk.PhotoImage(pil_img)
        self.image_panel.configure(image=tk_img)
        self.image_panel.image = tk_img

    # ---------------- Camera control & loop ----------------
    def start_camera(self):
        if self.cap is not None:
            self.stop_camera()
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            messagebox.showerror("Camera", "Could not open camera.")
            return
        self.running = True
        self.stop_event.clear()
        self.btn_start.config(state=tk.DISABLED); self.btn_stop.config(state=tk.NORMAL)
        self.thread = Thread(target=self.camera_loop, daemon=True)
        self.thread.start()

    def stop_camera(self):
        self.running = False
        self.stop_event.set()
        if self.cap:
            self.cap.release(); self.cap = None
        self.btn_start.config(state=tk.NORMAL); self.btn_stop.config(state=tk.DISABLED)

    def camera_loop(self):
      target_fps = 15.0
      while not self.stop_event.is_set():
        t0 = time.time()
        ret, frame = self.cap.read()
        if not ret:
            continue

        # MIRROR / FLIP CAMERA LEFT–RIGHT
        frame = cv2.flip(frame, 1)

        disp_frame = cv2.resize(frame, (DISPLAY_W, DISPLAY_H))
        overlay_rgb, detections, which = self.infer_on_frame(disp_frame)

        self.master.after(0, self.update_gui_from_cam, overlay_rgb, detections, which, time.time() - t0)

        elapsed = time.time() - t0
        sleep_time = max(0, (1.0 / target_fps) - elapsed)
        if sleep_time > 0:
            self.stop_event.wait(sleep_time)



    def infer_on_frame(self, img_bgr):
        img = img_bgr.copy()
        which = "words"
        dets = []
        overlay = img

        # words model inference
        try:
            r_words = self.words_model.predict(source=img, conf=float(self.conf_scale.get()), imgsz=DEFAULT_IMGSZ if 'DEFAULT_IMGSZ' in globals() else 640, device=DEVICE, verbose=False)
        except Exception:
            r_words = None
        if r_words and len(r_words) > 0 and getattr(r_words[0], "boxes", None) is not None and len(r_words[0].boxes) > 0:
            r = r_words[0]
            try:
                overlay = r.plot()
            except Exception:
                overlay = img.copy()
            names = getattr(r, "names", None)
            dets = self._result_to_detections(r, names)
            which = "words"
        else:
            which = "letters"
            try:
                r_letters = self.letters_model.predict(source=img, conf=float(self.conf_scale.get()), imgsz=DEFAULT_IMGSZ if 'DEFAULT_IMGSZ' in globals() else 640, device=DEVICE, verbose=False)
            except Exception:
                r_letters = None
            if r_letters and len(r_letters) > 0 and getattr(r_letters[0], "boxes", None) is not None and len(r_letters[0].boxes) > 0:
                r = r_letters[0]
                try:
                    overlay = r.plot()
                except Exception:
                    overlay = img.copy()
                names = getattr(r, "names", None)
                dets = self._result_to_detections(r, names)

        # convert overlay to RGB numpy (for display)
        try:
            overlay_rgb = cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB)
        except Exception:
            overlay_rgb = img[:,:,::-1]
        return overlay_rgb, dets, which

    def update_gui_from_cam(self, overlay_rgb, detections, which, frame_latency):
        pil = Image.fromarray(overlay_rgb)
        self.display_image(pil)
        # update text output
        self.txt_output.delete(1.0, tk.END)
        self.txt_output.insert(tk.END, f"mode: live_detection ({which})\n")
        self.txt_output.insert(tk.END, f"detections: {len(detections)}\n")
        for d in detections:
            self.txt_output.insert(tk.END, f"{d['name']} ({d['class_id']}) conf {d['conf']:.3f} box {d['xyxy']}\n")
        self.txt_output.insert(tk.END, f"frame latency: {frame_latency*1000:.1f} ms\n")
        self.fps_label.config(text=f"FPS: ~{int(1.0 / max(0.001, frame_latency))}")

    def _result_to_detections(self, r, names):
        dets = []
        boxes = getattr(r, "boxes", None)
        if boxes is None:
            return dets
        try:
            xyxy = boxes.xyxy.cpu().numpy()
            clsarr = boxes.cls.cpu().numpy().astype(int)
            confs = boxes.conf.cpu().numpy()
            for i in range(len(xyxy)):
                x1,y1,x2,y2 = [float(v) for v in xyxy[i]]
                cid = int(clsarr[i])
                conf = float(confs[i])
                name = names[cid] if (names is not None and cid < len(names)) else str(cid)
                dets.append({"class_id": cid, "name": name, "conf": conf, "xyxy": [x1,y1,x2,y2]})
        except Exception:
            pass
        return dets

    # ---------------- Text -> Sign logic ----------------
    def on_convert_text(self):
        txt = self.text_entry.get().strip()
        if not txt:
            messagebox.showwarning("No text", "Please enter some text to convert.")
            return
        # stop camera while animating (optional)
        self.stop_camera()
        # background generate frames then play
        threading.Thread(target=self._worker_text_to_sign, args=(txt,), daemon=True).start()

    def _worker_text_to_sign(self, text: str):
        try:
            self.set_status("Building token sequence...")
            seq = self.text_to_token_sequence(text)
            self.set_status(f"Sequence length: {len(seq)} tokens")
            # build frames (PIL images) for each token
            frames = []
            missing = []
            for ttype, tok in seq:
                if ttype == "pause":
                    frames.append(make_placeholder_image("pause", (DISPLAY_W, DISPLAY_H)))
                    continue
                img_path = None
                if ttype == "word":
                    img_path = self.WORDS_MAP.get(normalize_classname(tok))
                elif ttype == "letter":
                    img_path = self.LETTERS_MAP.get(normalize_classname(tok))
                if img_path and os.path.exists(img_path):
                    # load and letterbox to display size
                    pil = Image.open(img_path).convert("RGB")
                    pil.thumbnail((DISPLAY_W, DISPLAY_H), Image.LANCZOS)
                    bg = Image.new("RGB", (DISPLAY_W, DISPLAY_H), (0,0,0))
                    x = (DISPLAY_W - pil.width)//2
                    y = (DISPLAY_H - pil.height)//2
                    bg.paste(pil, (x,y))
                    # overlay label at bottom
                    draw = ImageDraw.Draw(bg)
                    try:
                        font = ImageFont.truetype(FONT_PATH, 22)
                    except Exception:
                        font = ImageFont.load_default()
                    label = f"{ttype.upper()}: {tok}"
                    try:
                        bbox = draw.textbbox((0,0), label, font=font)
                        tw = bbox[2]-bbox[0]; th = bbox[3]-bbox[1]
                    except Exception:
                        tw, th = draw.textsize(label, font=font)
                    draw.rectangle([(10, DISPLAY_H-th-20), (10+tw+6, DISPLAY_H-10)], fill=(0,0,0))
                    draw.text((13, DISPLAY_H-th-17), label, font=font, fill=(255,255,255))
                    frames.append(bg)
                else:
                    missing.append((ttype, tok))
                    frames.append(make_placeholder_image(f"MISS: {tok}", (DISPLAY_W, DISPLAY_H)))
            if missing:
                print("[text->sign] Missing tokens:", missing)
            # store & play
            self.play_frames = frames
            self.play_index = 0
            self.playing = True
            self.set_status("Playing sign sequence...")
            self.master.after(0, self._play_next_frame)
        except Exception as e:
            print("Text->Sign error:", e)
            self.set_status("Text->Sign failed")
            messagebox.showerror("Error", str(e))

    def text_to_token_sequence(self, text: str) -> List[Tuple[str,str]]:
        # tokenise simple words and punctuation
        import re
        tokens = re.findall(r"[A-Za-z]+|\d+|[^\sA-Za-z\d]+", text)
        out: List[Tuple[str,str]] = []
        for t in tokens:
            if not t.strip():
                continue
            norm = normalize_classname(t)
            if norm in self.WORDS_MAP:
                out.append(("word", t))
            else:
                # fallback: spell with letters if alphabet present
                if any(ch.isalpha() for ch in t):
                    for ch in t:
                        if ch.isalpha():
                            out.append(("letter", ch))
                        else:
                            out.append(("pause", ch))
                else:
                    out.append(("pause", t))
        return out

    def _play_next_frame(self):
        if not self.playing or not self.play_frames:
            self.set_status("Idle")
            return
        frame = self.play_frames[self.play_index]
        # display frame
        self.display_image(frame)
        # update sequence text
        self.txt_output.delete(1.0, tk.END)
        self.txt_output.insert(tk.END, f"Text→Sign playback: frame {self.play_index+1}/{len(self.play_frames)}\n")
        # advance
        self.play_index += 1
        if self.play_index >= len(self.play_frames):
            # finished playback
            self.playing = False
            self.set_status("Finished playback")
            return
        # schedule next frame
        delay_ms = int(1000 * FRAME_DURATION)
        self.play_after_id = self.master.after(delay_ms, self._play_next_frame)

    def set_status(self, s: str):
        self.txt_output.insert(tk.END, f"STATUS: {s}\n")
        self.fps_label.config(text=f"FPS: N/A")
        self.master.update_idletasks()

    # helper for overlay->base64 (unused but kept)
    def _overlay_to_b64(self, overlay_bgr):
        ret, buf = cv2.imencode(".jpg", overlay_bgr, [int(cv2.IMWRITE_JPEG_QUALITY), 85])
        if not ret:
            return ""
        b64 = base64.b64encode(buf).decode("ascii")
        return "data:image/jpeg;base64," + b64

    def __del__(self):
        self.stop_camera()

if __name__ == "__main__":
    root = tk.Tk()
    app = YOLOTkAppCam(root)
    root.mainloop()
