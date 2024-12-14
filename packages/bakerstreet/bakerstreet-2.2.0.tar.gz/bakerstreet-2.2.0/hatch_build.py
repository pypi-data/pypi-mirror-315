import os
import subprocess
from grpc_tools import protoc
from hatchling.builders.hooks.plugin.interface import BuildHookInterface

class CustomBuildHook(BuildHookInterface):
    def initialize(self, version, build_data):
        compile_proto()

def compile_proto():
    bakerstreet = "bakerstreet"
    proto_file = f"{bakerstreet}/{bakerstreet}.proto"
    
    # Remove existing generated files
    go_files = [f for f in os.listdir(bakerstreet) if f.endswith('.go') and f.startswith('bakerstreet')]
    py_files = [f for f in os.listdir(bakerstreet) if f.endswith('.py') and f.startswith('bakerstreet')]
    
    for file in go_files + py_files:
        os.remove(os.path.join(bakerstreet, file))
    
    # Compile Go protobuf and gRPC files
    go_compile_cmd = [
        "protoc", 
        "-I", ".", 
        "--go_out=.", 
        "--go_opt=paths=source_relative",
        "--go-grpc_out=.", 
        "--go-grpc_opt=paths=source_relative",
        proto_file
    ]
    
    # Execute commands
    subprocess.run(go_compile_cmd, check=True)

    # Compile Python protobuf and gRPC files
    protoc.main(
        ("-I  .", "--python_out=.", "--grpc_python_out=.", "{:s}".format(proto_file))
    )