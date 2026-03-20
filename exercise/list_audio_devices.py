import pyaudio

def list_devices():
    pa = pyaudio.PyAudio()
    print("-" * 50)
    
    device_count = pa.get_device_count()
    print(f"Found {device_count} devices:")
    
    for i in range(device_count):
        device_info = pa.get_device_info_by_index(i)
        is_input = device_info.get('maxInputChannels') > 0
        is_output = device_info.get('maxOutputChannels') > 0
        
        type_str = ""
        if is_input: type_str += "INPUT "
        if is_output: type_str += "OUTPUT "
        
        print(f"Device {i}: {device_info.get('name')}")
        print(f"  Type: {type_str}")
        print(f"  Sampling Rate: {device_info.get('defaultSampleRate')}")
    
    pa.terminate()

if __name__ == "__main__":
    list_devices()
