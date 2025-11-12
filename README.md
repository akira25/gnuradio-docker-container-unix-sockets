# Distribute Data from GNU-Radio Flowgraphs via Unix Domain sockets

Based on containerised setup mentioned in [akira25/gnuradio-docker-container](https://github.com/akira25/gnuradio-docker-container),
though it does not need to use containerised flowgraphs. The idea, techniques and
conventions established here, work also fine with flowgraphs that run on your
machine directly.

## Idea: Unix sockets for ZMQ-based data distribution

We published the idea of speaking ZMQ via TCP between docker containers already
earlier (see link above). This approach works great when streaming over a network,
but suffers sometimes from buffer underflows. Thus the advanced idea is, to use
unix domain sockets as the underlying socket type. Intended for Inter-Process-
Communication, this socket type avoids most of the overhead that is imposed by
transporting data over an IP-Network.

This approach narrows the deployment options down to run the flowgraphs on the
same single host system, but improves otherwise latency and throughput by orders
of magnitude.

## ZMQ-Scheme to use

The ZMQ-Sockets in the flowgraphs shall use the PUB-SUB scheme for data/signal
distribution. Whereas the publisher emits the data and the subscriber consumes
that data. The topics feature might be used, but we propose to not use it, for
simplicity.

## Creating Sockets and how to call Containers

We decided on abstract namespace unix sockets. They circumvent a lot of SELinux-
related stuff, that might complicate things on modern Linux distributions. As
a consequence, we need to start the containers using the same namespace and
network as the host, though:

```sh
podman run --rm --ipc=host --network=host gr-docker_source:latest
```

Please let me point out, that this will let the flowgraph in the container
communicate with all other IPC-Sockets in the abstract namespace. Effectively,
this is the same, as the flowgraph would run on your system directly, though.
So it might be no security issue to you.

For the sockets, some conventional naming might be good, to simplify interoperation
of different flowgraphs. For a start, we propose these sockets:

TODO: adjust Flotgraph for abstract name sockets.
```txt
                                     --------------------
-------------------                  |                  |                 -------------------
| SDR - Flowgraph | - - writes - - > | @iq_samples.sock | - - reads - - > | DSP - Flowgraph | - (1)
-------------------                  |                  |                 -------------------
                                     --------------------

                   ------------------
                   |                |
(1) - writes - - > |  @out_nn.sock  |
                   |                |
                   ------------------
```

Whereas `out_nn.sock` translates into an out socket of a certain datatype:

- `@iq_samples.sock`
- `@out_complex.sock`
- `@out_float.sock`
- `@out_int.sock`
- `@out_short.sock`
- `@out_byte.sock`

A DSP-Flowgraph might emit on every socket!

## Building Flowgraphs for this Approach

GNU-Radio flowgraphs that use this framework, should be built in that way that they:

- Are `No GUI`-Flowgraphs (Setting in Root-Block)
- `Run until completion` (also a setting there. Not setting this will likely result in your flowgraph exited immediately)
- Run in a minimal gnuradio runtime within a docker container. e.g. [github.com/akira25/gnuradio-docker-container](https://github.com/akira25/gnuradio-docker-container)

You can find example flowgraphs at `/flowgraphs`. If you have tmux installed,
you can run the examples easily via the demo scripts provided in this repos root.
