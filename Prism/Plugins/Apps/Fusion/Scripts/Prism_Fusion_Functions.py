# -*- coding: utf-8 -*-
#
####################################################
#
# PRISM - Pipeline for animation and VFX projects
#
# www.prism-pipeline.com
#
# contact: contact@prism-pipeline.com
#
####################################################
#
#
# Copyright (C) 2016-2020 Richard Frangenberg
#
# Licensed under GNU GPL-3.0-or-later
#
# This file is part of Prism.
#
# Prism is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Prism is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Prism.  If not, see <https://www.gnu.org/licenses/>.


import os
import json
import time
import sys

try:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
except:
    from PySide.QtCore import *
    from PySide.QtGui import *

from PrismUtils.Decorators import err_catcher as err_catcher


class Prism_Fusion_Functions(object):
    def __init__(self, core, plugin):
        self.core = core
        self.plugin = plugin

    @err_catcher(name=__name__)
    def instantStartup(self, origin):
        #   qapp = QApplication.instance()

        with (
            open(
                os.path.join(
                    self.core.prismRoot,
                    "Plugins",
                    "Apps",
                    "Fusion",
                    "UserInterfaces",
                    "FusionStyleSheet",
                    "Fusion.qss",
                ),
                "r",
            )
        ) as ssFile:
            ssheet = ssFile.read()

        ssheet = ssheet.replace(
            "qss:",
            os.path.join(
                self.core.prismRoot,
                "Plugins",
                "Apps",
                "Fusion",
                "UserInterfaces",
                "FusionStyleSheet",
            ).replace("\\", "/")
            + "/",
        )

        
        # ssheet = ssheet.replace("#c8c8c8", "rgb(47, 48, 54)").replace("#727272", "rgb(40, 40, 46)").replace("#5e90fa", "rgb(70, 85, 132)").replace("#505050", "rgb(33, 33, 38)")
        # ssheet = ssheet.replace("#a6a6a6", "rgb(37, 39, 42)").replace("#8a8a8a", "rgb(37, 39, 42)").replace("#b5b5b5", "rgb(47, 49, 52)").replace("#999999", "rgb(47, 49, 52)")
        # ssheet = ssheet.replace("#9f9f9f", "rgb(31, 31, 31)").replace("#b2b2b2", "rgb(31, 31, 31)").replace("#aeaeae", "rgb(35, 35, 35)").replace("#c1c1c1", "rgb(35, 35, 35)")
        # ssheet = ssheet.replace("#555555", "rgb(27, 29, 32)").replace("#717171", "rgb(27, 29, 32)").replace("#878787", "rgb(37, 39, 42)").replace("#7c7c7c", "rgb(37, 39, 42)")
        # ssheet = ssheet.replace("#4c4c4c", "rgb(99, 101, 103)").replace("#5b5b5b", "rgb(99, 101, 103)").replace("#7aa3e5", "rgb(65, 76, 112)").replace("#5680c1", "rgb(65, 76, 112)")
        # ssheet = ssheet.replace("#5a5a5a", "rgb(35, 35, 35)").replace("#535353", "rgb(35, 35, 41)").replace("#373737", "rgb(35, 35, 41)").replace("#858585", "rgb(31, 31, 31)").replace("#979797", "rgb(31, 31, 31)")
        # ssheet = ssheet.replace("#4771b3", "rgb(70, 85, 132)").replace("#638dcf", "rgb(70, 85, 132)").replace("#626262", "rgb(45, 45, 51)").replace("#464646", "rgb(45, 45, 51)")
        # ssheet = ssheet.replace("#7f7f7f", "rgb(60, 60, 66)").replace("#6c6c6c", "rgb(60, 60, 66)").replace("#565656", "rgb(35, 35, 41)").replace("#5d5d5d", "rgb(35, 35, 41)")
        # ssheet = ssheet.replace("white", "rgb(200, 200, 200)")
        if "parentWindows" in origin.prismArgs:
            origin.messageParent.setStyleSheet(ssheet)
            #   origin.messageParent.resize(10,10)
            #   origin.messageParent.show()
            origin.parentWindows = True
        else:
            qapp = QApplication.instance()
            qapp.setStyleSheet(ssheet)
            appIcon = QIcon(
                os.path.join(
                    self.core.prismRoot, "Scripts", "UserInterfacesPrism", "p_tray.png"
                )
            )
            qapp.setWindowIcon(appIcon)

        self.isRendering = [False, ""]

        return False

    @err_catcher(name=__name__)
    def startup(self, origin):
        if not hasattr(self, "fusion"):
            return False

        origin.timer.stop()
        return True

    @err_catcher(name=__name__)
    def onProjectChanged(self, origin):
        pass

    @err_catcher(name=__name__)
    def sceneOpen(self, origin):
        if hasattr(origin, "asThread") and origin.asThread.isRunning():
            origin.startasThread()

    @err_catcher(name=__name__)
    def executeScript(self, origin, code, preventError=False):
        if preventError:
            try:
                return eval(code)
            except Exception as e:
                msg = "\npython code:\n%s" % code
                exec(
                    "raise type(e), type(e)(e.message + msg), sys.exc_info()[2]")
        else:
            return eval(code)

    @err_catcher(name=__name__)
    def getCurrentFileName(self, origin, path=True):
        curComp = self.fusion.GetCurrentComp()
        if curComp is None:
            currentFileName = ""
        else:
            currentFileName = self.fusion.GetCurrentComp().GetAttrs()[
                "COMPS_FileName"]

        return currentFileName

    @err_catcher(name=__name__)
    def getSceneExtension(self, origin):
        return self.sceneFormats[0]

    @err_catcher(name=__name__)
    def saveScene(self, origin, filepath, details={}):
        try:
            return self.fusion.GetCurrentComp().Save(filepath)
        except:
            return ""

    @err_catcher(name=__name__)
    def getImportPaths(self, origin):
        return False

    @err_catcher(name=__name__)
    def getFrameRange(self, origin):
        startframe = self.fusion.GetCurrentComp().GetAttrs()[
            "COMPN_GlobalStart"]
        endframe = self.fusion.GetCurrentComp().GetAttrs()["COMPN_GlobalEnd"]

        return [startframe, endframe]

    @err_catcher(name=__name__)
    def setFrameRange(self, origin, startFrame, endFrame):
        comp = self.fusion.GetCurrentComp()
        comp.Lock()
        comp.SetAttrs(
            {
                "COMPN_GlobalStart": startFrame,
                "COMPN_RenderStart": startFrame,
                "COMPN_GlobalEnd": endFrame,
                "COMPN_RenderEnd": endFrame
            }
        )
        comp.SetPrefs(
            {
                "Comp.Unsorted.GlobalStart": startFrame,
                "Comp.Unsorted.GlobalEnd": endFrame,
            }
        )
        comp.Unlock()

    @err_catcher(name=__name__)
    def getFPS(self, origin):
        return self.fusion.GetCurrentComp().GetPrefs()["Comp"]["FrameFormat"]["Rate"]

    @err_catcher(name=__name__)
    def setFPS(self, origin, fps):
        return self.fusion.GetCurrentComp().SetPrefs({"Comp.FrameFormat.Rate": fps})

    @err_catcher(name=__name__)
    def getResolution(self):
        width = self.fusion.GetCurrentComp().GetPrefs()[
            "Comp"]["FrameFormat"]["Height"]
        height = self.fusion.GetCurrentComp().GetPrefs()[
            "Comp"]["FrameFormat"]["Width"]
        return [width, height]

    @err_catcher(name=__name__)
    def setResolution(self, width=None, height=None):
        self.fusion.GetCurrentComp().SetPrefs(
            {
                "Comp.FrameFormat.Width": width,
                "Comp.FrameFormat.Height": height,
            }
        )

    @err_catcher(name=__name__)
    def updateReadNodes(self):
        updatedNodes = []

        selNodes = self.fusion.GetCurrentComp().GetToolList(True, "Loader")
        if len(selNodes) == 0:
            selNodes = self.fusion.GetCurrentComp().GetToolList(False, "Loader")

        if len(selNodes):
            comp = self.fusion.GetCurrentComp()
            comp.StartUndo("Updating loaders")
            for k in selNodes:
                i = selNodes[k]
                curPath = comp.MapPath(i.GetAttrs()["TOOLST_Clip_Name"][1])

                newPath = self.core.getLatestCompositingVersion(curPath)

                if os.path.exists(os.path.dirname(newPath)) and not curPath.startswith(
                    os.path.dirname(newPath)
                ):
                    firstFrame = i.GetInput("GlobalIn")
                    lastFrame = i.GetInput("GlobalOut")

                    i.Clip = newPath

                    i.GlobalOut = lastFrame
                    i.GlobalIn = firstFrame
                    i.ClipTimeStart = 0
                    i.ClipTimeEnd = lastFrame - firstFrame
                    i.HoldLastFrame = 0

                    updatedNodes.append(i)
            comp.EndUndo(True)

        if len(updatedNodes) == 0:
            QMessageBox.information(
                self.core.messageParent, "Information", "No nodes were updated"
            )
        else:
            mStr = "%s nodes were updated:\n\n" % len(updatedNodes)
            for i in updatedNodes:
                mStr += i.GetAttrs()["TOOLS_Name"] + "\n"

            QMessageBox.information(
                self.core.messageParent, "Information", mStr)

    @err_catcher(name=__name__)
    def getAppVersion(self, origin):
        return self.fusion.Version

    @err_catcher(name=__name__)
    def onProjectBrowserStartup(self, origin):
        origin.actionStateManager.setEnabled(False)

    @err_catcher(name=__name__)
    def openScene(self, origin, filepath, force=False):
        if os.path.splitext(filepath)[1] not in self.sceneFormats:
            return False

        try:
            self.fusion.LoadComp(filepath)
        except:
            pass

        return True

    @err_catcher(name=__name__)
    def correctExt(self, origin, lfilepath):
        return lfilepath

    @err_catcher(name=__name__)
    def setSaveColor(self, origin, btn):
        btn.setPalette(origin.savedPalette)

    @err_catcher(name=__name__)
    def clearSaveColor(self, origin, btn):
        btn.setPalette(origin.oldPalette)

    @err_catcher(name=__name__)
    def importImages(self, origin):
        fString = "Please select an import option:"
        msg = QMessageBox(
            QMessageBox.NoIcon, "Fusion Import", fString, QMessageBox.Cancel
        )
        msg.addButton("Current pass", QMessageBox.YesRole)
        msg.addButton("All passes", QMessageBox.YesRole)
        #   msg.addButton("Layout all passes", QMessageBox.YesRole)
        self.core.parentWindow(msg)
        action = msg.exec_()

        if action == 0:
            self.fusionImportSource(origin)
        elif action == 1:
            self.fusionImportPasses(origin)
        else:
            return

    @err_catcher(name=__name__)
    def fusionImportSource(self, origin):
        self.fusion.GetCurrentComp().Lock()

        sourceData = origin.compGetImportSource()
        for i in sourceData:
            filePath = i[0]
            firstFrame = i[1]
            lastFrame = i[2]

            filePath = filePath.replace(
                "#"*self.core.framePadding, "%04d".replace("4", str(self.core.framePadding)) % firstFrame)

            tool = self.fusion.GetCurrentComp().AddTool("Loader", -32768, -32768)
            tool.Clip = filePath
            tool.GlobalOut = lastFrame
            tool.GlobalIn = firstFrame
            tool.ClipTimeStart = 0
            tool.ClipTimeEnd = lastFrame - firstFrame
            tool.HoldLastFrame = 0

        self.fusion.GetCurrentComp().Unlock()

    @err_catcher(name=__name__)
    def fusionImportPasses(self, origin):
        self.fusion.GetCurrentComp().Lock()

        sourceData = origin.compGetImportPasses()

        for i in sourceData:
            filePath = i[0]
            firstFrame = i[1]
            lastFrame = i[2]

            filePath = filePath.replace(
                "#"*self.core.framePadding, "%04d".replace("4", str(self.core.framePadding)) % firstFrame)

            self.fusion.GetCurrentComp().CurrentFrame.FlowView.Select()
            tool = self.fusion.GetCurrentComp().AddTool("Loader", -32768, -32768)
            tool.Clip = filePath
            tool.GlobalOut = lastFrame
            tool.GlobalIn = firstFrame
            tool.ClipTimeStart = 0
            tool.ClipTimeEnd = lastFrame - firstFrame
            tool.HoldLastFrame = 0

        self.fusion.GetCurrentComp().Unlock()

    @err_catcher(name=__name__)
    def setProject_loading(self, origin):
        pass

    @err_catcher(name=__name__)
    def onPrismSettingsOpen(self, origin):
        pass

    @err_catcher(name=__name__)
    def createProject_startup(self, origin):
        pass

    @err_catcher(name=__name__)
    def editShot_startup(self, origin):
        pass

    @err_catcher(name=__name__)
    def shotgunPublish_startup(self, origin):
        pass

    @err_catcher(name=__name__)
    def getOutputPath(self, node, render=False):
        self.isRendering = [False, ""]

        if node is None:
            msg = QMessageBox(
                QMessageBox.Warning, "Prism Warning", "Please select one or more write nodes you wish to refresh"
            )
            self.core.parentWindow(msg)
            if self.core.useOnTop:
                msg.setWindowFlags(msg.windowFlags() ^ Qt.WindowStaysOnTopHint)
            msg.exec_()
            return ""

        taskName = node.GetInput("PrismTaskControl")
        origComment = node.GetInput("PrismCommentControl")
        if origComment is None:
            comment = ""

        comment = self.core.validateStr(origComment)

        if origComment != comment:
            node.SetInput("PrismCommentControl", comment)

        FormatID = node.GetInput("OutputFormat")
        fileType = ""
        if FormatID == "PIXFormat":
            # Alias PIX
            fileType = "pix"
        elif FormatID == "IFFFormat":
            # Amiga IFF
            fileType = "iff"
        elif FormatID == "CineonFormat":
            # Kodak Cineon
            fileType = "cin"
        elif FormatID == "DPXFormat":
            # DPX
            fileType = "dpx"
        elif FormatID == "FusePicFormat":
            # Fuse Pic
            fileType = "fusepic"
        elif FormatID == "FlipbookFormat":
            # Fusion Flipbooks
            fileType = "fb"
        elif FormatID == "RawFormat":
            # Fusion RAW Image
            fileType = "raw"
        elif FormatID == "IFLFormat":
            # Image File List (Text File)
            fileType = "ifl"
        elif FormatID == "IPLFormat":
            # IPL
            fileType = "ipl"
        elif FormatID == "JpegFormat":
            # JPEG
            fileType = "jpg"
            # fileType = 'jpeg'
        elif FormatID == "Jpeg2000Format":
            # JPEG2000
            fileType = "jp2"
        elif FormatID == "MXFFormat":
            # MXF - Material Exchange Format
            fileType = "mxf"
        elif FormatID == "OpenEXRFormat":
            # OpenEXR
            fileType = "exr"
        elif FormatID == "PandoraFormat":
            # Pandora YUV
            fileType = "piyuv10"
        elif FormatID == "PNGFormat":
            # PNG
            fileType = "png"
        elif FormatID == "VPBFormat":
            # Quantel VPB
            fileType = "vpb"
        elif FormatID == "QuickTimeMovies":
            # QuickTime Movie
            fileType = "mov"
        elif FormatID == "HDRFormat":
            # Radiance
            fileType = "hdr"
        elif FormatID == "SixRNFormat":
            # Rendition
            fileType = "6RN"
        elif FormatID == "SGIFormat":
            # SGI
            fileType = "sgi"
        elif FormatID == "PICFormat":
            # Softimage PIC
            fileType = "si"
        elif FormatID == "SUNFormat":
            # SUN Raster
            fileType = "RAS"
        elif FormatID == "TargaFormat":
            # Targa
            fileType = "tga"
        elif FormatID == "TiffFormat":
            # TIFF
            # fileType = 'tif'
            fileType = "tiff"
        elif FormatID == "rlaFormat":
            # Wavefront RLA
            fileType = "rla"
        elif FormatID == "BMPFormat":
            # Windows BMP
            fileType = "bmp"
        elif FormatID == "YUVFormat":
            # YUV
            fileType = "yuv"
        else:
            # EXR fallback format
            fileType = "exr"

        location = node.GetInput("Location")
        useLastVersion = node.GetInput("RenderLastVersionControl")

        if taskName is None or taskName == "":
            msg = QMessageBox(
                QMessageBox.Warning, "Prism Warning", "Please choose a taskname"
            )
            self.core.parentWindow(msg)
            if self.core.useOnTop:
                msg.setWindowFlags(msg.windowFlags() ^ Qt.WindowStaysOnTopHint)
            msg.exec_()
            return ""

        if useLastVersion:
            msg = QMessageBox(
                QMessageBox.Warning,
                "Prism Warning",
                '"Render as previous version" is enabled.\nThis may overwrite existing files.',
            )
            self.core.parentWindow(msg)
            msg.exec_()

        outputName = self.core.getCompositingOut(
            taskName,
            fileType,
            useLastVersion,
            render,
            location,
            comment,
            ignoreEmpty=True,
        ).replace("####", "")

        node.Clip[self.fusion.TIME_UNDEFINED] = outputName
        node.FilePathControl = outputName

        return outputName

    @err_catcher(name=__name__)
    def startRender(self, node):
        fileName = self.getOutputPath(node, render=True)

        if fileName == "FileNotInPipeline":
            QMessageBox.warning(
                self.core.messageParent,
                "Prism Warning",
                "The current file is not inside the Pipeline.\nUse the Project Browser to create a file in the Pipeline.",
            )
            return

        self.core.saveScene(versionUp=False)

    @err_catcher(name=__name__)
    def updateNodeUI(self, nodeType, node):
        if nodeType == "writePrism":
            locations = self.core.paths.getRenderProductBasePaths()
            locNames = list(locations.keys())

            # As copySettings and loadSettings doesn't work with python we'll have to execute them as Lua code
            luacode = ' \
            local tool = comp.ActiveTool  \
            local ctrls = tool.UserControls  \
            local settings = comp:CopySettings(tool)  \
  \
            comp:Lock()  \
  \
            ctrls.Location = {'

            for location in locNames:
                luacode = luacode + \
                    '{CCS_AddString = "' + str(location) + '"},\n \
                     {CCID_AddID = "' + str(location) + '"},\n'

            luacode = luacode + ' \
            ICD_Width = 0.7,  \
            INP_Integer = false,  \
            INP_External = false,  \
            LINKID_DataType = "FuID",  \
            ICS_ControlPage = "File",  \
            CC_LabelPosition = "Horizontal",  \
            INPID_InputControl = "ComboIDControl",  \
            LINKS_Name = "Location",  \
        }  \
 \
            tool.UserControls = ctrls \
            tool:LoadSettings(settings) \
            refresh = tool:Refresh() \
            comp:Unlock() \
            '

            comp = self.fusion.GetCurrentComp()
            comp.Execute(luacode)

