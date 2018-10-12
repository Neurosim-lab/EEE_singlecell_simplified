"""
setup.py : Setup for EEE model
path     : eee/setup.py
author   : Joe Graham <joe.w.graham@gmail.com>

Removes compiled mod files if they exist.  Compiles mod files.  Creates data 
and figure directories.
"""

import os
import errno
from inspect import getsourcefile
import shutil
import subprocess

eeedir = os.path.dirname(os.path.abspath(getsourcefile(lambda:0)))
simdir = os.path.abspath(os.path.join(eeedir, "sim"))
moddir = os.path.abspath(os.path.join(simdir, "mod"))

ind_batchesdir = os.path.abspath(os.path.join(simdir, "batches_indcell"))
ind_batchdirs = [os.path.join(ind_batchesdir, batch) for batch in os.listdir(ind_batchesdir) if os.path.isdir(os.path.join(ind_batchesdir, batch)) and "batch" in batch]

net_batchesdir = os.path.abspath(os.path.join(simdir, "batches_network"))
net_batchdirs = [os.path.join(net_batchesdir, batch) for batch in os.listdir(net_batchesdir) if os.path.isdir(os.path.join(net_batchesdir, batch)) and "batch" in batch]

batchdirs = ind_batchdirs + net_batchdirs

modlinkdirs = list(batchdirs)
modlinkdirs.append(simdir)
modlinkdirs.append(ind_batchesdir)
modlinkdirs.append(net_batchesdir)

#batch_tools = ['analyze.py', 'batch_analysis.py', 'batch_init.py', 'batch_utils.py', 'instantiate.py', 'runmybatches']
ind_batch_tools = ['analyze.py', 'batch_init.py', 'instantiate.py', 'runmybatches']
ind_batch_tools_paths = [os.path.join(ind_batchesdir, bt) for bt in ind_batch_tools]


def make_output_dirs(batchdirs):
    """Makes dirs 'batch_data' and 'batch_figs' in each batch dir."""

    print("Making output dirs.")
    def make_batch_dirs(basedir):
        batchdatadir = os.path.join(simdir, basedir, "batch_data")
        if not os.path.exists(batchdatadir):
            os.mkdir(batchdatadir)
            print("  Making data dir: " + batchdatadir)
        batchfigdir = os.path.join(simdir, basedir, "batch_figs")
        if not os.path.exists(batchfigdir):
            os.mkdir(batchfigdir)
            print("  Making figs dir: " + batchfigdir)

    for batch in batchdirs:
        make_batch_dirs(batch)


def rm_mod_links(modlinkdirs=modlinkdirs):
    """Removes x86_64 or i386 compiled mod directory symlinks. """

    print("Removing links to compiled mods dir.")
    
    for modlinkdir in modlinkdirs:
        path1 = os.path.join(modlinkdir, "x86_64")
        path2 = os.path.join(modlinkdir, "i386")
        if os.path.islink(path1):
            if (os.path.realpath(path1) != path1):
                print("  Removing directory: " + path1)
                os.remove(path1)
            else:
                print("  Removing directory: " + path1)
                shutil.rmtree(path1, ignore_errors=True)
        if os.path.islink(path2):
            if (os.path.realpath(path1) != path2):
                print("  Removing directory: " + path2)
                os.remove(path2)
            else:
                print("  Removing directory: " + path2)
                shutil.rmtree(path2, ignore_errors=True)


def rm_mod_files(moddir=moddir):
    """Removes all symlinked mod files in the mod dir."""

    linked_mods = [os.path.join(moddir, mod) for mod in os.listdir(moddir) if os.path.islink(os.path.join(moddir, mod))]
    for mod in linked_mods:
        print("  Removing mod file: " + mod)
        os.remove(mod)


def compile(compiler="mkmod", moddir=moddir):
    """Compiles mod files using compiler (mkmod or nrnivmodl)."""
        
    curdir = os.getcwd()
    if curdir != moddir:
        os.chdir(moddir)

    print("Compiling mod files using: " + compiler)
    compile_output = subprocess.call(compiler, shell=True)

    print
    print("Compile output:")
    print(compile_output)
    print

    if curdir != os.getcwd():   
        os.chdir(curdir)
        

def link_mod_dirs(moddir=moddir, modlinkdirs=modlinkdirs):
    """Symlinks the NEURON compiler output folder into the given directories."""

    print("Linking to compiled mod file dir.")

    if not os.path.isdir(os.path.join(moddir, "x86_64")) and not os.path.isdir(os.path.join(moddir, "i386")):
        print("  Compiled folder not found for symlinking!")
    else:
        for modlinkdir in modlinkdirs:
            if os.path.isdir(os.path.join(moddir, "x86_64")): 
                if not os.path.isdir(os.path.join(modlinkdir, "x86_64")):
                    print("  Symlinking " + os.path.join(modlinkdir, "x86_64") + " to " + os.path.join(moddir, "x86_64"))
                    os.symlink(os.path.join(moddir, "x86_64"), os.path.join(modlinkdir, "x86_64"))
            elif os.path.isdir(os.path.join(moddir, "i386")): 
                if not os.path.isdir(os.path.join(modlinkdir, "i386")):
                    print("  Symlinking " + os.path.join(modlinkdir, "i386") + " to " + os.path.join(moddir, "i386"))
                    os.symlink(os.path.join(moddir, "i386"), os.path.join(modlinkdir, "i386"))


def make_symlinks(filepath, linkpath):
    """Creates symlinks to filepath(s) in linkpath(s), both can be string or list."""

    if type(filepath) is str:
        filepath = [filepath]
    if type(linkpath) is str:
        linkpath = [linkpath]

    for indfile in filepath:
        filename = os.path.split(indfile)[1]
        for indlink in linkpath:
            print("Executing: os.symlink(" + indfile + ", " + os.path.join(indlink, filename) + ")")
            try:
                os.symlink(indfile, os.path.join(indlink, filename))
            except OSError, e:  
                if e.errno == errno.EEXIST:
                    print("  Removing existing link and recreating.")
                    os.remove(os.path.join(indlink, filename))
                    os.symlink(indfile, os.path.join(indlink, filename))
                else:
                    raise e



if __name__ == "__main__":

    print
    print("Setting up EEE project from setup.py")
    print
    print("  eeedir    : %s" % (eeedir))
    print("  simdir    : %s" % (simdir))
    print("  moddir    : %s" % (moddir))
    print
    
    make_output_dirs(batchdirs)

    rm_mod_links(modlinkdirs=modlinkdirs)

    rm_mod_files(moddir=moddir)

    #compile(compiler="mkmod", moddir=moddir)
    compile(compiler="nrnivmodl", moddir=moddir)
    
    link_mod_dirs(moddir=moddir, modlinkdirs=modlinkdirs)

    make_symlinks(ind_batch_tools_paths, ind_batchdirs)
    
    print("Finished setting up EEE project.")




