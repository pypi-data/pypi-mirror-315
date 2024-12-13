# go get -u github.com/golang/protobuf/protoc-gen-go
# go get github.com/nstogner/protoc-gen-grpc-go-service
BAKERSTREET="bakerstreet"
PROTOFILE=$BAKERSTREET/$BAKERSTREET.proto
rm $BAKERSTREET/$BAKERSTREET*{.go,.py}
protoc -I . \
    --go_out=. --go_opt=paths=source_relative \
    --go-grpc_out=. --go-grpc_opt=paths=source_relative \
	$PROTOFILE

python -m grpc_tools.protoc \
	-I . \
	--python_out=. \
	--grpc_python_out=. \
	$PROTOFILE
