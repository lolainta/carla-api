"""gRPC serve loop. Reads PORT from env (default 50051), binds, blocks
on `wait_for_termination`, and shuts down cleanly on KeyboardInterrupt.

Two entry points so callers don't need to import the right
`add_*Servicer_to_server` themselves:

- `serve_sim(servicer)` → wires a SimServer
- `serve_av(servicer)`  → wires an AvServer
"""

# `int | str` syntax in annotations is only valid at runtime on
# Python 3.10+; pisa-api supports 3.8+. Defer evaluation so the
# union syntax is treated as a string and never executed.
from __future__ import annotations

import logging
import os
from concurrent import futures
from typing import Callable

import grpc

from pisa_api import av_server_pb2_grpc, sim_server_pb2_grpc

logger = logging.getLogger(__name__)

DEFAULT_PORT = "50051"
DEFAULT_MAX_WORKERS = 4


def _serve(
    add_to_server: Callable[[object, grpc.Server], None],
    servicer: object,
    *,
    port: int | str | None = None,
    max_workers: int = DEFAULT_MAX_WORKERS,
    name: str = "gRPC",
) -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
    add_to_server(servicer, server)
    port = port if port is not None else os.environ.get("PORT", DEFAULT_PORT)
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    logger.info("%s server started on port %s; waiting for clients", name, port)
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        logger.info("Shutting down %s server", name)
        server.stop(0)


def serve_sim(
    servicer: object,
    *,
    port: int | str | None = None,
    max_workers: int = DEFAULT_MAX_WORKERS,
    name: str = "SimServer",
) -> None:
    _serve(
        sim_server_pb2_grpc.add_SimServerServicer_to_server,
        servicer,
        port=port,
        max_workers=max_workers,
        name=name,
    )


def serve_av(
    servicer: object,
    *,
    port: int | str | None = None,
    max_workers: int = DEFAULT_MAX_WORKERS,
    name: str = "AvServer",
) -> None:
    _serve(
        av_server_pb2_grpc.add_AvServerServicer_to_server,
        servicer,
        port=port,
        max_workers=max_workers,
        name=name,
    )
