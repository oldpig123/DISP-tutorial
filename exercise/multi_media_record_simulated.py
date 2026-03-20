import scipy.io.wavfile as wav
import numpy as np
import simpleaudio as sa
import time

def simulate_recording(input_wav, output_wav, duration_sec=2):
    # 1. Load the "Source" file (Simulation of the environment)
    fs, data = wav.read(input_wav)
    if data.ndim > 1:
        data = data[:, 0] # Use mono for recording simulation
    
    # 2. Setup constants (From Slides 9-10)
    chunk = 1024
    num_chunks = int(fs / chunk * duration_sec)
    vocal = []
    
    print(f"--- SIMULATED RECORDING STARTED ---")
    print(f"Mocking a microphone using: {input_wav}")
    
    # 3. The "Tutorial" Loop (Simulating Slide 10)
    for i in range(num_chunks):
        # We simulate "waiting" for the microphone (44.1kHz real-time speed)
        # 1024 samples / 44100 samples per sec = ~23ms per chunk
        # time.sleep(chunk / fs) 
        
        # Pull 1024 samples from our source file instead of a microphone
        start_idx = (i * chunk) % len(data)
        end_idx = start_idx + chunk
        
        # Extract chunk and convert to bytes (exactly what stream.read(chunk) returns)
        audio_chunk = data[start_idx:end_idx].tobytes()
        
        # Add to our recording list (Slide 10 logic)
        vocal.append(audio_chunk)
        
        if i % 20 == 0:
            print(f"Recorded chunk {i}/{num_chunks}...")

    print("--- SIMULATED RECORDING FINISHED ---")
    
    # 4. Save and Play (Slide 10 + Playback logic)
    recorded_bytes = b"".join(vocal)
    
    # Save the simulated recording
    recorded_np = np.frombuffer(recorded_bytes, dtype=np.int16)
    wav.write(output_wav, fs, recorded_np)
    print(f"Simulated recording saved to: {output_wav}")
    
    # Play it back!
    print("Playing back the simulated recording...")
    play_obj = sa.play_buffer(recorded_bytes, 1, 2, fs)
    play_obj.wait_done()

if __name__ == "__main__":
    import os
    os.makedirs("exercise/simulation", exist_ok=True)
    simulate_recording("VocalSignal/Alarm01.wav", "exercise/simulation/mock_mic.wav", duration_sec=3)
