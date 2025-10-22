#!/usr/bin/env python3
"""
Alternative screen sharing receiver using socket
This is a more reliable alternative to vidstream
"""

import socket
import struct
import threading
import cv2
import numpy as np
import argparse

class ScreenShareReceiver:
    def __init__(self, host="0.0.0.0", port=9999):
        self.host = host
        self.port = port
        self.running = False
        self.sock = None
        
    def start_receiving(self):
        """Start receiving screen stream"""
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind((self.host, self.port))
            self.sock.listen(1)
            
            print(f"[Receiver] Listening on {self.host}:{self.port}")
            
            while self.running:
                try:
                    conn, addr = self.sock.accept()
                    print(f"[Receiver] Connected to {addr}")
                    
                    with conn:
                        while self.running:
                            # Receive image size
                            size_data = conn.recv(4)
                            if not size_data:
                                break
                                
                            size = struct.unpack('!I', size_data)[0]
                            
                            # Receive image data
                            data = b''
                            while len(data) < size:
                                packet = conn.recv(size - len(data))
                                if not packet:
                                    break
                                data += packet
                            
                            if len(data) == size:
                                # Decode image
                                nparr = np.frombuffer(data, np.uint8)
                                img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                                
                                if img is not None:
                                    # Display image in fullscreen
                                    cv2.namedWindow('Screen Share', cv2.WINDOW_NORMAL)
                                    cv2.setWindowProperty('Screen Share', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                                    cv2.imshow('Screen Share', img)
                                    
                                    # Check for exit key (ESC or 'q')
                                    key = cv2.waitKey(1) & 0xFF
                                    if key == 27 or key == ord('q'):  # ESC or 'q'
                                        print("[Receiver] Exit key pressed, stopping...")
                                        self.running = False
                                        break
                                    
                except Exception as e:
                    if self.running:
                        print(f"[Receiver] Connection error: {e}")
                    break
                    
        except Exception as e:
            print(f"[Receiver] Server error: {e}")
        finally:
            self.stop_receiving()
    
    def stop_receiving(self):
        """Stop receiving"""
        self.running = False
        if self.sock:
            self.sock.close()
            self.sock = None
        cv2.destroyAllWindows()
        print("[Receiver] Stopped.")

def main():
    parser = argparse.ArgumentParser(description="Alternative Screen stream receiver")
    parser.add_argument("--host", default="0.0.0.0",
                        help="IP to bind the receiver on (default: 0.0.0.0 for all interfaces)")
    parser.add_argument("--port", type=int, default=9999, help="Port to listen on (default: 9999)")
    args = parser.parse_args()

    receiver = ScreenShareReceiver(args.host, args.port)

    # Start receiving in a separate thread
    receive_thread = threading.Thread(target=receiver.start_receiving, daemon=True)
    receiver.running = True
    receive_thread.start()

    print("Press Enter to stop, or ESC/'q' in the video window to exit...")
    try:
        input()
    except KeyboardInterrupt:
        print("\n[Receiver] Interrupted by user.")
    finally:
        receiver.stop_receiving()

if __name__ == "__main__":
    main()
