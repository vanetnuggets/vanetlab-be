from threading import Lock, Thread
from app.managers.filemanager import filemanager
from app.managers.ns3manager import ns3manager

# TODO nejaky expert na multithreding a race conditions by to mohol pofixovat toto je bordel jak kkt

class Queue:
  queue = []
  running = False # Toto by mal byt mutex no
  mtx = Lock() # toto je mutex ale nepouzivam ho
  finished = {}
  current = None

  def __init__(self):
    pass
  
  def add(self, scenario) -> int:
    """ adds a scenario to run queue
      @scenario: json with elements "name", "config" and "action"
      @returns: queue number
    """
    name = scenario['name']
    
    if not filemanager.exists_scenario(name):
      raise Exception("scenario does not exist")

    if name == self.current:
      raise Exception("duplicate name");
    
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
    
    t = Thread(target=self._activate, args=(scenario,))
    t.start()
  
  def get_status_for(self, name):
    # Check if the simulation is done
    if name in self.finished:
      status = self.finished[name]
      del self.finished[name]
      return {
        "name": name,
        "finished": True,
        "status": status['status'],
        "error": status['error'],
        "message": status['message']
      }
    
    # Check if the simulation is currently being simulated
    if self.current is not None and self.current['name'] == name:
      return {
        "name": name,
        "finished": False,
        "status": "currently being simulated",
        "position": "currently being simulated",
        "total_length": len(self.queue),
        "current": name,
        "error": False
      }

    # Check if the specified simulation is in the queue
    for i, sim in enumerate(self.queue):
      if sim['name'] == name:
        return {
          "name": name,
          "finished": False,
          "status": "in queue",
          "position": i,
          "total_length": len(self.queue),
          "current": self.queue[0]['name'],
          "error": False
        }
    
    # not in queue, not finished, not being simulated == invalid
    return {
      "name": name,
      "finished": True,
      "error": True,
      "message": "error while running the scenario. ",
      "status": "error - unknown name"
    }

  def _activate(self, scenario) -> None:
    """simulates next scenario in queue
      @scenario: json with elements "name", "config" and "action"
    """
    self.current = scenario

    action = scenario['action']
    name = scenario['name']
    conf = scenario['config']
    filemanager.prepare_simulation(name, conf)

    err = None
    if action == 'validate':
      err = ns3manager.validate(name)
    
    elif action == 'simulate':
      err = ns3manager.simulate(name)
    
    status = {
      "name": name,
      "status": "ok" if err == None else "error",
      "message": err,
      "error": False if err == None else True
    }
    self.finished[name] = status

    self.running = False
    self.next()

queue = Queue()
