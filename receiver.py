# receiver.py
# Run this on the machine that will VIEW the shared screen.

import threading
from vidstream import StreamingServer
import argparse

def main():
    parser = argparse.ArgumentParser(description="Screen stream receiver")
    parser.add_argument("--host", default="0.0.0.0",
                        help="IP to bind the receiver on (default: 0.0.0.0 for all interfaces)")
    parser.add_argument("--port", type=int, default=9999, help="Port to listen on (default: 9999)")
    args = parser.parse_args()

    server = StreamingServer(args.host, args.port)

    t = threading.Thread(target=server.start_server, daemon=True)
    t.start()

    print(f"[Receiver] Listening on {args.host}:{args.port}")
    print("Press Enter to stop...")
    try:
        input()
    finally:
        server.stop_server()
        print("[Receiver] Stopped.")

if __name__ == "__main__":
    main()
