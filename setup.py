import cx_Freeze
from os import listdir, path
#from os.path import isfile, join

dir = path.dirname(__file__)

mypath = 'C:/Users/Liwia/Desktop/passage32/utilities/'

#print('da' + dir )

listOffiles = [f for f in listdir(mypath)]  #if isfile(join(mypath, f))]

#dir = path.dirname(__file__)

newlistOffiles = []
for i in listOffiles:
    newlistOffiles.append('utilities/' + str(i))

executables = [cx_Freeze.Executable("main.py")]

#dodatkowe parametry nie dzialaja
cx_Freeze.setup(targetName = "PPassage", author = "LL", version = "0.2", options = {"build_exe": {"packages":["pygame", "time", "random", "tkinter", "os", "sys", "PIL", "pickle"],
                           "include_files":[f for f in newlistOffiles]}}, description = "bida", executables = executables)


"""
from distutils.core import setup
import py2exe, sys
from os import listdir, path

#dir = path.dirname(__file__)
mypath = 'C:/Users/Liwia/Desktop/passage22/utilities/'
listOffiles = [f for f in listdir(mypath)]

newlistOffiles = []
for i in listOffiles:
    newlistOffiles.append('utilities/' + str(i))

sys.argv.append('py2exe')
setup( 
  options = {         
    'py2exe' : {
        'compressed': 1, 
        'optimize': 2,
        'bundle_files': 3, #Options 1 & 2 do not work on a 64bit system
        'dist_dir': 'dist',  # Put .exe in dist/
        'xref': False,
        'skip_archive': False,
        'ascii': False,
        }
        },    
    data_files = [f for f in newlistOffiles],         
    zipfile = "shared.lib", 
    windows = [{'script': "main.py"}],
)     
"""                     