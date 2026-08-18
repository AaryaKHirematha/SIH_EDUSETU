# EduSetu

EduSetu is an educational translation platform designed to seamlessly translate classroom notes, documents, and videos from English into Hindi and Kannada while meticulously preserving technical terminology, formulas, and morphological structure.

## Features
- **Text & Document Translation**: Supports TXT, PDF, DOCX, and MD file formats.
- **Video Transcription & Translation**: Extract audio from uploaded videos or public video URLs, transcribe it, and generate translated SRT/VTT subtitles.
- **Technical Integrity**: Protected tokens (formulas, equations, programming syntax) are verified against the source using the frozen Gate 1-4 validation logic.
- **Translation History**: Keeps track of your saved translations.
- **Authentication**: JWT-based secure user authentication.

## Architecture
The application follows a decoupled architecture, designed for distributed deployment:

- **Frontend**: React, Vite, React Router, and Vanilla CSS. Deployed separately (e.g., on Vercel).
- **Backend**: FastAPI (Python), SQLite (Auth/History), SQLAlchemy. Hosted on a GPU-capable instance.
- **Machine Learning Pipeline**:
  - `faster-whisper` (CPU/int8) for speech-to-text.
  - `IndicTrans2` (GPU with strict inference lock) for high-accuracy Indic translations.
  - `yt-dlp` and `FFmpeg` for media extraction.

## Local Setup

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Backend
Make sure you have the `gate1_venv` activated (or your equivalent Python environment).
```bash
cd backend
uvicorn api:app --host 0.0.0.0 --port 8000
```

## Environment Variables

**Frontend (`frontend/.env`)**:
- `VITE_API_URL`: The base URL for the backend API. (e.g., `http://127.0.0.1:8000` for local dev).

**Backend (`.env`)**:
- `JWT_SECRET`: A secure random string used to sign JWT tokens. Must be provided for production.
- `MEDIA_TEMP_DIR`: The directory used for processing temporary video/audio files (e.g., `/tmp/edusettu-media`). The application will clean up files here automatically.

## Deployment

1. **Frontend**: The React/Vite frontend can be deployed directly to Vercel. Ensure `VITE_API_URL` is set in your Vercel project settings.
2. **Backend**: The FastAPI backend requires a Python environment and a GPU for IndicTrans2. It cannot be deployed to Vercel Serverless Functions. Deploy it to a GPU-capable provider (e.g., AWS EC2, GCP Compute Engine, RunPod).

## Security Notes
- Video URL translation relies on `yt-dlp`. It supports many public providers, but DRM-protected, private, or login-required videos are not supported.
- Upload limits are strictly enforced (e.g., 50MB for video).
- Temporary files are deleted immediately after processing to conserve disk space.
