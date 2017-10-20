import os
import maya.cmds as cmds

class GlobalMenu(object):
    """
    Simplifyied api to create a global menu in maya.

    Example:
        GlobalMenu.addItem("UMedia", "A/Foo", "print 'foo'")
        GlobalMenu.addItem("UMedia", "A/B/Foo2", "print 'foo2'")
        GlobalMenu.addSeparator("UMedia", "A/B")
        GlobalMenu.addItem("UMedia", "A/B/Foo3", "print 'foo3'")
        GlobalMenu.addSeparator("UMedia")
        GlobalMenu.addItem("UMedia", "Foo4", "print 'foo4'")
    """

    __menus = {}
    __menuItems = {}

    @staticmethod
    def addItem(menuName, itemLabel, itemCommand):
        """
        Add an item to a global menu.

        In order to create submenus, separate the levels using "/":
        itemLabel="firstLevel/secondLevel/ThirdLevel..."
        """
        parent = GlobalMenu.__buildSubMenus(
            menuName,
            os.path.dirname(itemLabel)
        )

        # creating entry
        cmds.menuItem(
            label=os.path.basename(itemLabel),
            command=itemCommand,
            parent=parent
        )

    @staticmethod
    def addSeparator(menuName, where=''):
        """
        Add a separator to the menu.
        """
        parent = GlobalMenu.__buildSubMenus(
            menuName,
            where
        )

        # creating entry
        cmds.menuItem(
            divider=True,
            parent=parent
        )

    @staticmethod
    def menu(name):
        """
        Return a maya's object id about a global menu name.

        In case the menu name does not exist, then the menu is created
        automatically.
        """
        if name not in GlobalMenu.__menus:
            GlobalMenu.__menus[name] = cmds.menu(
                label=name,
                parent='MayaWindow',
                tearOff=True
            )

        return GlobalMenu.__menus[name]

    @staticmethod
    def __buildSubMenus(menuName, path):
        """
        Build sub-menus for the input path (in case they don't exist).

        Maya's object id about the last level of the path is returned.
        @private
        """
        parent = GlobalMenu.menu(menuName)

        if path:
            currentEntry = menuName
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
