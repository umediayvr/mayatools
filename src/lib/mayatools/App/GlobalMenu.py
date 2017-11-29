import os
import maya.cmds as cmds

class GlobalMenu(object):
    """
    Simplified api to create/manage a global menu in maya.

    Example:
        def doSomething():
            # ...

        umediaMenu = GlobalMenu("UMedia")
        umediaMenu.addItem("A/Foo", doSomething)
        umediaMenu.addItem("A/B/Foo2", lambda: maya.mel.eval('...'))
        umediaMenu.addSeparator("A/B")
    """

    __menus = {}
    __menuItems = {}
    __menuCommands = {}

    def __init__(self, menuName):
        """
        Create a global menu object.
        """
        self.__name = menuName

    def name(self):
        """
        Return the menu name.
        """
        return self.__name

    def addItem(self, itemLabel, callableCommand):
        """
        Add an item to a global menu.

        In order to create submenus, separate the levels using "/":
        itemLabel="firstLevel/secondLevel/ThirdLevel..."
        """
        assert callable(callableCommand), "callableCommand is not a callable"

        parent = self.__buildSubMenus(
            os.path.dirname(itemLabel)
        )

        # creating entry
        cmds.menuItem(
            label=os.path.basename(itemLabel),
            command="import mayatools;mayatools.App.GlobalMenu.executeMenuCommand('{0}', '{1}')".format(
                self.name(), itemLabel
            ),
            parent=parent
        )

        # registering the menu command callable
        if self.name() not in self.__menuCommands:
            self.__menuCommands[self.name()] = {}
        self.__menuCommands[self.name()][itemLabel] = callableCommand

    def addSeparator(self, where=''):
        """
        Add a separator to the menu.
        """
        parent = GlobalMenu.__buildSubMenus(
            self.name(),
            where
        )

        # creating entry
        cmds.menuItem(
            divider=True,
            parent=parent
        )

    @staticmethod
    def executeMenuCommand(menuName, itemLabel):
        """
        Execute the command associated with the menu item.
        """
        return GlobalMenu.__menuCommands[menuName][itemLabel]()

    def __mayaObjectId(self):
        """
        Return a maya's object id about a global menu name.

        In case the menu name does not exist, then the menu is created
        automatically.
        """
        if self.name() not in GlobalMenu.__menus:
            GlobalMenu.__menus[self.name()] = cmds.menu(
                label=self.name(),
                parent='MayaWindow',
                tearOff=True
            )

        return GlobalMenu.__menus[self.name()]

    def __buildSubMenus(self, path):
        """
        Build sub-menus for the input path (in case they don't exist).

        Maya's object id about the last level of the path is returned.
        @private
        """
        parent = self.__mayaObjectId()

        if path:
            currentEntry = self.name()
            for level in path.split("/"):
                currentEntry = os.path.join(currentEntry, level)
                if currentEntry not in GlobalMenu.__menuItems:
                    GlobalMenu.__menuItems[currentEntry] = cmds.menuItem(
                        label=level,
                        subMenu=True,
                        tearOff=True,
                        parent=parent
                    )
                parent = GlobalMenu.__menuItems[currentEntry]

        return parent
