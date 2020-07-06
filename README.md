# Domain Scanning Tool

A tool for domain bulk scanning based on SOA record. It can be used to find nice domain hacks at high speed.

Its features include:

- Easy to use interface;
- Fast scanning speed;
- Supporting both IPv4 and IPv6
- (Theoretically) supporting all suffixes including secondary ones and even higher levels;
- Supporting scanning multiple suffixes at once;
- Only relying on Python built-in libraries.



To use this tool, simple run:

```
git clone https://github.com/dynos01/DomainScanningTool
cd DomainScanningTool
python DomainScanningTool.py
```

Server addresses are like these: `8.8.8.8:53`, `1.1.1.1:53, [2001:4860:4860::8888]:53`

Suffixes are like these: `com`, `com, net` (e.g. without the dot)



The example dictionary `LLL.txt` contains all combinations of there letters. You can use your own dictionary instead.



Known limitations:

- Can't distinguish reserved domains, as this tool relies on DNS system.
