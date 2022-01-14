package old

import (
	"fmt"
	"os"
	"strings"
)

func readFile(filename string) map[string]map[string]string {
	data, err := os.ReadFile(filename)
	if err != nil {
		panic(err)
	}
	lines := strings.Split(strings.TrimSuffix(string(data), "\n"), "\n")
	readIBases(lines)
	return nil
}

func readIBases(lines []string) {
	var section string
	ibases := make(map[string]string)
	for _, line := range lines {
		fmt.Println(line)
		if string(line[0]) == "[" {
			section = string(line[1:(len(line) - 2)])
			continue
		}
		if strings.Contains(line, "ID=") {
			fmt.Println(line)
		}
		ibases[section] = "1"
	}
	// fmt.Println(ibases)
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
	ibases := readFile(filename)
	fmt.Println(ibases)
}

func main1() {
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
