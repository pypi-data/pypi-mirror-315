#!/usr/bin/python3
# @Мартин.
import cmd
import time
import socket
import json
import base64
import os
import hashlib
from collections import Counter, deque
import sys
sys.path.append('.')
from pack.S_Clustr_AES import S_Clustr_AES_CBC

configs = json.load(open('Version.conf'))[sys.argv[0].split('.')[0]]

title = f'''
************************************************************************************
<Disclaimer>:This tool is onl y for learning and experiment. Do not use it
for illegal purposes, or you will bear corresponding legal responsibilities
************************************************************************************
{configs['describe']}
'''
logo = f'''
███████╗       ██████╗██╗     ██╗   ██╗███████╗████████╗██████╗
██╔════╝      ██╔════╝██║     ██║   ██║██╔════╝╚══██╔══╝██╔══██╗
███████╗█████╗██║     ██║     ██║   ██║███████╗   ██║   ██████╔╝
╚════██║╚════╝██║     ██║     ██║   ██║╚════██║   ██║   ██╔══██╗
███████║      ╚██████╗███████╗╚██████╔╝███████║   ██║   ██║  ██║
╚══════╝       ╚═════╝╚══════╝ ╚═════╝ ╚══════╝   ╚═╝   ╚═╝  ╚═╝
                Github==>https://github.com/MartinxMax
                @Мартин. S-Clustr(Shadow Cluster) Client {configs['version']}'''


