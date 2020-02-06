# hs-dvr-telnet.py

Python implementation using a
[slightly modified 3DES algorithm](https://github.com/tothi/pyDes)
for opening telnet interface on HiSilicon DVR devices with
advanced (encrypted) command parser.

Co-work with [Vladislav Yarmak](https://github.com/Snawoot)
([@snawoot](https://twitter.com/@snawoot)).

Detailed analysis of this 0day backdoor by Vladislav is here:

https://habr.com/en/post/486856/

Recommended usage of this PoC:

```bash
git clone https://github.com/tothi/hs-dvr-telnet
cd hs-dvr-telnet
python -m venv venv
. ./venv/bin/activate
pip install -r requirements.txt
./hs-dvr-telnet.py
```

### vendor(?) reply

Huawei/HiSilicon released a "this is not ours"
[Security Notice](https://www.huawei.com/en/psirt/security-notices/2020/huawei-sn-20200205-01-hisilicon-en) about the backdoor.

At the moment, it seems the affected part of the firmware is
related to an OEM vendor (what is most likely
[Hangzhou Xiongmai Technology](http://www.xiongmaitech.com/en/index.php/product).
