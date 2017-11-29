from .GlobalMenu import GlobalMenu
from .MayaContext import MayaContext
from basetools.App import Hook
import maya.mel

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

        umediaMenu = GlobalMenu("UMedia")

        # items avaialble under umedia menu
        umediaMenu.addItem(
            'Rendering/Send to the farm...',
            lambda: maya.mel.eval("SubmitJobToDeadline()")
        )


# registering hook
Hook.register(
    'maya',
    MayaHook,
    MayaContext
)
