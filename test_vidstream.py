#!/usr/bin/env python3
"""
Test script to debug vidstream issues
"""

import cv2
import numpy as np
from vidstream import ScreenShareClient

def test_opencv_resize():
    """Test OpenCV resize function with different parameter types"""
    print("Testing OpenCV resize function...")
    
    # Create a test frame
    test_frame = np.zeros((480, 640, 3), dtype=np.uint8)
    
    # Test different resolution formats
    resolutions = [
        (1280, 720),
        (int(1280), int(720)),
        [1280, 720],
        [int(1280), int(720)]
    ]
    
    for i, res in enumerate(resolutions):
        try:
            print(f"Testing resolution format {i+1}: {res} (type: {type(res)})")
            resized = cv2.resize(test_frame, res, interpolation=cv2.INTER_AREA)
            print(f"  ✓ Success: {resized.shape}")
        except Exception as e:
            print(f"  ✗ Failed: {e}")

def test_screen_capture():
    """Test basic screen capture functionality"""
    print("\nTesting screen capture...")
    try:
        import pyautogui
        screenshot = pyautogui.screenshot()
        print(f"✓ Screenshot captured: {screenshot.size}")
        return True
    except Exception as e:
        print(f"✗ Screenshot failed: {e}")
        return False

def test_vidstream_client():
    """Test vidstream client creation"""
    print("\nTesting vidstream client creation...")
    
    # Test different ways to create the client
    test_cases = [
        ("Basic client", lambda: ScreenShareClient("127.0.0.1", 9999)),
        ("With resolution tuple", lambda: ScreenShareClient("127.0.0.1", 9999, (1280, 720))),
        ("With resolution list", lambda: ScreenShareClient("127.0.0.1", 9999, [1280, 720])),
        ("With fps", lambda: ScreenShareClient("127.0.0.1", 9999, (1280, 720), 24)),
    ]
    
    for name, client_func in test_cases:
        try:
            print(f"Testing {name}...")
            client = client_func()
            print(f"  ✓ Success: {type(client)}")
        except Exception as e:
            print(f"  ✗ Failed: {e}")

if __name__ == "__main__":
    print("=== Vidstream Debug Test ===\n")
    
    test_opencv_resize()
    test_screen_capture()
    test_vidstream_client()
    
    print("\n=== Test Complete ===")
