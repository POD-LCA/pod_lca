class Model:

    def __init__(self):
        self.processes = {}
        self.flows = {}
        self.calculator = Calculator()

    def create_process(self):

        process = Process()

        n = len(self.processes)
        process.id = n

        self.processes[process.id] = process

        return process
    
    def create_flow(self):

        flow = Flow()

        n = len(self.flows)
        flow.id = n

        self.flows[flow.id] = flow

        return flow


class Process:

    def __init__(self):
        self.id = None
        self.unit_process_id = None
        self.name = None
        self.life_cycle_stage = None
        self.year = 1900
        self.impacts = Impacts()

class transportationProcess(Process):

    def __init__(self):
        super().__init__(self)
        self.transported_distance = 0.0
        self.transported_weight = 0.0

class Flow:

    def __init__(self):
        self.id = None
        self.name = None
        self.type = None
        self.category = None
        self.qty = 0.0
        self.units = None
        self.impacts = Impacts()

class Impacts:

    def __init__(self):
        self.process = None
        self.GWP = 0.0
        self.acid_pot = 0.0
        self.eutro_pot = 0.0
        self.ozone_dep = 0.0
        self.smog = 0.0

class Calculator():

    def __init__(self):

        pass

    def calculate(self):

        return 2