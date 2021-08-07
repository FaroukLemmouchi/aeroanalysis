from aeros5p_analysis.aeros5py_reader import read_l1b, read_aod_nc
import tarfile, shutil
import os, glob, yaml, re
from aeros5p_analysis.index import cache
import numpy as np

loader = yaml.SafeLoader
loader.add_implicit_resolver(
u'tag:yaml.org,2002:float',
re.compile(u'''^(?:
 [-+]?(?:[0-9][0-9_]*)\\.[0-9_]*(?:[eE][-+]?[0-9]+)?
|[-+]?(?:[0-9][0-9_]*)(?:[eE][-+]?[0-9]+)
|\\.[0-9_]+(?:[eE][-+][0-9]+)?
|[-+]?[0-9][0-9_]*(?::[0-5]?[0-9])+\\.[0-9_]*
|[-+]?\\.(?:inf|Inf|INF)
|\\.(?:nan|NaN|NAN))$''', re.X),
list(u'-+0123456789.'))

def get_data_locally(session_id, **kwargs):
    @cache.memoize()
    def init_data(**kwargs):
        bay = f"{kwargs['root_path']}/OUTPUTS/{kwargs['date']}/{kwargs['simulation']}"

        l1b_file =f"{bay}/S5P_L1B_4ch_{kwargs['date']}_{kwargs['pixel']}.dat"

        if glob.glob(l1b_file) == []:
            print(f'ERROR: {l1b_file} not found')
        try :
            l1b = read_l1b(l1b_file)
        except :
            l1b = np.nan
 
        print('Opening data frames..', end='')
        aod = read_aod_nc(f'{bay}/', f'{bay}/', kwargs['date'])
        print('done')
        return l1b, aod
    return init_data(**kwargs)

def load_paths(config_file, mode):
    config = yaml.load(open(config_file,"r"), Loader=loader)
    return config[mode] 

def save_paths(config_file, mode, **kwargs):
    yaml.dump({mode:kwargs}, open(config_file, "w"))

