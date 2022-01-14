package main

import (
	"os"
)

func main() {
	fileName := "../ibases.v8i"
	fileData, err := readFile(fileName)
	if err != nil {
		println(err.Error())
		return
	}
	readIBases(fileData)
}

func splitStrings(d []byte) []string {
	ls := make([]string, 0, uint(len(d)/20))
	ln := make([]byte, 0, 50)
	for _, ch := range d {
		if string(ch) == "\n" {
			ls = append(ls, string(ln))
			ln = ln[:0]
			continue
		}
		ln = append(ln, ch)
	}
	return ls
}

func readFile(name string) (str []string, err error) {
	data, err := os.ReadFile(name)
	if err != nil {
		return
	}
	str = splitStrings(data)
	return str, nil
}
