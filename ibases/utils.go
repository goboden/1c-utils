package main

import "fmt"

func printMap(m map[string]string) {
	for k, v := range m {
		println(k + " = " + v)
	}
}

func printIBases(ibd IBases) {
	fs := "%-1s %-1t %-3d %-20s\n"
	for i, ib := range ibd.ibases {
		fmt.Printf(fs, "B", ib.external, i, ib.name)
	}
	for i, f := range ibd.folders {
		fmt.Printf(fs, "F", f.external, i, f.name)
	}
}
