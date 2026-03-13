proto:
    uv run -m grpc_tools.protoc -I=./proto --python_out=./src/pisa_api --grpc_python_out=./src/pisa_api ./proto/*.proto
    sed -i 's/^import \(.\+\) as/from . import \1 as/' src/pisa_api/*.py

clean:
    rm -rf src/pisa_api/*pb2*.py
