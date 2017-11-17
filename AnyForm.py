# -*- coding: utf-8 -*-
"""
/***************************************************************************
 AnyForm
                                 A QGIS plugin
 Performs an anisotropic transformation over a grid according to a ordered discrete set of points.
                              -------------------
        begin                : 2017-11-14
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Henrique Guarneri
        email                : henriqueguarneri@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import *#QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import *#QAction, QIcon, QFileDialog, QProgressBar
from qgis.core import *
from qgis.utils import iface
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from AnyForm_dialog import AnyFormDialog
import os.path
import pandas
import time
from anisotroPy import basegrid, basepath, transformation


class AnyForm:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'AnyForm_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)


        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Anisotropic Transformation')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'AnyForm')
        self.toolbar.setObjectName(u'AnyForm')

        

        


    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('AnyForm', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        # Create the dialog (after translation) and keep reference
        self.dlg = AnyFormDialog()

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)



        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/AnyForm/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Anisotropic transformation'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Anisotropic Transformation'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

    def set_progress_bar(self):

        """Set progress bar"""
        progressMessageBar = iface.messageBar().createMessage("Calculating anisotropic transformation...")
        progress = QProgressBar()
        progress.setMaximum(10)
        progress.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        progressMessageBar.layout().addWidget(progress)
        iface.messageBar().pushWidget(progressMessageBar, iface.messageBar().INFO)
        return progress

    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()

        def selectFile():
            self.dlg.OutputlineEdit.setText(QFileDialog.getSaveFileName())
        self.dlg.pushButton.clicked.connect(selectFile)
        # Run the dialog event loop
        result = self.dlg.exec_()

        # See if OK was pressed
        if result:
            # Setting progress bar
            progress = self.set_progress_bar()
            # Get the transformation base layers from view
            basepathLayer = self.dlg.basePathComboBox.currentLayer()
            basegridLayer = self.dlg.baseGridComboBox.currentLayer()
            # Get the transformation input parameters
            maximumSearch = float(self.dlg.MSSpinBox.value())
            searchTolerance = float(self.dlg.STSpinBox.value())
            # Create basepath
            bp  = basepath.Basepath()

            bp.load_layer(basepathLayer)
            bp.calculate_s()
            bp.calculate_bc()
            bp.calculate_vbc()
            
            # Create basegrid
            bg  = basegrid.Basegrid()
            bg.load_layer(basegridLayer)
            
            #print bp.basepath
            #print '------------------------------'
            #print bg.basegrid

            # Set transformation
            trg = transformation.Transformation(bp, bg, msp=maximumSearch, st = searchTolerance)
            # Run transformation
            trg.run(progressbar = progress)
            del trg
            bg.save_layer(basegridLayer)
            iface.messageBar().clearWidgets()
