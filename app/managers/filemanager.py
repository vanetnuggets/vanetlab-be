from os import mkdir, path
from shutil import rmtree
from app.parser.parser import parser
import glob, os
import uuid

class FileManager:
  def __init__(self):
    self.my_path = os.path.abspath('.')

  def delete_scenario(self, code):
    try:
      rmtree(f'{self.my_path}/scenarios/{code}')
      return True
    except OSError:
      return False
  def move_output(self, waf_path, code):
    # Move all .pcap files
    for f in glob.glob(f'{waf_path}/*.pcap'):
      filename = f.split('/')[-1].strip()
      os.rename(f, f'{self.my_path}/scenarios/{code}/{filename}')
    
    # Hopefully wont crash if empty
    for f in glob.glob(f'{waf_path}/*.tr'):
      filename = f.split('/')[-1].strip()
      os.rename(f, f'{self.my_path}/scenarios/{code}/{filename}')
    
    # Ze setko ok abo co 
    return True

  def get_pcap_logs(self, code):
    fnames = []
    for f in glob.glob(f'scenarios/{code}/*.pcap'):
      filename = f.split('/')[-1].strip()
      fnames.append({
        "name": filename,
        "size": os.path.getsize(f)
      })
    return fnames

  def get_file(self, filename):
    root = os.path.abspath('.')
    if os.path.isfile(f'{root}/scenarios/tmp/{filename}') is False:
      return None
    return f'{root}/scenarios/tmp/{filename}'

  def save_json(self, json):
    code = str(uuid.uuid4())
    # Create simulation directory
    # TODO check if already exists and regenerate new uuid if so
    
    full_path = f'{self.my_path}/scenarios/{code}'
    os.makedirs(full_path)

    filename = 'scenario.py'

    ns3_script = parser.parse(json, iam_json=True)
    scenario_path = f'{full_path}/{filename}'
    with open(scenario_path, 'w') as f:
      f.write(ns3_script)
    
    return scenario_path, code
    

filemanager = FileManager()