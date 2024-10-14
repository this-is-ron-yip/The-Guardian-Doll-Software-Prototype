import argparse
import tempfile
import queue
import sys

import sounddevice as sd
import soundfile as sf
import numpy  
assert numpy  
q = queue.Queue()


def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(indata.copy())

def record():
    try:
        samplerate = 16000
        filename = tempfile.mktemp(prefix='audio', suffix='.wav', dir='')

        # Make sure the file is opened before recording anything:
        with sf.SoundFile(filename, mode='x', samplerate=samplerate,
                        channels=1, subtype="PCM_16") as file:
            with sd.InputStream(samplerate=samplerate,
                                channels=1, callback=callback):
                print('#' * 80)
                print('press Ctrl+C to stop the recording')
                print('#' * 80)
                while True:
                    file.write(q.get())

    except KeyboardInterrupt:
        print('\nRecording finished: ' + repr(filename))
        return filename
    except Exception as e:
        exit(type(e).__name__ + ': ' + str(e))
