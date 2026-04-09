import whisper
import subprocess
import os
import torch

def extract_audio(video_path, audio_path="temp_audio.wav"):
    print("Extracting audio with FFmpeg...")
    # FFmpeg command to extract audio as a 16kHz mono WAV file (optimal for Whisper)
    command = [
        "ffmpeg",
        "-i", video_path,
        "-vn",               # Disable video processing
        "-acodec", "pcm_s16le", # Audio codec
        "-ar", "16000",      # Audio sample rate
        "-ac", "1",          # Mono audio
        audio_path,
        "-y"                 # Overwrite output file if it exists
    ]
    # Run the command and hide the massive FFmpeg text output
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return audio_path

def transcribe_video(video_path):
    # This checks your hardware and forces it to use your RTX card if available
    device = "cpu"
    print(f"Hardware selected: {device.upper()}")
    print("Loading Whisper model...")
    
    # 'base' is incredibly fast and usually accurate enough for summaries. 
    # You can change this to 'small' or 'medium' later if you want higher accuracy.
    model = whisper.load_model("base", device="cpu")
    
    audio_path = extract_audio(video_path)
    
    print("Transcribing... (This might take a minute depending on video length)")
    result = model.transcribe(audio_path)
    
    # Format the raw data into readable timestamps [MM:SS]
    transcript_lines = []
    for segment in result["segments"]:
        start_time = int(segment["start"])
        minutes = start_time // 60
        seconds = start_time % 60
        timestamp = f"[{minutes:02d}:{seconds:02d}]"
        
        transcript_lines.append(f"{timestamp} {segment['text'].strip()}")
        
    # Delete the temporary audio file to save space
    if os.path.exists(audio_path):
        os.remove(audio_path)
        
    print("Transcription complete!")
    return "\n".join(transcript_lines)

# --- Test Block ---
if __name__ == "__main__":
    # Change this to the exact name of a video file in your project folder
    test_video = "test.mp4" 
    
    if os.path.exists(test_video):
        print("\n--- Final Transcript ---\n")
        print(transcribe_video(test_video))
    else:
        print(f"Error: Drop a short video named '{test_video}' into your folder to test this.")