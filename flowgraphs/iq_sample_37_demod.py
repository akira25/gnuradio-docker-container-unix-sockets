#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: ZMQ Demo GNURadio 37
# Author: martin
# Description: Flowgraph demonstrating the demodulation of a signal on Gnuradio 3.7
# Generated: Sun Nov 23 15:39:29 2025
##################################################


from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import zeromq
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser


class top_block(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "ZMQ Demo GNURadio 37")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 48e3

        ##################################################
        # Blocks
        ##################################################
        self.zeromq_sub_source_0 = zeromq.sub_source(gr.sizeof_gr_complex, 1, 'ipc://@iq_samples.sock', 100, False, -1)
        self.zeromq_pub_sink_0 = zeromq.pub_sink(gr.sizeof_float, 1, 'ipc://@out_float.sock', 100, False, -1)
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=1,
                decimation=16,
                taps=None,
                fractional_bw=None,
        )
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_complex_to_float_0 = blocks.complex_to_float(1)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_float_0, 0), (self.zeromq_pub_sink_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_complex_to_float_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.zeromq_sub_source_0, 0), (self.rational_resampler_xxx_0, 0))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)


def main(top_block_cls=top_block, options=None):

    tb = top_block_cls()
    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()
