from faster_whisper import WhisperModel
import os

def SpeechToTextAgent(audio: str) -> str:
    whisper_model_size = "small"  # Adjust model size based on performance needs
    whisper_model = WhisperModel(whisper_model_size, device="cpu", compute_type="int8")

    output_text = ""

    try:
        # Check if audio file exists
        if not os.path.exists(audio):
            raise FileNotFoundError(f"Audio file '{audio}' not found.")

        # Transcribe the audio using the Whisper model
        segments, info = whisper_model.transcribe(
            audio, vad_filter=True, vad_parameters=dict(min_silence_duration_ms=3000)
        )

        for segment in segments:
            output_text += segment.text  # Accumulate transcribed text
        
        if output_text.strip() == "":
            raise ValueError("No speech detected in the audio.")

        return output_text

    except Exception as e:
        print(f"Error in SpeechToTextAgent: {str(e)}")
        return ""
