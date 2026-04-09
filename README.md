YT-Auto-Description

A modern, local Python GUI application that automates the creation of highly engaging, SEO-optimized YouTube descriptions and timestamped chapters for gaming videos.

Built with CustomTkinter, this tool analyzes top-ranking competitor videos, locally transcribes your gameplay using OpenAI's Whisper, and uses an LLM to write the final description.
Features

    Modern Drag-and-Drop GUI: Built with CustomTkinter for a sleek, dark-mode Windows interface.

    Competitor Analysis: Leverages the YouTube Data API v3 to pull descriptions from top-ranking videos based on your topic.

    Local Audio Transcription: Uses FFmpeg and OpenAI's Whisper model to locally transcribe your .mp4 files without expensive API costs.

    Smart Chapter Generation: Feeds the transcript to OpenAI's gpt-4o-mini to automatically summarize key events into perfectly formatted [MM:SS] timestamps.

    Persistent Custom Footers: Automatically appends permanent social links and PC specs to every description.

Prerequisites

Before running this project, ensure you have the following installed on your system:

    Python 3.11+

    FFmpeg: Must be installed and added to your System PATH for audio extraction.

    API Keys:

        YouTube Data API v3 Key (Google Cloud Console)

        OpenAI API Key (OpenAI Developer Platform)

Setup and Installation

    Clone the repository:
    git clone https://github.com/WilliamDHaynes/YT-Auto-Description.git
    cd YT-Auto-Description

    Create and activate a virtual environment:
    python -m venv venv
    venv\Scripts\activate

    Install the dependencies:
    pip install customtkinter tkinterdnd2 python-dotenv google-api-python-client openai-whisper openai

    Create a .env file in the root directory and add your API keys:
    YOUTUBE_API_KEY=your_key_here
    OPENAI_API_KEY=your_key_here

    Run the application:
    python app.py

Compiling to .exe

If you want to compile the app into a standalone desktop executable, use PyInstaller:
pyinstaller --noconsole --collect-all customtkinter --collect-data tkinterdnd2 --collect-all whisper --collect-all tiktoken app.py

(Note: You will need to manually copy your .env file into the generated dist/app folder before running the executable).