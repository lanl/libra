# state file generated using paraview version 5.12.0
import paraview
import sys

# ----------------------------------------------------------------
# total arguments
n = len(sys.argv)
if n < 3:
    print("Not enough arguments")
    exit(0)

input_file = sys.argv[1]
output_file = sys.argv[2]
# ----------------------------------------------------------------

paraview.compatibility.major = 5
paraview.compatibility.minor = 12

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# ----------------------------------------------------------------
# setup views used in the visualization
# ----------------------------------------------------------------

# get the material library
materialLibrary1 = GetMaterialLibrary()

# Create a new 'Render View'
renderView1 = CreateView('RenderView')
renderView1.ViewSize = [1530, 1148]
renderView1.AxesGrid = 'Grid Axes 3D Actor'
renderView1.CenterOfRotation = [256.0, 256.0, 256.0]
renderView1.StereoType = 'Crystal Eyes'
renderView1.CameraPosition = [927.3917601880481, -841.4384129647123, 847.1897933640862]
renderView1.CameraFocalPoint = [255.9999999999999, 255.9999999999999, 255.9999999999999]
renderView1.CameraViewUp = [-0.22986936132331293, 0.34881369227665393, 0.9085642986630831]
renderView1.CameraFocalDisk = 1.0
renderView1.CameraParallelScale = 443.4045633326258
renderView1.LegendGrid = 'Legend Grid Actor'
renderView1.UseColorPaletteForBackground = 0
renderView1.Background = [0.0, 0.0, 0.0]
renderView1.BackEnd = 'OSPRay raycaster'
renderView1.OSPRayMaterialLibrary = materialLibrary1

SetActiveView(None)

# ----------------------------------------------------------------
# setup view layouts
# ----------------------------------------------------------------

# create new layout object 'Layout #1'
layout1 = CreateLayout(name='Layout #1')
layout1.AssignView(0, renderView1)
layout1.SetSize(1530, 1148)

# ----------------------------------------------------------------
# restore active view
SetActiveView(renderView1)
# ----------------------------------------------------------------

# ----------------------------------------------------------------
# setup the data processing pipelines
# ----------------------------------------------------------------

# create a new 'VisIt Pixie Reader'
nyx_dataset = VisItPixieReader(registrationName='nyx_dataset', FileName=input_file)
nyx_dataset.Meshes = ['mesh_512x512x512']
nyx_dataset.CellArrays = ['native_fields/baryon_density']

# create a new 'Resample To Image'
resampleToImage1 = ResampleToImage(registrationName='ResampleToImage1', Input=nyx_dataset)
resampleToImage1.SamplingDimensions = [512, 512, 512]
resampleToImage1.SamplingBounds = [0.0, 512.0, 0.0, 512.0, 0.0, 512.0]

# ----------------------------------------------------------------
# setup the visualization in view 'renderView1'
# ----------------------------------------------------------------

# show data from resampleToImage1
resampleToImage1Display = Show(resampleToImage1, renderView1, 'UniformGridRepresentation')

# get 2D transfer function for 'native_fieldsbaryon_density'
native_fieldsbaryon_densityTF2D = GetTransferFunction2D('native_fieldsbaryon_density')
native_fieldsbaryon_densityTF2D.ScalarRangeInitialized = 1
native_fieldsbaryon_densityTF2D.Range = [0.04938583821058273, 500.0, 0.0, 1.0]

# get color transfer function/color map for 'native_fieldsbaryon_density'
native_fieldsbaryon_densityLUT = GetColorTransferFunction('native_fieldsbaryon_density')
native_fieldsbaryon_densityLUT.TransferFunction2D = native_fieldsbaryon_densityTF2D
native_fieldsbaryon_densityLUT.RGBPoints = [0.04938583821058273, 0.278431372549, 0.278431372549, 0.858823529412, 71.54232366334647, 0.0, 0.0, 0.360784313725, 142.53531087432054, 0.0, 1.0, 1.0, 214.52819931361825, 0.0, 0.501960784314, 0.0, 285.52118652459234, 1.0, 1.0, 0.0, 357.0141243497282, 1.0, 0.380392156863, 0.0, 428.50706217486413, 0.419607843137, 0.0, 0.0, 500.0, 0.878431372549, 0.301960784314, 0.301960784314]
native_fieldsbaryon_densityLUT.ColorSpace = 'RGB'
native_fieldsbaryon_densityLUT.ScalarRangeInitialized = 1.0

# get opacity transfer function/opacity map for 'native_fieldsbaryon_density'
native_fieldsbaryon_densityPWF = GetOpacityTransferFunction('native_fieldsbaryon_density')
native_fieldsbaryon_densityPWF.Points = [0.04938583821058273, 0.0, 0.5, 0.0, 15.45070743560791, 0.9955357313156128, 0.5, 0.0, 500.0, 1.0, 0.5, 0.0]
native_fieldsbaryon_densityPWF.ScalarRangeInitialized = 1

