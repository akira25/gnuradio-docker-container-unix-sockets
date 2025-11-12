#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: ZMQ Pipeline test receive
# Author: martin
# GNU Radio version: 3.10.11.0

from gnuradio import audio
from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import zeromq
import threading




class iq_sample_audio(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "ZMQ Pipeline test receive", catch_exceptions=True)
        self.flowgraph_started = threading.Event()

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 48e3

        ##################################################
        # Blocks
        ##################################################

        self.zeromq_sub_source_1 = zeromq.sub_source(gr.sizeof_float, 1, 'ipc://@out_float.sock', 100, False, (-1), '', False)
        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_float*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.audio_sink_0 = audio.sink(int(samp_rate), '', True)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_throttle2_0, 0), (self.audio_sink_0, 0))
        self.connect((self.zeromq_sub_source_1, 0), (self.blocks_throttle2_0, 0))


    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle2_0.set_sample_rate(self.samp_rate)




def main(top_block_cls=iq_sample_audio, options=None):
    tb = top_block_cls()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()
    tb.flowgraph_started.set()

    tb.wait()


if __name__ == '__main__':
    main()