class Load_Handler:
    def __init__(self,payload):
        self.__aes=S_Clustr_AES_CBC()
        self.PAYLOAD = payload
        self.map = {'RUN': 'RUN', 'STOP': 'STOP', 'TIME': 'TIME','FOR':'FOR'}
        self.code = {}
        self.action=False

    def run(self, code,rkey,rhost,rport,action=False):
        self.code = self.__check_json(code)
        print(self.code)
        if not self.code:
            return False
        self.action = action
        return self.__EIP_MAIN(rkey,rhost,rport)

    def __call_function(self, function_name, args,rkey,rhost,rport):
        if function_name not in self.code:
            return False
        if self.action:print("[--+] Enter the execution subfunction program")
        func_info = self.code[function_name]
        if len(args) != len(func_info['args']):
            return False
        if any(isinstance(arg, str) and arg.isdigit() for arg in func_info['args']):
            return False
        var = dict(zip(func_info['args'], args))
        queue = deque(func_info['eip'])
        while queue:
            eip = queue.popleft()
            k, v = eip.split(':')
            if 'FOR' not in k :
                v = v.split(',')
            if 'CALL' in k:
                called_function = k.replace('CALL-', '')
                if called_function in self.code:
                    if called_function == 'MAIN':
                        return False
                    if not self.__call_function(called_function, v,rkey,rhost,rport):
                        return False
            elif k in self.map:
                if self.action:
                    stat = False
                    id_c = None   
                    task_c = None   
                    if '-' in v[0]:
                        id_c=v[0].split('-')[0]
                        task_c=v[0].split('-')[1]
                    if id_c in var and k != 'FOR':
                        id_c = int(var.get(id_c))
                    if task_c in var and k != 'FOR':
                        task_c = int(var.get(task_c))
                    if self.map[k] == 'RUN':
                            currentTime = int(time.time())
                            signature = self.__aes.aes_cbc_encode(rkey, str(currentTime))
                            payload = self.PAYLOAD._build_payload(currentTime,int(id_c),1,int(task_c),signature)
                            self.PAYLOAD._send_hex_string(payload,int(id_c), 1,rhost,rport,rkey)
                            stat=True
                    elif self.map[k] == "STOP":
                            currentTime = int(time.time())
                            signature = self.__aes.aes_cbc_encode(rkey, str(currentTime))
                            payload = self.PAYLOAD._build_payload(currentTime,int(id_c),2,int(task_c),signature)
                            self.PAYLOAD._send_hex_string(payload,int(id_c), 2,rhost,rport,rkey)
                            stat=True
                    elif self.map[k] == "TIME":
                        time.sleep(int(v[0])/1000)
                    elif self.map[k] == "FOR":
                        if len(v.split(',')) != 5:
                            return False
                        start,end,step,asname,b64_payload = v.split(',')
                        ebeip = base64.b64decode(b64_payload.encode('utf-8')).decode('utf-8')
                        for next_num in range(int(start),int(end),int(step)):
                            result = [item for item in ebeip.split(';') if item]
                            for eip_c in result:
                                k_, v_ = eip_c.split(':')
                                if k_ in self.map:
                                    if self.action:
                                        stat_ = False
                                        if k_ == 'RUN' or k_ == 'STOP':
                                            if  '-' in v_:
 
                                                if v_.split('-')[0] == asname:
                                                    id_ = int(next_num)
                                                elif v_.split('-')[0] in var:
                                                    id_ = int(var[v_.split('-')[0]])
                                                elif v_.split('-')[0].isdigit():
                                                    id_ =  int(v_.split('-')[0])
                                                
                                                if v_.split('-')[1]  == asname:
                                                    task_ = int(next_num)
                                                elif v_.split('-')[1].isdigit():
                                                    task_ = int(v_.split('-')[1])
                                                elif v_.split('-')[1] in var:
                                                    task_ = int(v_.split('-')[1])
                                                
                                        if k_ == 'TIME':
                                            if v_ == asname:
                                                time.sleep(int(next_num)/1000)
                                            elif v_.isdigit():
                                                time.sleep(int(v_)/1000)
                                            
                                        elif k_ == 'RUN':
                                                currentTime = int(time.time())
                                                signature = self.__aes.aes_cbc_encode(rkey, str(currentTime))
                                                payload = self.PAYLOAD._build_payload(currentTime,id_,1,task_,signature)
                                                self.PAYLOAD._send_hex_string(payload,id_, 1,rhost,rport,rkey)
                                                stat_=True
                                        elif k_ == "STOP":
                                                currentTime = int(time.time())
                                                signature = self.__aes.aes_cbc_encode(rkey, str(currentTime))
                                                payload = self.PAYLOAD._build_payload(currentTime,id_,2,task_,signature)
                                                self.PAYLOAD._send_hex_string(payload,id_, 2,rhost,rport,rkey)
                                                stat_=True

                                        if stat_:
                                            print(f"[{'+' if stat_ else '-'}] [{self.map[k_]}] ID: {id_} ")
                    if stat:
                        print(f"[{'+' if stat else '-'}] [{self.map[k]}] ID: {id} ")


        return True

    def __check_json(self, data):
        try:
            result = json.loads(data)
            if isinstance(result, dict):
                return result
            else:
                return False
        except json.JSONDecodeError:
            return False

    def __EIP_MAIN(self,rkey,rhost,rport):
        if 'MAIN' not in self.code:
            return False
  
        if not (rkey and rhost and rport):
            print("[!] The target parameter is incomplete...")
            return False
        queue = deque(self.code['MAIN']['eip'])
        while queue:
            eip = queue.popleft()
            if len(eip.split(':')) != 2:
                return False
            k, v = eip.split(':')
            v = v.split(',')
            if self.action:print(f"[+] Execute script")
            if 'CALL' in k:
                function_name = k.replace('CALL-', '')
                if function_name in self.code:
                    if function_name == 'MAIN':
                        return False
                    if not self.__call_function(function_name, v,rkey,rhost,rport):
                        return False
            elif k in self.map:  
                if self.action:
                    stat_ = False
                    if k == 'RUN' or k == 'STOP':
                        if  '-' in v[0]:
                            id_ = int(v[0].split('-')[0])
                            task_ =  int(v[0].split('-')[1])
                    if k == 'TIME':
                        if k.isdigit():
                            time.sleep(int(v[0])/1000)
                    
                    elif k == 'RUN':
                            currentTime = int(time.time())
                            signature = self.__aes.aes_cbc_encode(rkey, str(currentTime))
                            payload = self.PAYLOAD._build_payload(currentTime,id_,1,task_,signature)
                            self.PAYLOAD._send_hex_string(payload,id_, 1,rhost,rport,rkey)
                            stat_=True
                    elif k == "STOP":
                            currentTime = int(time.time())
                            signature = self.__aes.aes_cbc_encode(rkey, str(currentTime))
                            payload = self.PAYLOAD._build_payload(currentTime,id_,2,task_,signature)
                            self.PAYLOAD._send_hex_string(payload,id_, 2,rhost,rport,rkey)
                            stat_=True

                    if stat_:
                        print(f"[{'+' if stat_ else '-'}] [{self.map[k]}] ID: {id_} TASK:{task_} ")
        return True


