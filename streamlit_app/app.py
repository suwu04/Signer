import streamlit as st
import os
import glob
import time
from PIL import Image
import speech_recognition as sr

# ================= CONFIGURATION =================
# ⚠️ IMPORTANT: Update these paths to match your actual folder structure
WORDS_DIR = "examples_per_class"
LETTERS_DIR = "examples_per_class_l"

FRAME_DELAY = 0.9  # Seconds between frames
TARGET_SIZE = (640, 480) # Fixed resolution to prevent UI jumping

# ================= UTILS: MAP LOADING =================

def normalize_key(s):
    return s.strip().lower().replace(" ", "").replace("-", "").replace("_", "")

@st.cache_data
def load_image_map(directory):
    """Loads images once and caches the result."""
    mapping = {}
    if not os.path.isdir(directory):
        return mapping
    
    extensions = ['*.jpg', '*.jpeg', '*.png']
    files = []
    for ext in extensions:
        files.extend(glob.glob(os.path.join(directory, ext)))
        
    for p in sorted(files):
        name = os.path.basename(p)
        parts = name.split("_", 1)
        if len(parts) == 2:
            cls_name = os.path.splitext(parts[1])[0]
        else:
            cls_name = os.path.splitext(name)[0]
        
        key = normalize_key(cls_name)
        mapping[key] = p
    return mapping

# ================= LOGIC: SPEECH =================

def listen_to_mic():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        status_placeholder = st.empty()
        status_placeholder.info("🎤 Listening... Speak now!")
        try:
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            status_placeholder.success("Processing audio...")
            text = r.recognize_google(audio)
            return text
        except sr.WaitTimeoutError:
            status_placeholder.warning("No speech detected.")
            return None
        except sr.UnknownValueError:
            status_placeholder.error("Could not understand audio.")
            return None
        except sr.RequestError:
            status_placeholder.error("API unavailable.")
            return None
        except Exception as e:
            status_placeholder.error(f"Error: {e}")
            return None

# ================= UI SETUP =================

st.set_page_config(page_title="SignBridge Web", layout="wide")

# --- DARK MODE CSS ---
st.markdown("""
    <style>
    /* Force Dark Background for the whole app */
    .stApp {
        background-color: #0e1117; /* Standard Streamlit Dark */
        color: #fafafa;
    }
    
    /* Custom styling for headers to ensure visibility */
    h1, h2, h3, p, label {
        color: #ffffff !important;
    }

    /* Sign Label Styling */
    .sign-label {
        font-size: 24px;
        font-weight: bold;
        color: #00ffcc; /* Cyan accent for visibility */
        background-color: #1f2937;
        padding: 10px;
        text-align: center;
        border-radius: 8px;
        margin-top: 10px;
        border: 1px solid #374151;
        width: 100%;
    }
    
    /* Fix input box visibility in dark mode */
    .stTextInput > div > div > input {
        color: white;
        background-color: #262730;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize State
if 'text_input' not in st.session_state:
    st.session_state.text_input = ""
if 'run_animation' not in st.session_state:
    st.session_state.run_animation = False

# Load Data
words_map = load_image_map(WORDS_DIR)
letters_map = load_image_map(LETTERS_DIR)

# ================= MAIN LAYOUT =================

st.title("SignBridge: Sign Language Translator")

# Create a container for the main app content
with st.container():
    col1, col2 = st.columns([1, 1])

    # --- RIGHT COLUMN: CONTROLS ---
    with col2:
        st.subheader("Input Controls")
        
        # Mic Button
        if st.button("🎤 Record Speech", type="secondary", use_container_width=True):
            recognized_text = listen_to_mic()
            if recognized_text:
                st.session_state.text_input = recognized_text
                st.session_state.run_animation = True
                st.rerun()

        # Text Input with Hint/Placeholder
        text_entry = st.text_input(
            "Text to translate:", 
            value=st.session_state.text_input, 
            placeholder="Type here or use the mic...",
            key="text_entry_widget"
        )
        
        # Sync text entry
        if text_entry != st.session_state.text_input:
            st.session_state.text_input = text_entry
            st.session_state.run_animation = True
        
        # Manual Play Button
        if st.button("▶ Play Animation", type="primary", use_container_width=True):
            st.session_state.run_animation = True

        st.markdown("---")
        # Check if data loaded correctly
        if len(words_map) == 0 and len(letters_map) == 0:
            st.error(f"⚠️ No images loaded! Check paths:\n{WORDS_DIR}\n{LETTERS_DIR}")
        else:
            st.info(f"✅ Loaded {len(words_map)} words and {len(letters_map)} letters.")

    # --- LEFT COLUMN: ANIMATION DISPLAY ---
    with col1:
        image_spot = st.empty()
        label_spot = st.empty()
        
        # Default State (Placeholder)
        if not st.session_state.run_animation:
            placeholder_img = Image.new('RGB', TARGET_SIZE, color='#1f2937')
            image_spot.image(placeholder_img, caption="Waiting for input...", use_container_width=True)
        
        else:
            # --- ANIMATION LOGIC ---
            text = st.session_state.text_input
            import re
            tokens = re.findall(r"[A-Za-z0-9]+", text.lower())
            
            frames = []
            
            # Build the sequence
            for token in tokens:
                norm_token = normalize_key(token)
                if norm_token in words_map:
                    frames.append((token, words_map[norm_token]))
                else:
                    # Spell it out
                    for char in token:
                        if char in letters_map:
                            frames.append((char, letters_map[char]))
                        else:
                            frames.append(("...", None))
                
                # Pause between words
                frames.append(("...", None))

            # Play the sequence
            if not frames:
                st.warning("No signable text found.")
            else:
                for txt, img_path in frames:
                    # Standardize image size
                    if img_path and os.path.exists(img_path):
                        raw_img = Image.open(img_path)
                        # Force Resize to fixed dimensions so the UI doesn't jump
                        img = raw_img.resize(TARGET_SIZE)
                        
                        image_spot.image(img, use_container_width=True)
                        label_spot.markdown(f"<div class='sign-label'>SIGN: {txt.upper()}</div>", unsafe_allow_html=True)
                    else:
                        # Pause frame
                        pause_img = Image.new('RGB', TARGET_SIZE, color='#1f2937')
                        image_spot.image(pause_img, use_container_width=True)
                        label_spot.markdown(f"<div class='sign-label'>...</div>", unsafe_allow_html=True)
                    
                    time.sleep(FRAME_DELAY)

            # Reset Animation State
            st.session_state.run_animation = False