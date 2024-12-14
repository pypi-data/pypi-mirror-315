# bakerstreet
Baker Street - The place where characters frequently meet


### Development setup

```
uv sync
```

Install the protocol compiler plugins for Go:
```
go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
```

### Build

Includes generation of protobuf files

```
uv build
```

### Publish package to PyPI

```
uv publish
```
