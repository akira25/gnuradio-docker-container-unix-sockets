#!/bin/bash

podman build -f ./Dockerfile.source -t gr-docker_source:latest
podman build -f ./Dockerfile.demod -t gr-docker_demod:latest

tmux new-session -d  "echo '[ Signal source ]'; podman run --rm --ipc=host --network=host gr-docker_source:latest"
tmux split-window -h "echo '[ Signal demodulation ]'; podman run --rm --ipc=host --network=host gr-docker_demod:latest"
tmux split-window -h "echo '[ Replay demoded signal ]'; ./flowgraphs/iq_sample_audio.py"
tmux select-layout even-horizontal
tmux attach
