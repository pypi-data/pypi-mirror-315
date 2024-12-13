# -*- coding: utf-8 -*-
import subprocess

from okmodule import Module


class Filtlong(Module):
    """使用Filtlong过滤reads。

    使用该模块需要安装Filtlong，见https://github.com/rrwick/Filtlong。
    
    Args:
        input_reads_file: <pathlib.Path>，输入reads文件路径
        min_length: <int>，最小read长度
        min_mean_q: <int>，最小read平均质量值
        output_reads_file: <pathlib.Path>，输出reads文件路径k
    """
    def __init__(self, input_reads_file, min_length, min_mean_q, output_reads_file):
        self.input_reads_file = input_reads_file
        self.min_length = min_length
        self.min_mean_q = min_mean_q
        self.output_reads_file = output_reads_file

    def main(self):
        args = [
            'filtlong',
            '--min_length', str(self.min_length),
            '--min_mean_q', str(self.min_mean_q),
            str(self.input_reads_file)
        ]
        self.log(f'Running command {" ".join(args)}')
        with self.output_reads_file.open('wb') as fp:
            subprocess.run(args, stdout=fp, check=True)
