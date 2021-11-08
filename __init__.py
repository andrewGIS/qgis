# -*- coding: utf-8 -*-
"""
/***************************************************************************
 mySelectionNewDock
                                 A QGIS plugin
 mySelectionNewDock
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2021-11-03
        copyright            : (C) 2021 by andrew tarasov
        email                : some@mail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load mySelectionNewDock class from file mySelectionNewDock.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .mySelectionNewDock import mySelectionNewDock
    return mySelectionNewDock(iface)
