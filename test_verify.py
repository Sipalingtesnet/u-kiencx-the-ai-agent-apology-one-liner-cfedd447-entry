import subprocess
import hashlib
import os

def run_main():
    result = subprocess.run(["python3", "main.py"], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"main.py failed: {result.stderr}")
        return None
    
    path = "/output/entry.txt"
    if not os.path.exists(path):
        print("/output/entry.txt does not exist")
        return None
        
    with open(path, "rb") as f:
        content_bytes = f.read()
        
    return content_bytes

def verify():
    # Run 1
    bytes1 = run_main()
    if bytes1 is None:
        print("Match: False (Run 1 failed)")
        return
    hash1 = hashlib.sha256(bytes1).hexdigest()
    
    # Run 2
    bytes2 = run_main()
    if bytes2 is None:
        print("Match: False (Run 2 failed)")
        return
    hash2 = hashlib.sha256(bytes2).hexdigest()
    
    # Check UTF-8, length, trailing newline
    try:
        text = bytes1.decode("utf-8")
    except UnicodeDecodeError:
        print("Match: False (Not valid UTF-8)")
        return
        
    length = len(text)
    if not (1 <= length <= 159):
        print(f"Match: False (Invalid length: {length})")
        return
        
    if text.endswith("\n") or text.endswith("\r"):
        print("Match: False (Has trailing newline)")
        return
        
    if not text.strip():
        print("Match: False (Only whitespace)")
        return
        
    hashes_match = (hash1 == hash2)
    print(f"Match: {hashes_match}")

if __name__ == "__main__":
    verify()
