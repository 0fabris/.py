#!/usr/bin/python

'''

    M3U Converter into Enigma2 IPTV Bouquet format
    0fabris
    12/2020

'''

#Include Librerie
import sys
import re

#Class Converter
class E2M3UConverter():
    #Constructor
    def __init__(self,name, dest):
        self.name = name
        self.dest = outname

    #Private method -> get list of tuple (name,url) from M3U
    def _parseM3U(self):
        with open(self.name, "r") as f:
            fl = f.read()
        return re.findall(r"#EXTINF:.*,\s?(.*?)\n(.*?)\n",fl)

    #given tuple list write the E2 File 
    def _writeE2IPTV(self,chanurl):
        count = 1
        with open(f"userbouquet.{self.dest}.tv","w") as f:
            f.write("#NAME IPTV LIST\n")
            for i in chanurl:
                f.write(f"#SERVICE 4097:0:1:{count}:0:0:0:0:0:0:" + i[1].replace(":","%3a") + ":" + i[0] + f"\n#DESCRIPTION {i[0]}\n")

    #method that converts from m3u to E2
    def convert(self):
        m3u = self._parseM3U()
        self._writeE2IPTV(m3u)
        print("OK, m3u converted into E2 IPTV Playlist")


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        conv = E2M3UConverter(sys.argv[1],sys.argv[1].replace("."+sys.argv[1].split(".")[-1],"") if len(sys.argv) == 2 else sys.argv[2])
        conv.convert()
    else:
        exit("Use: python " + sys.argv[0] + " nf.m3u [dest -> \"userbouquet.{dest}.tv\"]")
