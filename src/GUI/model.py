class Model():

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


class Process():

    def __init__(self):
        self.id = None
        self.unit_process_id = None
        self.name = None
        self.exchanges = {}

class Flow():

    def __init__(self):
        self.id = None
        self.flow_id = None
        self.name = None

class Calculator():

    def __init__(self):

        pass

    def calculate(self):

        return 2