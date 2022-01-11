package main

import (
	"fmt"
	"os"
)

func readFile(filename string) {
	data, err := os.ReadFile(filename)
	if err != nil {
		panic(err)
	}
	fmt.Println(string(data))
}

func openFile(filename string) {
	file, err := os.Open(filename)
	if err != nil {
		fmt.Println(err)
		return
	}
	f, err := file.Stat()
	fmt.Println("Read Ok. File size:", f.Size())
	file.Close()
}

func readCommand() string {
	args := os.Args
	if len(args) > 1 {
		return args[1]
	}
	return ""
}

func listIBases() {
	fmt.Println("IBases list:")
	filename := "..\\ibases.v8i"
	readFile(filename)
}

func main() {
	// readFile("..\\ibases.v8i")
	// openFile("..\\ibases.v8i")
	command := readCommand()
	switch command {
	case "list":
		listIBases()
	default:
		fmt.Println("Use \"list\" command.")
	}

}
