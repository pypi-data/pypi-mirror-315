# -*- coding: utf-8 -*-
from okmodule import Command


class Fastqc(Command):
    """使用fastqc进行质量控制。

    使用该模块需要安装fastqc，安装方法可以参考https://www.bioinformatics.babraham.ac.uk/projects/fastqc/。

    Args:
        outdir: <pathlib.Path>，输出路径
        seqfile: <pathlib.Path>，测序文件
        threads: <int>，线程数，默认为4
    """
    def __init__(self, outdir, seqfile, threads=4):
        self.outdir = outdir
        self.seqfile = seqfile
        self.threads = threads

    def args(self):
        return [
            '--outdir', str(self.outdir),
            '--threads', str(self.threads),
            '--extract',
            str(self.seqfile)
        ]
