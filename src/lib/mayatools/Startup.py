from .GlobalMenu import GlobalMenu
from maya import cmds

class Startup(object):
    """
    Class called during maya's initialization.
    """

    @staticmethod
    def run():
        """
        Perform the startup routines.
        """
        Startup.__buildMenus()

    @staticmethod
    def __buildMenus():
        """
        Create the default menus.
        """
        # returning when maya is under batch mode
        if cmds.about(batch=True):
            return

        # items avaialble under umedia menu
        GlobalMenu.addItem(
            'UMedia',
            'Rendering/Send to the farm...',
            'import maya.mel; maya.mel.eval("SubmitJobToDeadline()")'
        )
