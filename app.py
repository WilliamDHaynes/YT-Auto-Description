import os
import threading
from tkinterdnd2 import DND_FILES, TkinterDnD
import customtkinter as ctk
from dotenv import load_dotenv
from openai import OpenAI

# Import your custom tools
from youtube_fetcher import get_youtube_examples
from transcriber import transcribe_video

# Load environment variables and set up OpenAI
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

# --- Set Modern UI Theme ---
ctk.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"

def generate_logic():
    video_file = video_path_entry.get().strip("{}") 
    basic_info = info_textbox.get("0.0", "end").strip()
    
    if not video_file or not os.path.exists(video_file):
        update_output("\nError: Please drag and drop a valid video file.")
        reset_button()
        return
        
    if not basic_info:
        update_output("\nError: Please enter some basic info about the video.")
        reset_button()
        return

    try:
        update_output("\n[1/3] Fetching YouTube examples...\n")
        examples = get_youtube_examples(basic_info, max_results=3)
        
        update_output("[2/3] Extracting audio & transcribing video (this might take a minute)...\n")
        transcript = transcribe_video(video_file)
        
        update_output("[3/3] Sending data to OpenAI for final description...\n")
        
        # --- THE MASTER PROMPT (NO EMOJIS) ---
        prompt = f"""
        You are an expert YouTube SEO strategist. 
        I am uploading a new gaming video. Here is the core premise: "{basic_info}"
        
        Please write a highly engaging YouTube description for this video. 
        Match the general style, tone, and formatting of these top-ranking examples. Do NOT use any emojis anywhere in the output:
        {examples}
        
        Next, read this transcript of the video. Summarize the key events into 5 to 8 engaging, timestamped chapters. Format the timestamps as [MM:SS] - Chapter Title.
        
        Transcript:
        {transcript}
        
        Finally, at the very bottom of the description, permanently append this exact block of text exactly as written, with no emojis:
        
        Find me!
        Twitch: https://twitch.tv/nimitz1
        Instagram: https://www.instagram.com/nimitztv/
        TikTok: https://www.tiktok.com/@nimitzzzzzzz
        Facebook: https://www.facebook.com/profile.php?id=61588378366432
        
        My Setup:
        Mic: Audio-Technica AT2020
        GPU: NVIDIA GeForce RTX 5070
        CPU: i7-14700k
        MB: GIGABYTE Z790 AORUS ELITE AX
        """
        
        response = client.chat.completions.create(
            model="gpt-4o-mini", 
            messages=[
                {"role": "system", "content": "You are a helpful YouTube assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        
        final_description = response.choices[0].message.content
        
        # Clear the box and post the final result!
        output_textbox.delete("0.0", "end")
        output_textbox.insert("end", final_description)
        
    except Exception as e:
        update_output(f"\nAn error occurred: {e}")
        
    finally:
        reset_button()

# --- Helper Functions for the GUI ---
def update_output(text):
    output_textbox.insert("end", text)
    output_textbox.see("end")

def reset_button():
    generate_btn.configure(state="normal", text="Generate Description")

def start_generation_thread():
    generate_btn.configure(state="disabled", text="Working...")
    output_textbox.delete("0.0", "end")
    threading.Thread(target=generate_logic, daemon=True).start()

def drop(event):
    file_path = event.data
    video_path_entry.delete(0, "end")
    video_path_entry.insert(0, file_path)

# --- Modern GUI Construction ---
root = TkinterDnD.Tk()
root.title("YouTube Description & Chapter Generator")
root.geometry("750x850")
root.configure(bg="#242424") # Matches the CustomTkinter dark mode background

# Main container frame
main_frame = ctk.CTkFrame(root, corner_radius=15)
main_frame.pack(fill="both", expand=True, padx=20, pady=20)

# Video File Input
ctk.CTkLabel(main_frame, text="Drag & Drop Video File Anywhere:", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(20, 5))
video_path_entry = ctk.CTkEntry(main_frame, width=650, height=40, placeholder_text="C:/path/to/video.mp4")
video_path_entry.pack(pady=5)

# Basic Info Input
ctk.CTkLabel(main_frame, text="Basic Video Info (Game, topic, vibe):", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(20, 5))
info_textbox = ctk.CTkTextbox(main_frame, width=650, height=80, corner_radius=8)
info_textbox.pack(pady=5)

# Generate Button
generate_btn = ctk.CTkButton(main_frame, text="Generate Description", command=start_generation_thread, height=50, width=250, font=ctk.CTkFont(size=16, weight="bold"))
generate_btn.pack(pady=25)

# Output Box
ctk.CTkLabel(main_frame, text="Generated Description & Timestamps:", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(10, 5))
output_textbox = ctk.CTkTextbox(main_frame, width=650, height=400, corner_radius=8)
output_textbox.pack(pady=5)

# Bind the drag and drop to the ENTIRE root window
root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', drop)

root.mainloop()