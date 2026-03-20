import pyaudio
import wave
import numpy as np

def record_audio(output_filename, duration_sec=5):
    pa = pyaudio.PyAudio()
    
    fs = 44100
    chunk = 1024
    channels = 1
    sample_format = pyaudio.paInt16
    
    print(f"Opening stream for {duration_sec} seconds of recording...")
    
    # Based on Slide 9
    stream = pa.open(
        format=sample_format,
        channels=channels,
        rate=fs,
        input=True,
        frames_per_buffer=chunk
    )
    
    vocal = []
    # Calculate how many chunks to read
    # Slide 10 used a count < 200, which is about 4.6 seconds at 44.1kHz/1024
    num_chunks = int(fs / chunk * duration_sec)
    
    print("Recording started... (Please speak into your local microphone)")
    
    for _ in range(num_chunks):
        try:
            data = stream.read(chunk, exception_on_overflow=False)
            vocal.append(data)
        except Exception as e:
            print(f"Error reading chunk: {e}")
            break
            
    print("Recording finished.")
    
    # Close stream
    stream.stop_stream()
    stream.close()
    pa.terminate()
    
    # Save the recorded data
    print(f"Saving to {output_filename}...")
    with wave.open(output_filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(pa.get_sample_size(sample_format))
        wf.setframerate(fs)
        wf.writeframes(b''.join(vocal))
    
    print("File saved successfully.")

if __name__ == "__main__":
    import os
    output_dir = "exercise/multi_media_record"
    os.makedirs(output_dir, exist_ok=True)
    record_audio(f"{output_dir}/test_record.wav", duration_sec=3)
