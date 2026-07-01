YT-Auto-Description


looks at top ranking competitor vidoes, makes a description


Prerequisites

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
