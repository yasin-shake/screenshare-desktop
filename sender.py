# sender.py
# Run this on the machine that will SHARE its screen.

import threading
from vidstream import ScreenShareClient
import argparse
import time
import sys

def main():
    parser = argparse.ArgumentParser(description="Screen stream sender")
    parser.add_argument("receiver_ip", help="IP address of the receiver machine")
    parser.add_argument("--port", type=int, default=9999, help="Receiver port (default: 9999)")
    # Optional tuning:
    parser.add_argument("--fps", type=int, default=24, help="Frames per second (default: 24)")
    parser.add_argument("--width", type=int, default=1280, help="Capture width (default: 1280)")
    parser.add_argument("--height", type=int, default=720, help="Capture height (default: 720)")
    args = parser.parse_args()

    # Note: ScreenShareClient in vidstream accepts (host, port, resolution=(w,h), fps=?)
    # Ensure resolution values are integers to avoid OpenCV type errors
    try:
        client = ScreenShareClient(
            args.receiver_ip,
            args.port,
            (int(args.width), int(args.height)),
            int(args.fps)
        )
    except Exception as e:
        print(f"[Sender] Error creating client: {e}")
        print("[Sender] Trying with default resolution...")
        # Try with default resolution if custom resolution fails
        client = ScreenShareClient(
            args.receiver_ip,
            args.port
        )

    t = threading.Thread(target=client.start_stream, daemon=True)
    t.start()

    print(f"[Sender] Streaming screen to {args.receiver_ip}:{args.port} "
          f"at {args.width}x{args.height} @{args.fps}fps.")
    print("Press Enter to stop...")
    try:
        input()
    except KeyboardInterrupt:
        print("\n[Sender] Interrupted by user.")
    except Exception as e:
        print(f"[Sender] Error: {e}")
    finally:
        try:
            client.stop_stream()
            # give the background thread a moment to exit cleanly
            time.sleep(0.5)
            print("[Sender] Stopped.")
        except Exception as e:
            print(f"[Sender] Error stopping stream: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()
