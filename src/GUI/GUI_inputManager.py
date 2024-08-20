from POD_LCA_MATERIAL.projectManager.inputManager import InputManager

class GUIInputManager(InputManager):

    @staticmethod
    def create_process(model, name, project):

        model.create_process(name, project)


    @classmethod
    def create_product():

        pass