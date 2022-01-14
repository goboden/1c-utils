package main

type IBases struct {
	ibases  []IBase
	folders []Folder
}

type IBase struct {
	name        string
	id, connect string
	folder      uint
}

type Folder struct {
	name   string
	id     string
	folder uint
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
		ibd.ibases = append(ibd.ibases, *ibase)
	} else {
		folder := new(Folder)
		folder.name = name
		folder.id = data["ID"]
		ibd.folders = append(ibd.folders, *folder)
	}
}

func readData(lines []string) IBases {
	var cibname string
	ibases := new(IBases)
	params := make([]string, 0, 15)
	parsed := make(map[string]string)
	for _, line := range lines {
		if string(line[0]) == "[" {
			ibname := line[1 : len(line)-2]
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
