"""Base servicer classes that supply the boilerplate every wrapper
otherwise re-implements: a default `Ping` returning a `Pong` with the
servicer's name.

Concrete wrappers subclass and implement `Init` / `Reset` / `Step` /
`Stop` / `ShouldQuit`. The class-level `_name` attribute customises
the Ping reply so a healthcheck can tell wrappers apart in logs.
"""

import logging

from pisa_api import av_server_pb2_grpc, sim_server_pb2_grpc
from pisa_api.pong_pb2 import Pong

logger = logging.getLogger(__name__)


class BaseSimServer(sim_server_pb2_grpc.SimServerServicer):
    _name: str = "SimServer"

    def Ping(self, request, context):  # noqa: N802  (gRPC method name)
        logger.debug("Ping received from %s", context.peer())
        return Pong(msg=f"{self._name} alive")


class BaseAvServer(av_server_pb2_grpc.AvServerServicer):
    _name: str = "AvServer"

    def Ping(self, request, context):  # noqa: N802
        logger.debug("Ping received from %s", context.peer())
        return Pong(msg=f"{self._name} alive")
