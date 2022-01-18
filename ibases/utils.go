package main

import (
	"fmt"
	"strings"
)

func printMap(m map[string]string) {
	for k, v := range m {
		println(k + " = " + v)
	}
}

func printIBasesList(ibd IBases) {
	fs := "%-1s | %-5t | %-3d | %-75s | %-20s\n"
	for i, ib := range ibd.ibases {
		fmt.Printf(fs, "B", ib.external, i, ib.name, ib.path)
	}
	for i, f := range ibd.folders {
		fmt.Printf(fs, "F", f.external, i, f.name, f.path)
	}
}

func printFolders(ibd IBases, name string, level int) {
	fs := "%s [%s]\n"
	for _, f := range ibd.folders {
		if f.path == name {
			fmt.Printf(fs, strings.Repeat(" ", level*3), f.name)
			nlevel := level + 1
			printIBases(ibd, name, nlevel)
			printFolders(ibd, "/"+f.name, nlevel)
		}
	}
}

func printIBases(ibd IBases, name string, level int) {
	fs := "%s * %s\n"
	for _, ib := range ibd.ibases {
		if ib.path == name {
			fmt.Printf(fs, strings.Repeat(" ", level*3), ib.name)
		}
	}
}
