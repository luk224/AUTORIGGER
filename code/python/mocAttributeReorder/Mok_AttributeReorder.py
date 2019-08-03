# ######### Mok_AttributeReorder v1.0 ##########
#
# Description: Script For reorder Attributes in channelbox and Attribute Editor/Extra attributes
#
# 
# Intallation: 
#		place files in yourdocument\maya\2012\scripts
#
# How to use:   
#		 import Mok_AttributeReorder
#		 Mok_AttributeReorder.UI()
#
# Author: PERIN Morgan
#	  scudyreal@gmail.com

import maya.mel as mel
import os

adresse = os.path.split(__file__)[0]


def UI():

	mel.eval(""" global proc Mok_AttributeReorderUI(){float $mayaVersion = `getApplicationVersionAsFloat` ;string $fileAddress = " """+adresse+""" ";$fileAddress = strip($fileAddress);string $LayoutName = "Win_Mok_AttrReorder";if (`formLayout -ex $LayoutName`){deleteUI -lay $LayoutName;}string $Objs[] = `channelBox -q -mol mainChannelBox`;string $Attrs[] = {};if (size($Objs) > 0) $Attrs = `listAttr -ud $Objs[0]` ;string $NameLayout = "ChannelsLayersPaneLayout";if (`paneLayout -q -cn $NameLayout` == "horizontal2") { paneLayout -e -cn "horizontal3" $NameLayout; paneLayout -e -setPane "LayerEditorForm" 3 $NameLayout;}formLayout -numberOfDivisions 100 -p "ChannelsLayersPaneLayout" $LayoutName;string $b1 = `button -w 100 -h 20 -l " Check " -c ("Mok_AttributeReorderCheck")`;string $b2 = `button -w 100 -h 20 -l " Reorder " -c ("Mok_AttributeReorder")`;string $b3 = `button -w 20 -h 20 -l "X" -c ("Mok_AttributeReorderUI_Delete " + $LayoutName)`;string $Scroll = `loadUI -uiFile ($fileAddress+"\/Mok_AttributeReorderUI.ui")`;showWindow $Scroll;window -e -vis 0 -wh 10 10 -tlc 0 0 $Scroll;textScrollList -e -p "Win_Mok_AttrReorder" ScrollListAttrReor;deleteUI -wnd $Scroll;for ($Attr in $Attrs){ textScrollList -edit -append $Attr ScrollListAttrReor;	}formLayout -edit -attachForm     $b1     "top"    5 -attachForm     $b1     "left"   5 -attachControl  $b2 	"left"   5 $b1 -attachControl  $b2 	"right"  5 $b3 -attachForm     $b2     "top"    5 -attachForm     $b3 	"right"  5 -attachForm     $b3     "top"    5 -attachControl ScrollListAttrReor "top" 5 $b1 -attachForm ScrollListAttrReor "left" 5 -attachForm ScrollListAttrReor "right" 5 -attachForm ScrollListAttrReor "bottom" 5 $LayoutName;}global proc Mok_AttributeReorderCheck(){string $Objs[] = `channelBox -q -mol mainChannelBox`;string $Attrs[] = {};if (size($Objs) > 0) $Attrs = `listAttr -ud $Objs[0]` ;textScrollList -e -ra ScrollListAttrReor;for ($Attr in $Attrs){ textScrollList -edit -append $Attr ScrollListAttrReor;}}global proc Mok_AttributeReorderUI_Delete(string $Layout){ deleteUI -lay $Layout; paneLayout -e -setPane "LayerEditorForm" 2 "ChannelsLayersPaneLayout"; paneLayout -e -cn "horizontal2" "ChannelsLayersPaneLayout";}global proc Mok_AttributeReorder(){string $Objs[] = `channelBox -q -mol mainChannelBox`;string $Attrs[] = `textScrollList -q -ai ScrollListAttrReor`;for ($obj in $Objs){for ($attr in $Attrs){ if (`attributeExists $attr $obj`) { if (`getAttr -lock ($obj+"."+$attr)`){setAttr -lock 0 ($obj+"."+$attr);catch (`deleteAttr -attribute $attr $obj`);undo;setAttr -lock 1 ($obj+"."+$attr);}else{catch (`deleteAttr -attribute $attr $obj`);undo; }}}}refreshEditorTemplates;}Mok_AttributeReorderUI; """)