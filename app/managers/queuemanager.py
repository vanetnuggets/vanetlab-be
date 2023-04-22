from threading import Lock
from app.managers.filemanager import filemanager
from app.managers.ns3manager import ns3manager

class Queue:
  queue = []
  running = False
  mtx = Lock()
  finished = {}

  def __init__(self):
    pass
  
  def add(self, scenario) -> int:
    """ adds a scenario to run queue
      @scenario: json with elements "name", "config" and "action"
      @returns: queue number
    """
    for name in self.queue:
      if scenario == name:
        raise Exception("duplicate name")
    
    self.queue.append(scenario)
    return len(self.queue) - 1

  def next(self) -> None:
    """ checker wrapper for _activate function 
    """
    if self.running:
      return
    
    if len(self.queue) == 0:
      return
    
    self.running = True
    scenario = self.queue.pop(0)
    self._activate(scenario)
  
  def get_status_for(self, name):
    if name in finished:
      return {
        "name": name,
        "finished": True,
        "status": finished['name']
      }
      del finished[name]

    for i, sim in enumerate(self.queue):
      if self.queue['name'] == name:
        return {
          "name": name,
          "finished": False,
          "status": "in queue",
          "position": i,
          "total_length": len(self.queue),
          "current": self.queue[0]['name']
        }

  def _activate(self, scenario) -> None:
    """simulates next scenario in queue
      @scenario: json with elements "name", "config" and "action"
    """
    action = scenario['action']
    name = scenario['name']
    conf = scenario['config']
    
    print('preparing', name)
    filemanager.prepare_simulation(name, conf)

    err = None
    print('simulating...')
    if action == 'validate':
      err = ns3manager.validate(name)
    
    elif action == 'simulate':
      err = ns3manager.simulate(name)
    
    status = {
      "name": name,
      "status": "ok" if err == None else "error",
      "message": err
    }
    print(status)
    self.finished[name] = status

    self.running = False
    self.next()

queue = Queue()
