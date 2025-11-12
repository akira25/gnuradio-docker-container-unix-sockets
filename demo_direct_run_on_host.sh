#!/bin/bash

mkdir -p /tmp/gr-unixsocks/

tmux new-session -d  'echo "[ Signal source ]"; ./flowgraphs/iq_sample_sender.py'
tmux split-window -h 'echo "[ Signal demodulation ]"; ./flowgraphs/iq_sample_demod.py'
tmux split-window -h 'echo "[ Replay demoded signal ]"; ./flowgraphs/iq_sample_audio.py'
tmux select-layout even-horizontal
tmux attach
