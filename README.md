# send-frames-over-tcp

To run `opencv-python` is required. `pip3 install opencv-python` 
or `pip3 install -r requirements.txt`.

In one terminal window, run `python3 vidd.py` to start up the 
frame streaming server. In another terminal run `python3 client_player.py`
to start up a client that will display each frame as it receives it. 

Metrics for sending and receiving frames will be printed out from both
the server and client. 

To use a different video, update `VIDEO_FILE = "surf.mp4"` in vidd.py. 
`water.mp4` is a larger 4K sample video.

Credit for most of the code goes to https://stackoverflow.com/questions/49084143/opencv-live-stream-video-over-socket-in-python-3
