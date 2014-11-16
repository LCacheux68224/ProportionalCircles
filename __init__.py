# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ProportionalCircles
                                 A QGIS plugin
 Proportional circles
                             -------------------
        begin                : 2014-07-27
        copyright            : (C) 2014 by Lionel Cacheux
        email                : lionel.cacheux@gmx.fr
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

def classFactory(iface):
    # load ProportionalCircles class from file ProportionalCircles
    from proportionalcircles import ProportionalCircles
    return ProportionalCircles(iface)
