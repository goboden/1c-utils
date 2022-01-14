package main

func printMap(m map[string]string) {
	for k, v := range m {
		println(k + " = " + v)
	}
}

func printIBases(ibd IBases) {
	for i, ib := range ibd.ibases {
		println("B", i, ib.name)
	}
	for i, f := range ibd.folders {
		println("F ", i, f.name)
	}
}
