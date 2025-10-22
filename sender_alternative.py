#!/usr/bin/env python3
"""
Alternative screen sharing sender using mss and socket
This is a more reliable alternative to vidstream
"""

import socket
import pickle
import struct
import threading
import time
import argparse
import sys
from mss import mss
import cv2
import numpy as np

class ScreenShareSender:
    def __init__(self, receiver_ip, port=9999, fps=24, width=1280, height=720):
        self.receiver_ip = receiver_ip
        self.port = port
        self.fps = fps
        self.width = width
        self.height = height
        self.running = False
        self.sock = None
        
    def start_streaming(self):
        """Start streaming the screen"""
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.receiver_ip, self.port))
            print(f"[Sender] Connected to {self.receiver_ip}:{self.port}")
            
            self.running = True
            
            # Capture screen using mss
            with mss() as sct:
                # Get the primary monitor
                monitor = sct.monitors[1]
                
                while self.running:
                    start_time = time.time()
                    
                    # Capture screenshot
                    screenshot = sct.grab(monitor)
                    
                    # Convert to numpy array
                    img = np.array(screenshot)
                    
                    # Convert BGRA to BGR (remove alpha channel)
                    img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
                    
                    # Resize if needed
                    if img.shape[1] != self.width or img.shape[0] != self.height:
                        img = cv2.resize(img, (self.width, self.height))
                    
                    # Compress image
                    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 80]
                    _, buffer = cv2.imencode('.jpg', img, encode_param)
                    
                    # Send image size first
                    size = len(buffer)
                    self.sock.sendall(struct.pack('!I', size))
                    
                    # Send image data
                    self.sock.sendall(buffer)
                    
                    # Control frame rate
                    elapsed = time.time() - start_time
                    sleep_time = max(0, (1.0 / self.fps) - elapsed)
                    time.sleep(sleep_time)
                    
        except Exception as e:
            print(f"[Sender] Streaming error: {e}")
        finally:
            self.stop_streaming()
    
    def stop_streaming(self):
        """Stop streaming"""
        self.running = False
        if self.sock:
            self.sock.close()
            self.sock = None
        print("[Sender] Stopped.")

def main():
    parser = argparse.ArgumentParser(description="Alternative Screen stream sender")
    parser.add_argument("receiver_ip", help="IP address of the receiver machine")
    parser.add_argument("--port", type=int, default=9999, help="Receiver port (default: 9999)")
    parser.add_argument("--fps", type=int, default=24, help="Frames per second (default: 24)")
    parser.add_argument("--width", type=int, default=1280, help="Capture width (default: 1280)")
    parser.add_argument("--height", type=int, default=720, help="Capture height (default: 720)")
    args = parser.parse_args()

    sender = ScreenShareSender(
        args.receiver_ip,
        args.port,
        args.fps,
        args.width,
        args.height
    )

    # Start streaming in a separate thread
    stream_thread = threading.Thread(target=sender.start_streaming, daemon=True)
    stream_thread.start()

    print(f"[Sender] Streaming screen to {args.receiver_ip}:{args.port} "
          f"at {args.width}x{args.height} @{args.fps}fps.")
    print("Press Enter to stop...")
    
    try:
        input()
    except KeyboardInterrupt:
        print("\n[Sender] Interrupted by user.")
    finally:
        sender.stop_streaming()

if __name__ == "__main__":
    main()
