import socket

class NdControl():
    
    def __init__(self,nd287_ip,nd287_port=1050):
        self.ip_address = nd287_ip
        self.port_num = nd287_port#port番号は固定.
        self.buffer_size = 1024
        self.getvalue_command = (0x61B).to_bytes(13,'little')
        #self.getbalue_commandの中身
        #b'\x1b\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

    #値取得用のメソッド
    def socket_send(self,send_cmd):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_client:
            tcp_client.connect((self.ip_address,self.port_num))
            tcp_client.send(send_cmd) 
            raw_response = tcp_client.recv(self.buffer_size)            
            tcp_client.close()
            return raw_response

    def get_display(self):
        raw_response = self.socket_send((0x61B).to_bytes(13,'little'))
        after_ex_value = float((raw_response[12:24]).decode("utf-8").replace(' ', ''))
        return after_ex_value
    
    def get_value(self):
        raw_response = self.socket_send((0x501).to_bytes(13,'little'))
        #after_ex_value = float((raw_response[12:24]).decode("utf-8").replace(' ', ''))
        return raw_response