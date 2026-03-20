import simpleaudio as sa
import scipy.io.wavfile as wav
import os

record_path = "exercise/multi_media_record/test_record.wav"

if not os.path.exists(record_path):
    print(f"Error: {record_path} not found. Please run the recording script first.")
else:
    print(f"Playing {record_path}...")
    
    # Load the recording
    fs, data = wav.read(record_path)
    
    # SimpleAudio expects raw bytes or a buffer with correct parameters
    # Since we saved it as int16, we can play it directly
    play_obj = sa.play_buffer(data, 1, 2, fs)
    
    print("Wait for audio to finish...")
    play_obj.wait_done()
    print("Playback finished (note: a segmentation fault might occur now during cleanup).")
