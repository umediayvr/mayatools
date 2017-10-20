from basetools.App import Context, ContextFileNameError
import maya.cmds as cmds

class MayaContext(Context):
    """
    Context implementation for maya.
    """

    @classmethod
    def fileName(cls):
        """
        Return a string about current file path of the opened file.

        In case the file is not saved, then raise the exception ContextFileNameError.
        """
        if not cls.isEmpty():
            return cmds.file(query=True, location=True)

        raise ContextFileNameError(
            "Could not figureout scene name"
        )

    @classmethod
    def isEmpty(cls):
        """
        Return a boolean telling if the scene has never been saved.
        """
        return cmds.file(query=True, location=True) == "unknown"

    @classmethod
    def hasModification(cls):
        """
        Return a boolean telling if the scene has modifications.

        This is used to decide if the scene needs to be saved.
        """
        return cmds.file(query=True, modified=True)

    @classmethod
    def hasGUI(cls):
        """
        Return a boolean telling if application is running with through GUI.
        """
        return (not cmds.about(batch=True))
