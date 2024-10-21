import tempfile
import queue
import sys
import sounddevice as sd
import soundfile as sf

q = queue.Queue()

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(indata.copy())

def record():
    try:
        samplerate = 16000
        filename = tempfile.mktemp(prefix='audio', suffix='.wav', dir='audio')  # Save audio files to audio directory

        # Make sure the file is opened before recording anything:
        with sf.SoundFile(filename, mode='x', samplerate=samplerate, channels=1, subtype="PCM_16") as file:
            with sd.InputStream(samplerate=samplerate, channels=1, callback=callback):
                print('Recording... Press Ctrl+C to stop')
                while True:
                    file.write(q.get())

    except KeyboardInterrupt:
        print(f'\nRecording finished: {filename}')
        return filename
    except Exception as e:
        print(f"Error during recording: {e}")
        return None
