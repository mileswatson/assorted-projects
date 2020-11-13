package main

import (
	"bytes"
	"crypto/rand"
	"crypto/sha256"
	"encoding/binary"
	"encoding/hex"
	"fmt"
	"math/big"
	"strconv"
)

////////////////////////////////////////////////////////////////

type Block struct {
	Stage         uint64
	PrevBlockHash []byte
	Data          []byte
	Nonce         []byte
	Hash          []byte
}

func NewBlock(stage uint64, prevBlockHash []byte, data string) *Block {
	block := &Block{
		Stage:         stage,
		PrevBlockHash: prevBlockHash,
		Data:          []byte(data),
		Nonce:         []byte{},
		Hash:          []byte{},
	}
	block.SetHash()
	return block
}

func (b *Block) SetHash() {
	stage := make([]byte, 8)
	binary.LittleEndian.PutUint64(stage, b.Stage)
	headers := bytes.Join([][]byte{
		stage,
		b.PrevBlockHash,
		b.Data,
		b.Nonce,
	}, []byte{})
	hash := sha256.Sum256(headers)
	b.Hash = hash[:]
}

func (b *Block) Prove(bc *Blockchain) {
	b.Nonce = make([]byte, 8)
	hashNum := big.NewInt(0)
	for {
		rand.Read(b.Nonce)
		b.SetHash()
		hashNum.SetBytes(b.Hash)
		if bc.Target.Cmp(hashNum) > 0 {
			return
		}
	}
}

func (b *Block) String() string {
	returnString := "\t" + hex.EncodeToString(b.Hash) + ":\n"
	returnString += "\t\tPreviousID: " + hex.EncodeToString(b.PrevBlockHash) + "\n"
	returnString += "\t\tData: " + string(b.Data) + "\n"
	returnString += "\t\tNonce: " + string(b.Nonce) + "\n"
	return returnString
}

////////////////////////////////////////////////////////////////

type Stage struct {
	Blocks []*Block
}

func (s *Stage) containsHash(hash []byte) bool {
	var same bool
	for _, element := range s.Blocks {
		same = true
		if !bytes.Equal(hash, element.Hash) {
			same = false
		}
		if same {
			return true
		}
	}
	return false
}

///////////////////////////////////////////////////////////////

type Blockchain struct {
	Stages []*Stage
	Target *big.Int
}

func NewBlockchain(targetBits int) *Blockchain {
	target := big.NewInt(1)
	target.Lsh(target, uint(256-targetBits))
	return &Blockchain{[]*Stage{{[]*Block{NewBlock(0, []byte{}, "")}}}, target}
}

func (bc *Blockchain) String() string {
	returnString := ""
	for index, stage := range bc.Stages {
		returnString += "Stage " + strconv.Itoa(index)
		for _, block := range stage.Blocks {
			returnString += "\n" + block.String()
		}
	}
	return returnString
}

func (bc *Blockchain) AddBlock(b *Block) bool {
	b.SetHash()
	hashNum := big.NewInt(0)
	hashNum.SetBytes(b.Hash)
	if bc.Target.Cmp(hashNum) > 0 && b.Stage > 0 && b.Stage <= uint64(len(bc.Stages)) {
		if b.Stage == uint64(len(bc.Stages)) {
			bc.Stages = append(bc.Stages, &Stage{[]*Block{}})
		}
		if bc.Stages[b.Stage-1].containsHash(b.PrevBlockHash) {
			bc.Stages[b.Stage].Blocks = append(bc.Stages[b.Stage].Blocks, b)
			return true
		}
	}
	return false
}

///////////////////////////////////////////////////////////////

func main() {
	x := NewBlockchain(16) // creates new blockchain with genesis block at stage 0
	b := NewBlock(1, x.Stages[0].Blocks[0].Hash, "This is the first block on the blockchain!!!") // 

    b.Prove(x)
    added := x.AddBlock(b)
    fmt.Println(added)

    b = NewBlock(2,x.Stages[1].Blocks[0].Hash, "This is the second block.")
    b.Prove(x)
    added = x.AddBlock(b)
    fmt.Println(added)

    fmt.Print(x)
}