class GAME:
    def __init__(self,payload):
        self.__aes=S_Clustr_AES_CBC()
        self.PAYLOAD = payload
        self.action_mapping =  [
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0]
        ]
    def get_differences(self,new_mapping):
        all_differences = {}
        for row_index in range(len(self.action_mapping)):
            differences = [i for i in range(len(self.action_mapping[row_index])) if self.action_mapping[row_index][i] != new_mapping[row_index][i]]
            if differences:
                ids = [(row_index * 5 + i + 1) for i in differences]   
                values = [new_mapping[row_index][i] for i in differences]   
                all_differences[row_index] = {
                    'index': differences,
                    'ids': ids,
                    'var': values
                }
                for i in differences:
                    self.action_mapping[row_index][i] = new_mapping[row_index][i]
        return  all_differences
    
    def run(self, ip, port, rkey, rhost, rport):
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            SERVER_ADDRESS = (ip, int(port))
       
            try:
                client_socket.connect(SERVER_ADDRESS)
                print("[*] Attempting to connect to the game server...")
                client_socket.setblocking(0) 
                while True:
                    try:
                        data = client_socket.recv(4096).decode('utf-8')
                        if not data:
                            break
                        try:
                            matrix = json.loads(data)
                            conf = self.get_differences(matrix)
                            print(conf)
                            for line_index, details in conf.items():
                                ids = details['ids']
                                for id_arr_index, id_ in enumerate(ids):
                                    currentTime = int(time.time())
                                    signature = self.__aes.aes_cbc_encode(rkey, str(currentTime))
                                    payload = self.PAYLOAD._build_payload(currentTime, line_index+1, 1 if details['var'][id_arr_index] == 1 else 2,(id_ - 1) % 5 + 1,signature)
                                    print(payload)
                                    self.PAYLOAD._send_hex_string(payload, currentTime, 1 if details['var'][id_arr_index] == 1 else 2, rhost, rport, rkey)
                        except json.JSONDecodeError:
                            pass
                    except BlockingIOError:
                        continue
            except Exception as e:
                print(f"[!] Unable to connect to the game server. {e}")
            finally:
                client_socket.close()
 
class S_Clustr(cmd.Cmd):
    intro = 'Welcome to S-Clustr console. Type [options][help/?] to list commands.\n'
    prompt = f'S-Clustr({configs["version"]})> '


    def __init__(self):
        super().__init__()
        self.__aes=S_Clustr_AES_CBC()
        self.PAYLOAD = PAYLOAD()
 
        self.options = {
            "rhost": {"value":"","description":"The target host"},
            "rport": {"value":"9999","description":"The target port (TCP)"},
            "id": {"value":"","description":"Device ID [0-n/0 represents specifying all]"},
            "pwr": {"value":"","description":"Device behavior (run[1]/stop[2]/Query device status[3])"},
            "task": {"value":"0","description":"Device Task Execution Number (Default:0) (0-255)"},
            "key": {"value":"","description":"Server Key"}
        }


    def do_game(self, line):
        parts = line.split(maxsplit=1)
        if len(parts) != 2:
            print("Usage: game <ip> <port>")
            return
        ip = parts[0]
        port = parts[1]
 
        self.PAYLOAD.game_run(ip,port,self.options)

    def do_load(self, line):
        parts = line.split(maxsplit=1)
        if len(parts) != 2:
            print("Usage: load <key> <path>")
            return

        key = parts[0]
        path = parts[1]
        if not os.path.isfile(path):
            print(f"[!] Error: The file '{path}' does not exist.")
            return
        self.PAYLOAD.auto_attack(key,path,self.options)
 
    
    def do_set(self, arg):
        """Set an option value. Usage: set <option> <value>"""
        try:
            option, value = arg.split()
        except ValueError:
            print("[-] Invalid syntax. Usage: set <option> <value>")
            return
        else:
            if option in self.options:
                if option == 'task'  and (int(value) > 255 or int(value) < 0):
                    print("[!] The maximum selection range for the task is 0-255")
                    return False
                self.options[option]['value'] = value
                print(f'[*] {option} => {value}')
            else:
                print(f'[-] Unknown variable: {option}')


    def do_run(self,arg):
        print("[*] Connecting to the server...")
        self.PAYLOAD.run(self.options)


    def do_options(self, arg):
        """List all available options and their current values."""
        table =  "| Name           | Current Setting | Required | Description       \n"
        table += "|:--------------:|:---------------:|:--------:|:-----------------\n"
        for key in self.options:
            name = f"{key:<14}"
            setting = f"{self.options[key]['value'] if self.options[key]['value'] else ' ':<15}"
            required = f"{'no' if self.options[key]['value'] else 'yes':<8}"
            description = f"{self.options[key]['description']:<20}"
            table += f"| {name} | {setting} | {required} | {description}\n"
        table += "|:--------------:|:---------------:|:--------:|:-----------------\n"
        print(table)
 
    
    def do_exit(self, arg):
        """Exit the program. Usage: exit"""
        return True