# trace defaults for the display properties.
resampleToImage1Display.Representation = 'Volume'
resampleToImage1Display.ColorArrayName = ['POINTS', 'native_fields/baryon_density']
resampleToImage1Display.LookupTable = native_fieldsbaryon_densityLUT
resampleToImage1Display.SelectTCoordArray = 'None'
resampleToImage1Display.SelectNormalArray = 'None'
resampleToImage1Display.SelectTangentArray = 'None'
resampleToImage1Display.OSPRayScaleArray = 'native_fields/baryon_density'
resampleToImage1Display.OSPRayScaleFunction = 'Piecewise Function'
resampleToImage1Display.Assembly = ''
resampleToImage1Display.SelectOrientationVectors = 'None'
resampleToImage1Display.ScaleFactor = 51.199948799999994
resampleToImage1Display.SelectScaleArray = 'None'
resampleToImage1Display.GlyphType = 'Arrow'
resampleToImage1Display.GlyphTableIndexArray = 'None'
resampleToImage1Display.GaussianRadius = 2.5599974399999996
resampleToImage1Display.SetScaleArray = ['POINTS', 'native_fields/baryon_density']
resampleToImage1Display.ScaleTransferFunction = 'Piecewise Function'
resampleToImage1Display.OpacityArray = ['POINTS', 'native_fields/baryon_density']
resampleToImage1Display.OpacityTransferFunction = 'Piecewise Function'
resampleToImage1Display.DataAxesGrid = 'Grid Axes Representation'
resampleToImage1Display.PolarAxes = 'Polar Axes Representation'
resampleToImage1Display.ScalarOpacityUnitDistance = 1.7354386040415881
resampleToImage1Display.ScalarOpacityFunction = native_fieldsbaryon_densityPWF
resampleToImage1Display.TransferFunction2D = native_fieldsbaryon_densityTF2D
resampleToImage1Display.OpacityArrayName = ['POINTS', 'native_fields/baryon_density']
resampleToImage1Display.ColorArray2Name = ['POINTS', 'native_fields/baryon_density']
resampleToImage1Display.Shade = 1
resampleToImage1Display.SliceFunction = 'Plane'
resampleToImage1Display.Slice = 255
resampleToImage1Display.SelectInputVectors = [None, '']
resampleToImage1Display.WriteLog = ''

# init the 'Piecewise Function' selected for 'ScaleTransferFunction'
resampleToImage1Display.ScaleTransferFunction.Points = [0.04938583821058273, 0.0, 0.5, 0.0, 71011.75, 1.0, 0.5, 0.0]

# init the 'Piecewise Function' selected for 'OpacityTransferFunction'
resampleToImage1Display.OpacityTransferFunction.Points = [0.04938583821058273, 0.0, 0.5, 0.0, 71011.75, 1.0, 0.5, 0.0]

# init the 'Plane' selected for 'SliceFunction'
resampleToImage1Display.SliceFunction.Origin = [256.0, 256.0, 256.0]

# setup the color legend parameters for each legend in this view

# get color legend/bar for native_fieldsbaryon_densityLUT in view renderView1
native_fieldsbaryon_densityLUTColorBar = GetScalarBar(native_fieldsbaryon_densityLUT, renderView1)
native_fieldsbaryon_densityLUTColorBar.Title = 'native_fields/baryon_density'
native_fieldsbaryon_densityLUTColorBar.ComponentTitle = ''

# set color bar visibility
native_fieldsbaryon_densityLUTColorBar.Visibility = 1

# show color legend
resampleToImage1Display.SetScalarBarVisibility(renderView1, True)

# ----------------------------------------------------------------
# setup color maps and opacity maps used in the visualization
# note: the Get..() functions create a new object, if needed
# ----------------------------------------------------------------

# ----------------------------------------------------------------
# setup animation scene, tracks and keyframes
# note: the Get..() functions create a new object, if needed
# ----------------------------------------------------------------

# get time animation track
timeAnimationCue1 = GetTimeTrack()

# initialize the animation scene

# get the time-keeper
timeKeeper1 = GetTimeKeeper()

# initialize the timekeeper

# initialize the animation track

# get animation scene
animationScene1 = GetAnimationScene()

# initialize the animation scene
animationScene1.ViewModules = renderView1
animationScene1.Cues = timeAnimationCue1
animationScene1.AnimationTime = 0.0

# ----------------------------------------------------------------
# restore active source
SetActiveSource(resampleToImage1)
# ----------------------------------------------------------------
SaveScreenshot(output_file, renderView1)

##--------------------------------------------
## You may need to add some code at the end of this python script depending on your usage, eg:
#
## Render all views to see them appears
# RenderAllViews()
#
## Interact with the view, usefull when running from pvpython
# Interact()
#
## Save a screenshot of the active view
# SaveScreenshot("path/to/screenshot.png")
#
## Save a screenshot of a layout (multiple splitted view)
# SaveScreenshot("path/to/screenshot.png", GetLayout())
#
## Save all "Extractors" from the pipeline browser
# SaveExtracts()
#
## Save a animation of the current active view
# SaveAnimation()
#
## Please refer to the documentation of paraview.simple
## https://kitware.github.io/paraview-docs/latest/python/paraview.simple.html
##--------------------------------------------
