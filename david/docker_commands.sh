# launch docker daemon (virtual machine) manually


# interactive mode via bash
docker run -p 8810:8888 -p 6006:6006 -v /Users:/host/Users -it gcr.io/tensorflow/tensorflow bash

# run image with jupyter export on port 8810
docker run -p 8810:8888 -p 6006:6006 gcr.io/tensorflow/tensorflow /run_jupyter.sh
