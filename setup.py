from distutils.core import setup
import py2exe
import os

my_dir_files = [] # list of all file in my_dir .. it a result to use
my_dir = 'qt' # set folder to want to add file to distibuit.. it in same folder
except_ext = ['.pyc']  #set not use file extention

walk = os.walk(os.path.join(os.getcwd(),my_dir)) #for dir in same folder only ... not include sub folder 

# if not use below and my dir is must to be a full path 'E:\python\...'
#my_dir = 'E:\python\...'
#walk = os.walk(my_dir)
#full_path = my_dir


for root , dirs, files in walk : #get all file with path to use and send to result
    for fi in files:
        fi_name , ext = os.path.splitext(fi)
        if ext not in except_ext:
            fi_path = os.path.join(root,fi)
            my_dir_files.append(fi_path)


setup(
    name = 'AutoTransition',
    description = 'This for a lazy Customs... include me!',
    version = '1.0',

    windows = [
                  {
                      'script': 'AutoTransition.py',
                      'icon_resources':[(1,'ubuntu.ico')],
                  }
              ],

    options = {
                  'py2exe': {
                      'packages':'encodings',
                      #'bundle_files':1, #for a single file .... error qt
                      'compressed':True,
                      'optimize' : 2,
                      'excludes':['doctest','pdb','unittest','difflib','inspect'],
                      # Optionally omit gio, gtk.keysyms, and/or rsvg if you're not using them
                      #'includes': 'cairo, pango, pangocairo, atk, gobject, gio, gtk.keysyms',
                  }
              },

    data_files=[(my_dir,my_dir_files), #add folder and file seleted into it
                   'IEDriverServer.exe',
                   'ubuntu.ico',
               ]
)
