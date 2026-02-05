proto:
    uv run -m grpc_tools.protoc -I=./proto --python_out=./src/carla_api --grpc_python_out=./src/carla_api ./proto/*.proto
    sed -i 's/^import \(.\+\) as/from . import \1 as/' src/carla_api/*.py

clean:
    rm -rf src/carla_pb2*.py
