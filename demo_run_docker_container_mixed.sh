#!/bin/bash

#
# Runs a mixture of a gnuradio-3.10 flowgraph and a gnuradio-3.7 flowgraph
#

podman build -f ./Dockerfile.source -t gr-docker_source:latest
podman build -f ./Dockerfile.demod_gr37 -t gr-docker_demod_gr37:latest

tmux new-session -d  "echo '[ Signal source ]'; podman run --rm --ipc=host --network=host gr-docker_source:latest"
tmux split-window -h "echo '[ Signal demodulation ]'; podman run --rm --ipc=host --network=host gr-docker_demod_gr37:latest"
tmux split-window -h "echo '[ Replay demoded signal ]'; ./flowgraphs/iq_sample_audio.py"
tmux select-layout even-horizontal
tmux attach