class PAYLOAD():


    def __init__(self):
        self.__aes=S_Clustr_AES_CBC()
        self.__BEHAVIORS = {1: 'RUN', 2: 'STOP', 3: 'Query State'}
        self.__load_handler =  Load_Handler(self)
        self.__game =  GAME(self)
    def run(self,info):
        if self.__check_params_complete(info):
            id = int(info['id']['value'])
            pwr = int(info['pwr']['value'])
            key = info['key']['value']
            rhost = info['rhost']['value']
            rport = int(info['rport']['value'])
            task = int(info['task']['value'])
      
            if pwr >0 and pwr < 4:
                if self._check_params(id,pwr,key,rhost,rport):
                    currentTime = int(time.time())
                    signature = self.__aes.aes_cbc_encode(key, str(currentTime))
                    payload = self._build_payload(currentTime,id,pwr,task,signature)
                    self._send_hex_string(payload,id, pwr,rhost,rport,key)
            else:
                print(f"[-] The status parameter is not within the valid range![1-3]")

    def auto_attack(self,key,path,info):
        print("[***** AUTO ATTACK *****]")
        try:
            with open(path, 'r') as f:
                payload = f.read()
            payload = self.__aes.aes_cbc_decode(key, payload)
            rkey = info['key']['value']
            rhost = info['rhost']['value']
            rport = int(info['rport']['value'])
            print("[*] Start checking the packet")
            if self.__load_handler.run(payload,rkey,rhost,rport,False):
                print("[+] Packet complete availability")
                self.__load_handler.run(payload,rkey,rhost,rport,True)
                
            else:
                print("[!] The packet is damaged and unavailable")
        except Exception as e:
            print(f"An error occurred: {e}")

    def game_run(self,ip,port,info):
        try:
            rkey = info['key']['value']
            rhost = info['rhost']['value']
            rport = int(info['rport']['value'])
            print("[*] Init Cre")
            self.__game.run(ip,port,rkey,rhost,rport)
                
 
        except Exception as e:
            print(f"An error occurred: {e}")

    def __check_params_complete(self,info):
        for key in ['id', 'pwr', 'key', 'rhost', 'rport','task']:
            if key not in info or not info[key].get('value'):
                print(f"[-] Parameter '{key}' is missing or incomplete!")
                return False
        return True

    def _check_params(self,id, pwr, key, rhost, rport):
        if not isinstance(id, int):
            print("[-] The id parameter must be an integer!")
            return False
        if not isinstance(pwr, int) or pwr < 1 or pwr > 3:
            print("[-] The pwr parameter must be an integer between 1 and 3!")
            return False
        if not isinstance(key, str):
            print("[-] The key parameter must be a string!")
            return False
        if not isinstance(rhost, str):
            print("[-] The rhost parameter must be a string!")
            return False
        if not isinstance(rport, int):
            print("[-] The rport parameter must be an integer!")
            return False
        return True

    def _send_hex_string(self,hex_string,id,pwr,rhost,rport,key):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if pwr == 3:
            client_socket.settimeout(3)
        else:
            client_socket.settimeout(0.1)
        client_socket.connect((rhost, int(rport)))
        print(f"[*] Attempting to authenticate to the server [{rhost}:{rport}]")
        client_socket.sendall(hex_string.encode('utf-8'))
        while True:
            try:
                result = self.__aes.aes_cbc_decode(key,client_socket.recv(2048).decode('utf-8'))
                if not result:
                    break
                if pwr == 3 :
                    result = json.loads(result)
                    self.__display(result)
                else:
                    print(f"[*] Control Device ID:[{id}] Action:[{self.__BEHAVIORS[pwr]}]")
                    print("[+] "+result)
            except socket.timeout:
                break
            except Exception as e:
                break
        client_socket.close()


    def _build_payload(self,time,id,state,task,signature):
        return f"{time:08x} {id:04x} {state:02x} {task:02x} {signature}"


    def __display(self, jsond):
        if jsond:
            table = "|   Device ID   |  Device Type | Device Network |\n"
            table += "|:-------------:|:-------------:|:---------------:|\n"

            if jsond["device_id"] != 'all':
                device_type = jsond["device_type"] if jsond["device_type"] else 'NULL'
                device_network = 'Connected' if jsond["device_connect_state"] else 'Disconnected'
                table += f"| {jsond['device_id']:^14} | {device_type:^14} | {device_network:^16} |\n"
                table += "|:-------------:|:-------------:|:---------------:|\n"
            else:
                for device_id, _ in jsond["device_type"].items():
                    device_connect_state = jsond["device_connect_state"][device_id]
                    device_type = jsond["device_type"][device_id]
                    device_id_formatted = f"{device_id:^14}"
                    device_type_formatted = f"{device_type if device_type else 'NULL':^14}"
                    device_network_formatted = f"{'Disconnected' if device_connect_state == 0 else 'Connected':^16}"
                    table += f"| {device_id_formatted} | {device_type_formatted} | {device_network_formatted} |\n"
                table += "|:-------------:|:-------------:|:---------------:|\n"
        
            print(table)

if __name__ == '__main__':
    print(logo)
    print(title)
    S_Clustr().cmdloop()
