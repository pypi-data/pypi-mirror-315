'''
Date: 2024-12-13 20:18:59
LastEditors: BHM-Bob 2262029386@qq.com
LastEditTime: 2024-12-16 10:12:31
Description: 
'''

import argparse
import os
import time
from functools import wraps
from pathlib import Path
from typing import Dict, List, Tuple, Union

from mbapy_lite.base import Configs, put_err
from mbapy_lite.file import get_paths_with_extension, opts_file
from mbapy_lite.web import TaskPool, random_sleep
from pymol import cmd
from tqdm import tqdm

from lazydock.scripts._script_utils_ import Command, clean_path, excute_command
from lazydock.web.cgenff import get_login_browser, get_result_from_CGenFF


class prepare_complex(Command):
    HELP = """
    prepare complex for GROMACS MDS.
    - input complex.pdb should have two chains, one for receptor and one for ligand.
    - complex.pdb should already add hydrogens by Avogadro or other software.
    - complex.pdb is supposed to be aligned with the axes to save space when MDS.
    
    STEPS:
    0. center complex.pdb by obabel, align with xyz axes by lazydock.
    1. extract receptor and ligand from complex.pdb.
    2. transfer ligand.pdb to mol2 by obabel.
    3. fix ligand name in mol2 file.
    4. sort mol2 bonds by lazydock.
    5. retrive str file from CGenFF.
    6. transfer str file to top and gro file by cgenff_charmm2gmx.py
    7. make receptor.top
    8. build complex.top and complex.gro
    9. run solve, ion
    10. make select index file and add restraints to complex.top and complex.gro
    11. run last MDS
    """
    def __init__(self, args, printf = print):
        super().__init__(args, printf)
        
    @staticmethod
    def make_args(args: argparse.ArgumentParser):
        args.add_argument('-d', '--dir', type = str, default='.',
                                help='complex directory. Default is %(default)s.')
        args.add_argument('-n', '--complex-name', type = str,
                                help='complex name in each sub-directory.')
        args.add_argument('--receptor-chain-name', type = str,
                                help='receptor chain name.')
        args.add_argument('--ligand-chain-name', type = str,
                                help='ligand chain name.')
        return args
    
    def process_args(self):
        self.args.dir = clean_path(self.args.dir)
        
    def main_process(self):
        if os.path.isdir(self.args.dir):
            complexs_path = get_paths_with_extension(self.args.dir, [], name_substr=self.args.complex_name)
        else:
            put_err(f'dir argument should be a directory: {self.args.config}, exit.', _exit=True)
        print(f'get {len(complexs_path)} complex(s)')
        for complex_path in tqdm(complexs_path, total=len(complexs_path)):
            complex_path = Path(complex_path).resolve()
            result_dir = complex_path.parent / f'{complex_path.stem}_result'
            os.makedirs(result_dir, exist_ok=True)
            cmd.reinitialize()
            # extract receptor and ligand
            cmd.load(str(complex_path), 'complex')
            success = True
            for mol, chain in zip(['receptor', 'ligand'], [self.args.receptor_chain_name, self.args.ligand_chain_name]):
                if cmd.select(mol, f'complex and chain {chain}') == 0:
                    put_err(f'{mol} chain {chain} has zero atom in {complex_path}, skip this complex.')
                    success = False
                else:
                    cmd.save(f'{complex_path.parent}/{complex_path.stem}_{mol}.pdb', mol)
            if not success:
                continue

_str2func = {
    'prepare-complex': prepare_complex,
}

def main(sys_args: List[str] = None):
    args_paser = argparse.ArgumentParser(description = 'tools for GROMACS.')
    subparsers = args_paser.add_subparsers(title='subcommands', dest='sub_command')

    prepare_complex_args = prepare_complex.make_args(subparsers.add_parser('prepare-complex', description=prepare_complex.HELP))

    excute_command(args_paser, sys_args, _str2func)


if __name__ == "__main__":
    # pass
    
    main()