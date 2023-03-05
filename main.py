from app.app import app
import os

port = 9000
host = '0.0.0.0'

if os.getenv('VANETLAB_BE_PORT') is not None:
  try:
    port = int(os.getenv('VANETLAB_BE_PORT'))
  except:
    print('[X] Invalid port specified, defaulting to 9000')
  
if os.getenv('VANETLAB_BE_HOST') is not None:
  host = os.getenv('VANETLAB_BE_HOST')

if __name__ == '__main__':
  app.run(host=host, port=port, debug=False, use_evalex=False)
