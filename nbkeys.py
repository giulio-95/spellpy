import os
from glob import glob
from spellpy import spell
import matplotlib.pyplot as plt


if __name__ == '__main__':
    input_dir = './data'
    output_dir = './result'
    log_format = '<Date> <Time,<Content>'
    tau = 0.5
    taux = [p / 10 for p in range(1, 11)]
    keys = []
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for pwd in glob(input_dir + '/testdevo.log'):
        log_name = os.path.basename(pwd)
    for tau in taux:
        parser = spell.LogParser(indir=input_dir, outdir=output_dir,
                                 log_format=log_format, tau=tau)
        parser.parse(log_name)
        keys.append(parser.nb_keys)
        print(keys)

    plt.plot(taux, keys, '-ok')
    plt.title('hdfs number keys for different tau')
    plt.show()
