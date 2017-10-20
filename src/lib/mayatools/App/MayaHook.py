from .GlobalMenu import GlobalMenu
from .MayaContext import MayaContext
from basetools.App import Hook

class MayaHook(Hook):
    """
    Hook implementation for maya.
    """

    def startup(self):
        """
        Perform startup routines.
        """
        super(MayaHook, self).startup()

        self.__buildMenus()

    def __buildMenus(self):
        """
        Create the default menus.
        """
        # returning when application is under batch mode
        if not self.context().hasGUI():
            return

        # items avaialble under umedia menu
        GlobalMenu.addItem(
            'UMedia',
            'Rendering/Send to the farm...',
            'import maya.mel; maya.mel.eval("SubmitJobToDeadline()")'
        )


# registering hook
Hook.register(
    'maya',
    MayaHook,
    MayaContext
)
