# encoding: utf-8

"""
Test module for ``r.sif`` build
"""

import os
import subprocess
import tempfile


pth = os.path.join('singularity', 'r.sif')


def test_r_R():
    call = f'singularity run {pth} R --version'
    out = subprocess.run(call.split(' '))
    assert out.returncode == 0


def test_r_Rscript():
    call = f'singularity run {pth} Rscript --version'
    out = subprocess.run(call.split(' '))
    assert out.returncode == 0


def test_r_R_packages():
    pwd = os.getcwd()
    call = f'singularity run --home={pwd} {pth} Rscript {pwd}/tests/extras/r.R'
    out = subprocess.run(call.split(' '))
    assert out.returncode == 0


def test_r_R_rmarkdown():
    pwd = os.getcwd()
    with tempfile.TemporaryDirectory() as d:
        os.chdir(d)
        os.system(f"cp {os.path.join(pwd, 'tests', 'extras', 'cars.Rmd')} .")
        os.system(f"cp {os.path.join(pwd, 'tests', 'extras', 'cars.R')} .")
        sif = os.path.join(pwd, pth)
        call = f"""singularity run --home={d} {sif} Rscript cars.R"""
        out = subprocess.run(call.split(' '))
        pdf_output = os.path.isfile('cars.pdf')
        os.chdir(pwd)
        assert out.returncode == 0
        assert pdf_output


def test_r_gcta():
    cwd = os.getcwd()
    with tempfile.TemporaryDirectory() as d:
        os.system(f'tar -xvf {cwd}/tests/extras/ex.tar.gz -C {d}')
        call = f'singularity run --home={d}:/home/ {pth} gcta64 --bfile /home/ex --out /home/'
        out = subprocess.run(call.split(' '))
        assert out.returncode == 0


def test_r_bigsnpr():
    pwd = os.getcwd()
    with tempfile.TemporaryDirectory() as d:
        os.chdir(d)
        os.system(f"cp {os.path.join(pwd, 'tests', 'extras', 'bigsnpr.R')} .")
        sif = os.path.join(pwd, pth)
        call = f"""singularity run --home={d} {sif} Rscript bigsnpr.R"""
        out = subprocess.run(call.split(' '))
        os.chdir(pwd)
        assert out.returncode == 0


def test_r_prsice():
    call = f'singularity run {pth} PRSice_linux --version'
    out = subprocess.run(call.split(' '))
    assert out.returncode == 0
