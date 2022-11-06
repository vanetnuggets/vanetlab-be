from os import mkdir, path
from shutil import rmtree

class FileManager:
  def __init__(self):
    if path.exists('./scenarios'):
      rmtree('./scenarios')
    
    mkdir('./scenarios')
    mkdir('./scenarios/tmp')
  
  def load(self, file):
    filename = file.filename

    if filename == '':
      return None, 'no file uploaded'
    
    print(filename.split('.'))
    if filename.split('.')[-1].strip() != 'py':
      return None, "only accepts python ns3 scripts for now."

    try:
      rmtree('./scenarios/tmp/')
      mkdir('./scenarios/tmp/')
    
    except OSError as e:
      print(e)

    file_path = './scenarios/tmp/' + filename

    file.save(file_path)
    return file_path, None
    

filemanager = FileManager()