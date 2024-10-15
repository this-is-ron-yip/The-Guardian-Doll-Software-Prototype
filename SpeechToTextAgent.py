from faster_whisper import WhisperModel
def SpeechToTextAgent(audio: str) -> str:
    
    whisper_model_size = "small"  

    # Run on GPU with FP16
    # model = WhisperModel(model_size, device="cuda", compute_type="float16")
    # or run on GPU with INT8
    # model = WhisperModel(model_size, device="cuda", compute_type="int8_float16")
    # or run on CPU with INT8
    whisper_model = WhisperModel(whisper_model_size, device="cpu", compute_type="int8")
    
    file=audio
    segments, info = whisper_model.transcribe(file,
        vad_filter=True,
        vad_parameters=dict(min_silence_duration_ms=3000),
    )

    outputtext=""

    #print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

    for segment in segments:
        #print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
        outputtext+=segment.text

    return outputtext
