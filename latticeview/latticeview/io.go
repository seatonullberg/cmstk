package latticeview

import (
	"io/ioutil"

	"github.com/golang/protobuf/proto"
)

// ReadProtoFile initializes a ProtoLattice from a protobuf file.
func ReadProtoFile(path string) (*ProtoLattice, error) {
	protoLattice := &ProtoLattice{}

	bytes, err := ioutil.ReadFile(path)
	if err != nil {
		return protoLattice, err
	}
	if err = proto.Unmarshal(bytes, protoLattice); err != nil {
		return protoLattice, err
	}
	return protoLattice, nil
}

// WriteProtoFile writes a ProtoLattice to a protobuf file.
func WriteProtoFile(path string, lattice *ProtoLattice) error {
	bytes, err := proto.Marshal(lattice)
	if err != nil {
		return err
	}
	return ioutil.WriteFile(path, bytes, 0644)
}
