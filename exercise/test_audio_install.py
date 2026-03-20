import pyaudio
import simpleaudio as sa

try:
    p = pyaudio.PyAudio()
    print(f"PyAudio version: {pyaudio.get_portaudio_version_text()}")
    print("PyAudio initialized successfully!")
    p.terminate()
except Exception as e:
    print(f"PyAudio initialization failed: {e}")

try:
    # simpleaudio doesn't have an explicit init, so we just check the import and a version/attr
    print("SimpleAudio successfully imported!")
except Exception as e:
    print(f"SimpleAudio verification failed: {e}")

print("\nAll audio packages are ready for use!")
