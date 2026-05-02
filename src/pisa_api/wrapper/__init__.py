"""Shared scaffolding for PISA wrapper gRPC servers.

A wrapper that wires a simulator (esmini, CARLA, …) or AV stack
(carla-agent, autoware, …) into the SIM/AV gRPC contract used to need
~30 lines of identical boilerplate per repo: a `serve()` function that
binds a port, a default `Ping` handler, and a `logging.basicConfig`
call. This subpackage centralises all of that.

Typical wrapper:

    from pisa_api.wrapper import BaseSimServer, serve_sim, setup_logging

    setup_logging()

    class EsminiService(BaseSimServer):
        _name = "Esmini"
        def Init(self, request, context): ...
        # Reset, Step, Stop, ShouldQuit; Ping inherited.

    if __name__ == "__main__":
        serve_sim(EsminiService(), name="Esmini")
"""

from .base import BaseAvServer, BaseSimServer
from .logging import setup_logging
from .serve import serve_av, serve_sim

__all__ = [
    "BaseAvServer",
    "BaseSimServer",
    "serve_av",
    "serve_sim",
    "setup_logging",
]
