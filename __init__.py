# -*- coding: utf-8 -*-
"""
/***************************************************************************
 AnyForm
                                 A QGIS plugin
 Performs an anisotropic transformation over a grid according to a ordered discrete set of points.
                             -------------------
        begin                : 2017-11-14
        copyright            : (C) 2017 by Henrique Guarneri
        email                : henriqueguarneri@gmail.com
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
    """Load AnyForm class from file AnyForm.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .AnyForm import AnyForm
    return AnyForm(iface)
