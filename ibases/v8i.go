package main

import (
	"strings"
)

type IBases struct {
	ibases  []IBase
	folders []Folder
}

type IBase struct {
	name        string
	id, connect string
	external    bool
	folder      uint
}

type Folder struct {
	name     string
	id       string
	external bool
	folder   uint
}

func readIBases(data []string) IBases {
	ibases := readData(data)
	printIBases(ibases)
	return *&ibases
}

func (ibd *IBases) appendData(name string, data map[string]string) {
	if _, ok := data["Connect"]; ok {
		ibase := new(IBase)
		ibase.name = name
		ibase.id = data["ID"]
		ibase.external = data["External"] != "0"
		ibd.ibases = append(ibd.ibases, *ibase)
		// fmt.Printf("%v %T\n", data["External"], data["External"])
	} else {
		folder := new(Folder)
		folder.name = name
		folder.id = data["ID"]
		folder.external = data["External"] != "0"
		ibd.folders = append(ibd.folders, *folder)
	}
}

func isIBName(s string) bool {
	return strings.HasPrefix(s, "[")
}

func parseIBName(s string) (name string, ok bool) {
	if strings.HasPrefix(s, "[") {
		name = strings.Trim(s, "[]")
		ok = true
		return
	}
	return
}

func readData(lines []string) IBases {
	var cibname string
	ibases := new(IBases)
	params := make([]string, 0, 15)
	parsed := make(map[string]string)
	for _, line := range lines {
		if ibname, ok := parseIBName(line); ok {
			if cibname != ibname {
				if cibname != "" {
					parsed = parseParams(params)
					ibases.appendData(cibname, parsed)
					params = params[:0]
				}
				cibname = ibname
			}
		} else {
			params = append(params, line)
		}
	}
	ibases.appendData(cibname, parsed)
	return *ibases
}

func parseParams(params []string) map[string]string {
	parsed := make(map[string]string)
	for _, line := range params {
		key, value := parseParam(line)
		parsed[key] = value
	}
	return parsed
}

func parseParam(param string) (key, value string) {
	for i, ch := range param {
		if string(ch) == "=" {
			key = param[:i]
			value = param[i+1:]
			return
		}
	}
	return
}
