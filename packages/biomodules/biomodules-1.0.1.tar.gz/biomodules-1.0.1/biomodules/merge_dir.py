# -*- coding: utf-8 -*-
import gzip
from pathlib import Path
from shutil import copyfileobj

from okmodule import Module


class MergeDir(Module):
    """给定一个输入文件夹和一个输出文件，把该文件夹下的所有文件合并到该文件中。

    Args:
        indir: <pathlib.Path>，输入文件夹
        outfile: <pathlib.Path>，输出文件
    """
    def __init__(self, indir, outfile):
        if isinstance(indir, str):
            indir = Path(indir)
        self.indir = indir
        if isinstance(outfile, str):
            outfile = Path(outfile)
        self.outfile = outfile

    def main(self):
        with self.outfile.open('wb') as ofp:
            for infile in self.indir.iterdir():
                if not infile.is_file():
                    continue
                with open(infile, 'rb') as ifp:
                    copyfileobj(ifp, ofp)


class MergeGzipDir(Module):
    """给定一个输入文件夹和一个输出文件，把该文件夹下的所有gzip文件合并到该文件中。

    Args:
        indir: <pathlib.Path>，输入文件夹
        outfile: <pathlib.Path>，输出文件（gzip文件，以.gz结尾）
    """
    def __init__(self, indir, outfile):
        self.indir = indir
        self.outfile = outfile

    def main(self):
        with self.outfile.open('wb') as ofp:
            for infile in self.indir.iterdir():
                if (not infile.is_file()) or (infile.suffix != '.gz'):
                    continue
                with gzip.open(infile, 'rb') as ifp:
                    copyfileobj(ifp, ofp)