################################################
#                                              #
#                    EXPORT                    #
#                                              #
################################################

    @err_catcher(name=__name__)
    def getNodeName(self, origin, node):
        if self.isNodeValid(origin, node):
            try:
                return node["name"]
            except:
                QMessageBox.warning(
                    self.core.messageParent, "Warning", "Cannot get name from %s" % node
                )
                return node
        else:
            return "invalid"

    @err_catcher(name=__name__)
    def selectNodes(self, origin):
        if origin.lw_objects.selectedItems() != []:
            nodes = []
            for i in origin.lw_objects.selectedItems():
                node = origin.nodes[origin.lw_objects.row(i)]
                if self.isNodeValid(origin, node):
                    nodes.append(node)
           

    @err_catcher(name=__name__)
    def isNodeValid(self, origin, handle):
        #Validar que los nodos que seleccionemos sean objetos exportables
        #print(origin.className)
        if origin.className == "Export":
            obj = self.getObject(handle)
            return obj.ID == "Merge3D"
        elif origin.className == "ImportFile":
            #print("Importando")
            return True
    
    @err_catcher(name=__name__)
    def sm_export_exportShotcam(self, origin, startFrame, endFrame, outputName):
        result = self.sm_export_exportAppObjects(
            origin,
            startFrame,
            endFrame,
            (outputName + ".abc"),
            nodes=[origin.curCam],
            expType=".abc",
        )
        result = self.sm_export_exportAppObjects(
            origin,
            startFrame,
            endFrame,
            (outputName + ".fbx"),
            nodes=[origin.curCam],
            expType=".fbx",
        )
        return result

    @err_catcher(name=__name__)
    def sm_export_exportAppObjects(
        self,
        origin,
        startFrame,
        endFrame,
        outputName,
        scaledExport=False,
        nodes=None,
        expType=None,
    ):
        comp = self.fusion.GetCurrentComp()
        #Tomemos los nodos que están en la lista
        expNodes = origin.nodes
        
        #Seleccionemos los nodos elegidos en la lista
        #recordemos que en la lista hay guardados definiciones de nodos de Fusion.
        #loopeamos por todos los nodos seleccionados
        for i in expNodes:            
            #chequemos cual es el formato de salida
            outType = origin.getOutputType()

            #Manejamos el export de acuerdo a el formato de salida.
            if outType == ".fbx":
                #Checamos si hay que bakear anim (para FBX no es necesario)
                useAnim = startFrame != endFrame
                #bloqueamos la comp para que no salgan ventanas emergentes
                comp.Lock()

                #toolName = i.Name
                #El node guardado en el stateManager tiene el formato {name: "nombre"} getObject nos da el objeto
                activeNode = self.getObject(i)
                flow = comp.CurrentFrame.FlowView
                #Tiene un objeto asignado a ActiveNode o no
                if activeNode:                    
                    #por cada nodo extraemos su posición
                    x, y = flow.GetPosTable(activeNode).values()                    
                    #creamos el FBXExport en la posición correspondiente.
                    exporter = comp.AddTool("ExporterFBX",x+2,y-1)

                    exporter.Filename = outputName
                    #exporter.ScaleFusionUnitsBy = 10.0

                    exporter.Input.ConnectTo(activeNode.Output)
                    comp.Render({'Tool':exporter, 'Start':startFrame, 'End':endFrame, 'Wait':True})
                    interval = 3
                    time.sleep(interval)
                    exporter.Delete()
                else:
                    #ThrowError
                    pass
                #Desbloqueamos la comp.
                comp.Unlock()
        
        #Seleccionar los FBX nodes

        #Retornar el nombre de archivo.
        #Si el nombre es outputName = "Canceled" default export cancela la operacion y arroja error.
        return outputName

    @err_catcher(name=__name__)
    def sm_export_preDelete(self, origin):
        pass

    @err_catcher(name=__name__)
    def sm_export_startup(self, origin):
        if origin.className == "Export":
            #print(dir(origin))
            #origin.l_convertExport.setText("Additional export in centimeters:")
            #origin.chb_convertExport.deleteLater()
            origin.chb_convertExport.setVisible(False)
            origin.chb_wholeScene.setVisible(False)
            origin.l_convertExport.setVisible(False)
            origin.w_additionalOptions.setVisible(False)

    #########################################################################
    #########################################################################

    @err_catcher(name=__name__)
    def updateList(self, origin):
        comp = self.fusion.GetCurrentComp()
        nodes = origin.nodes
        origin.nodes = []
        isobjactive = True
        try:
            actobj = comp.ActiveTool()
        except Exception:
            actobj = None
        if actobj:
            #print(len(nodes))
            if len(nodes) > 0:
                if actobj.Name != nodes[0]["name"]:
                    nodes = [self.getNode(actobj)]
            else:
                nodes = [self.getNode(actobj)]
        else:
            isobjactive = False

        origin.nodes = nodes
        return isobjactive

    @err_catcher(name=__name__)
    def sm_export_updateObjects(self, origin):
        #comp = self.fusion.GetCurrentComp()
        #nodes = origin.nodes
        #nodesnames = [n["name"] for n in nodes]
        #print(nodesnames)
        #origin.nodes = []
        #objects = list(comp.GetToolList(True).values())

        #for i in nodes:
        #    if i["name"] not in nodesnames:
        #        print("Soy")
        #        print(i["name"])
        #        nodes.append(self.getNode(i["name"]))
        #        nodesnames.append(i["name"])
        #for i in objects:
        #    if i["name"] not in nodesnames:
        #        nodes.append(self.getNode(i))
        #print(nodesnames)

        #Cada Export debería ser un sólo nodo
        self.updateList(origin)

    @err_catcher(name=__name__)
    def getCamNodes(self, origin, cur=False):
        comp = self.fusion.GetCurrentComp()
        return [x.Name for x in comp.GetToolList().values() if x.ID == "Camera3D"]
    
    @err_catcher(name=__name__)
    def getCamName(self, origin, handle):
        return handle

    @err_catcher(name=__name__)
    def sm_export_addObjects(self, origin, objects=None):
        #print("sm_export_addObjects")
        #comp = self.fusion.GetCurrentComp()
        #nodes = origin.nodes
        #nodesnames = [n["name"] for n in nodes]

        #si objects no es None (no es falso)
        #if not objects:
            # get selected objects from scene
        #    objects = list(comp.GetToolList(True).values())
        #for i in objects:
        #    if i.Name not in nodesnames:
        #        origin.nodes.append(self.getNode(i))

        gate = self.updateList(origin)                
        if not gate:
            QMessageBox.warning(
                self.core.messageParent, 
                "Warning", 
                "No hay nodos activos en la comp \n Selecciona un nodo y asegurate que este activo",
            )

        origin.updateUi()
        origin.stateManager.saveStatesToScene()

    
    @err_catcher(name=__name__)
    def sm_export_preExecute(self, origin, startFrame, endFrame):
        warnings = []

        outType = origin.getOutputType()

        if outType != "ShotCam":
            if (
                outType == ".Comp"
            ):
                warnings.append(
                    [
                        "El Export de .Comp files aún no está implementado",
                        "Copia y pega los nodos deseados como de costumbre.",
                    ]
                )

        return warnings

    @err_catcher(name=__name__)
    def clearActiveTool(self):
        comp = self.fusion.GetCurrentComp()
        comp.SetActiveTool(None)

    @err_catcher(name=__name__)
    def sm_export_removeSetItem(self, origin, node):
        self.clearActiveTool()

    @err_catcher(name=__name__)
    def sm_export_clearSet(self, origin):
        self.clearActiveTool()

    ################################################
    #                                              #
    #                    IMPORT                    #
    #                                              #
    ################################################
    abc_options = {
        "Points": True,
        "Transforms": True,
        "Hierarchy": False,
        "Lights": True,
        "Normals": True,
        "Meshes": True,
        "UVs": True,
        "Cameras": True,
        "InvCameras": True
        # "SamplingRate": 24
    }

    @err_catcher(name=__name__)
    def importFormatByUI(self, origin, formatCall, filepath, global_scale, options = None, interval = 1):
        #sys.path.append(self.core.prismRoot+"\\PythonLibs\\Python27\\")
        print("PrismRoot= "+ self.core.prismRoot)
        origin.stateManager.showMinimized()
        sys.path.append(self.core.prismRoot + '/PythonLibs/Python27')
        import pyautogui

        fusion = self.fusion
        comp = fusion.CurrentComp
        #comp.Lock()
        flow = comp.CurrentFrame.FlowView
        flow.Select(None)

        if not os.path.exists(filepath):
            QMessageBox.warning(
                self.core.messageParent, "Warning", "File %s does not exists" % filepath
            )

        if formatCall == "AbcImport" and isinstance(options, dict):
            current = fusion.GetPrefs("Global.Alembic.Import")
            new = current.copy()
            for key, value in options.items():
                if key in current:
                    new[key] = value
                else:
                    print("Invalid option %s:" % key)
            fusion.SetPrefs("Global.Alembic.Import", new)

        fusion.QueueAction("Utility_Show", {"id":formatCall})


        pyautogui.typewrite(filepath)
        pyautogui.press("enter")
        pyautogui.press("enter")
        time.sleep(interval)

        origin.stateManager.showNormal()
        #comp.Unlock()

        #return comp.GetToolList(True).values()

    @err_catcher(name=__name__)
    def sm_import_startup(self, origin):
        origin.b_browse.setMinimumWidth(50 * self.core.uiScaleFactor)
        origin.b_browse.setMaximumWidth(50 * self.core.uiScaleFactor)
        origin.f_abcPath.setVisible(False)
        origin.f_unitConversion.setVisible(False)
        origin.l_preferUnit.setText("Prefer versions in cm:")

    @err_catcher(name=__name__)
    def sm_import_disableObjectTracking(self, origin):
        self.deleteNodes(origin, [origin.setName])

    @err_catcher(name=__name__)
    def sm_import_importToApp(self, origin, doImport, update, impFileName):
        #print(impFileName)
        comp = self.fusion.GetCurrentComp()
        flow = comp.CurrentFrame.FlowView
        #default_importfile.py llama a ésta función pasándole el nombre del archivo a importar
        fileName = os.path.splitext(os.path.basename(impFileName))
        origin.setName = ""
        result = False
        activetool = None
        try:
            activetool = comp.ActiveTool()
        except:
            pass
        
        ext = fileName[1].lower()
        #Si el formato no es un formato reconocible entonces no es importable
        if ext not in [".fbx",".abc"]:
            self.core.popup("Format is not supported.")
            return {"result": False, "doImport": doImport}
        #se refiere a chbx al lado de:Update path only (if exists)
        # if not (ext == ".abc" and origin.chb_abcPath.isChecked()):
        #     origin.preDelete(
        #         baseText="Do you want to delete the currently connected objects?\n\n"
        #     )

        #Vamos a agarrar todos los nodos de la escena a ver si hay que reemplazar alguno        
        existingNodes = [n.Name for n in comp.GetToolList().values()]
        if ext == ".fbx":
            self.importFormatByUI(origin = origin, formatCall="FBXImport", filepath=impFileName,global_scale=100)
        elif ext == ".abc":
            self.importFormatByUI(origin = origin, formatCall="AbcImport", filepath=impFileName,global_scale=100, options = self.abc_options)

        #Agarramos los nodos importados y los hacemos relativos al active node.
        if activetool is not None:
            print("locs")
            impnodes = [n for n in comp.GetToolList(True).values()]
            print(impnodes)
            if len(impnodes) > 0:
                comp.Lock()
                fisrtnode = impnodes[0]
                fstnx = flow.GetPosTable(fisrtnode).values()[0]
                fstny = flow.GetPosTable(fisrtnode).values()[1]
                for n in impnodes:
                    print("locs")
                    atx = flow.GetPosTable(activetool).values()[0]
                    aty = flow.GetPosTable(activetool).values()[1]
                    x = flow.GetPosTable(n).values()[0]
                    y = flow.GetPosTable(n).values()[1]
                    offset = [x-fstnx,y-fstny]
                    newx = x+(atx-x)+offset[0]
                    newy = y+(aty-y)+offset[1]
                    flow.SetPos(n, newx, newy)
                comp.Unlock()

        #vemos si hay que reemplazar nodos en la comp
        newNodes = [n.Name for n in comp.GetToolList(True).values()]
        importedNodes = []
        for i in newNodes:
            #si tiene el patrón de un nodo duplicado reemplazamos el nodo anterior
            #if i.endswith("_1"):
            # if i[-1].isdigit(): 
            #     digit = int(i[-1]) - 1
            #     if digit > 0:
            #         tmpname = i[:-1] + str(digit)
            #         if tmpname in existingNodes:
            #             oldnode = comp.FindTool(tmpname)
            #             newnode = comp.FindTool(i)
            #             x = flow.GetPosTable(oldnode).values()[0]
            #             y = flow.GetPosTable(oldnode).values()[1]

            #             flow.SetPos(newnode, x, y)
            #             oldnode.Delete()
            #             newnode.Name = tmpname 
            #             importedNodes.append(self.getNode(tmpname))
            #         else:
            #             importedNodes.append(self.getNode(i))
            # else:
            #     importedNodes.append(self.getNode(i))
            importedNodes.append(self.getNode(i))

        origin.setName = "Import_" + fileName[0]
        # extension = 1
        # while origin.setName in self.getGroups() and extension < 999:
        #     if "%s_%s" % (origin.setName, extension) not in self.getGroups():
        #         origin.setName += "_%s" % extension
        #     extension += 1

        #if origin.chb_trackObjects.isChecked():
        origin.nodes = importedNodes
        #Deseleccionar todo
        flow.Select()

        objs = [self.getObject(x) for x in importedNodes]

        for o in objs:
            flow.Select(o)

        result = len(importedNodes) > 0
        print(importedNodes)
        return {"result": result, "doImport": doImport}
        

    # @err_catcher(name=__name__)
    # def sm_import_updateObjects(self, origin):
    #     if origin.setName == "":
    #         return

    #     origin.nodes = []
    #     if origin.setName in self.getGroups() and origin.chb_trackObjects.isChecked():
    #         group = self.getGroups()[origin.setName]
    #         nodes = []
    #         for obj in group.objects:
    #             if not obj.users_scene:
    #                 group.objects.unlink(obj)
    #                 continue

    #             nodes.append(self.getNode(obj))

    #         origin.nodes = nodes

    @err_catcher(name=__name__)
    def sm_import_removeNameSpaces(self, origin):
        for i in origin.nodes:
            if not self.getObject(i):
                continue

            nodeName = self.getNodeName(origin, i)
            newName = nodeName.rsplit(":", 1)[-1]
            if newName != nodeName and not i["library"]:
                self.getObject(i).name = newName

        origin.updateUi()

    # @err_catcher(name=__name__)
    # def sm_import_unitConvert(self, origin):
    #     if origin.taskName == "ShotCam" and len(origin.nodes) == 1:
    #         prevObjs = list(bpy.context.scene.objects)
    #         bpy.ops.object.empty_add(type="PLAIN_AXES")
    #         empObj = [x for x in bpy.context.scene.objects if x not in prevObjs][0]
    #         empObj.name = "UnitConversion"
    #         empObj.location = [0, 0, 0]

    #         self.getObject(origin.nodes[0]).parent = empObj
    #         sVal = 0.01
    #         empObj.scale = [sVal, sVal, sVal]

    #         bpy.ops.object.select_all(
    #             self.getOverrideContext(origin), action="DESELECT"
    #         )
    #         self.selectObject(self.getObject(origin.nodes[0]))
    #         bpy.ops.object.parent_clear(
    #             self.getOverrideContext(origin), type="CLEAR_KEEP_TRANSFORM"
    #         )

    #         bpy.ops.object.select_all(
    #             self.getOverrideContext(origin), action="DESELECT"
    #         )
    #         self.selectObject(empObj)
    #         bpy.ops.object.delete(self.getOverrideContext(origin))

    @err_catcher(name=__name__)
    def sm_import_fixImportPath(self, filepath):
        return filepath.replace("\\\\", "\\")

    @err_catcher(name=__name__)
    def sm_import_updateUi(self, origin):
        origin.f_unitConversion.setVisible(origin.taskName == "ShotCam")

    ##Dentro de Fusion necesitamos trabajar con objetos,
    ##Pero Prisma necesita data más genérica como Strings o diccionarios 
    ##para guardarlas en la data del state manager como "connectednodes"
    #Estas dos funciones convierten data de prisma a objetos de Fusion. 

    @err_catcher(name=__name__)
    def getNode(self, obj):
        if type(obj) == str:
            node = {"name": obj}
        elif type(obj) == dict:
            node = {"name": obj["name"]}
        else:
            node = {"name": obj.Name}
        return node

    @err_catcher(name=__name__)
    def getObject(self, node):
        comp = self.fusion.GetCurrentComp()
        if type(node) == str:
            node = self.getNode(node)

        return comp.FindTool(node["name"])

    #######################################################################

    ###STATE MANAGER STUFF####
    
    @err_catcher(name=__name__)
    def sm_getExternalFiles(self, origin):
        extFiles = []
        return [extFiles, []]

    @err_catcher(name=__name__)
    def getFusionStatesFilePath(self):
        comp = self.fusion.GetCurrentComp()
        file_name = 'PrismStates.txt'        
        #file_name = 'PrismStates.json'
        file_path = comp.GetAttrs()["COMPS_FileName"]
        abs_path = os.path.abspath(file_path)
        file_dir = os.path.dirname(abs_path)
        newfile_path = os.path.join(file_dir,file_name)

        return newfile_path

    @err_catcher(name=__name__)
    def sm_saveStates(self, origin, buf):
        prismstates = self.getFusionStatesFilePath()
        
        file_dir = os.path.dirname(prismstates)
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        with open(prismstates, "w") as file:
            #json.dump(buf, file)
            file.write(buf)

    @err_catcher(name=__name__)
    def sm_saveImports(self, origin, importPaths):
        #bpy.context.scene["PrismImports"] = importPaths.replace("\\\\", "\\")
        pass

    @err_catcher(name=__name__)
    def sm_readStates(self, origin):
        prismstates = self.getFusionStatesFilePath()
        
        if os.path.exists(prismstates):
            with open(prismstates, "r") as file:
                file_contents = str(file.read())
                #print(file_contents)
                return file_contents
                #return json.load(file)

    @err_catcher(name=__name__)
    def sm_deleteStates(self, origin):
        prismstates = self.getFusionStatesFilePath()
        if os.path.exists(prismstates):
                os.remove(prismstates)