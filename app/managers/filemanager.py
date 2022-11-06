from os import mkdir, path
from shutil import rmtree
import glob, os

class FileManager:
  def __init__(self):
    if path.exists('./scenarios'):
      rmtree('./scenarios')
    
    mkdir('./scenarios')
    mkdir('./scenarios/tmp')
    self.my_path = os.path.abspath('.')
  
  def get_logs(self):
    fnames = []
    for f in glob.glob(f'scenarios/tmp/*.pcap'):
      filename = f.split('/')[-1].strip()
      fnames.append(filename)
    return fnames

  def get_file(self, filename):
    root = os.path.abspath('.')
    if os.path.isfile(f'{root}/scenarios/tmp/{filename}') is False:
      return None
    return f'{root}/scenarios/tmp/{filename}'

  def load(self, file):
    filename = file.filename

    if filename == '':
      return None, 'no file uploaded'
    
    if filename.split('.')[-1].strip() != 'py':
      return None, "only accepts python ns3 scripts for now."

    try:
      rmtree('./scenarios/tmp/')
      mkdir('./scenarios/tmp/')
    
    except OSError as e:
      pass

    file_path = './scenarios/tmp/' + filename

    file.save(file_path)
    return file_path, None
    

filemanager = FileManager()