import os
import paraview
from paraview.simple import *

paraview.compatibility.major = 5
paraview.compatibility.minor = 12

#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# Define the list of file names
file_names = [
    "/Users/yetchi/Desktop/vizStudy/project_libra/libra/eval/data/decompressed_30.raw",
    '/Users/yetchi/Desktop/vizStudy/project_libra/libra/eval/data/decompressed_31.raw',
    '/Users/yetchi/Desktop/vizStudy/project_libra/libra/eval/data/decompressed_32.raw',
    '/Users/yetchi/Desktop/vizStudy/project_libra/libra/eval/data/decompressed_33.raw',
    '/Users/yetchi/Desktop/vizStudy/project_libra/libra/eval/data/decompressed_34.raw',
    '/Users/yetchi/Desktop/vizStudy/project_libra/libra/eval/data/decompressed_35.raw',
    '/Users/yetchi/Desktop/vizStudy/project_libra/libra/eval/data/decompressed_36.raw',
    '/Users/yetchi/Desktop/vizStudy/project_libra/libra/eval/data/decompressed_37.raw',
    '/Users/yetchi/Desktop/vizStudy/project_libra/libra/eval/data/decompressed_38.raw',
    '/Users/yetchi/Desktop/vizStudy/project_libra/libra/eval/data/decompressed_39.raw',
    '/Users/yetchi/Desktop/vizStudy/project_libra/libra/eval/data/decompressed_40.raw',
    '/Users/yetchi/Desktop/vizStudy/project_libra/libra/eval/data/decompressed_41.raw',
    '/Users/yetchi/Desktop/vizStudy/project_libra/libra/eval/data/decompressed_42.raw',
    '/Users/yetchi/Desktop/vizStudy/project_libra/libra/eval/data/decompressed_43.raw',
    '/Users/yetchi/Desktop/vizStudy/project_libra/libra/eval/data/decompressed_44.raw',
    '/Users/yetchi/Desktop/vizStudy/project_libra/libra/eval/data/decompressed_45.raw',
    '/Users/yetchi/Desktop/vizStudy/project_libra/libra/eval/data/decompressed_46.raw',
    '/Users/yetchi/Desktop/vizStudy/project_libra/libra/eval/data/decompressed_47.raw',
    '/Users/yetchi/Desktop/vizStudy/project_libra/libra/eval/data/decompressed_48.raw',
    '/Users/yetchi/Desktop/vizStudy/project_libra/libra/eval/data/decompressed_49.raw',
    '/Users/yetchi/Desktop/vizStudy/project_libra/libra/eval/data/decompressed_50.raw',
    '/Users/yetchi/Desktop/vizStudy/project_libra/libra/eval/data/decompressed_51.raw',
    '/Users/yetchi/Desktop/vizStudy/project_libra/libra/eval/data/decompressed_52.raw',
    '/Users/yetchi/Desktop/vizStudy/project_libra/libra/eval/data/decompressed_53.raw',
    '/Users/yetchi/Desktop/vizStudy/project_libra/libra/eval/data/decompressed_54.raw',
    '/Users/yetchi/Desktop/vizStudy/project_libra/libra/eval/data/decompressed_55.raw',
    '/Users/yetchi/Desktop/vizStudy/project_libra/libra/eval/data/decompressed_56.raw',
    '/Users/yetchi/Desktop/vizStudy/project_libra/libra/eval/data/decompressed_57.raw',
    '/Users/yetchi/Desktop/vizStudy/project_libra/libra/eval/data/decompressed_58.raw',
    '/Users/yetchi/Desktop/vizStudy/project_libra/libra/eval/data/decompressed_59.raw',
    '/Users/yetchi/Desktop/vizStudy/project_libra/libra/eval/data/decompressed_60.raw',
    '/Users/yetchi/Desktop/vizStudy/project_libra/libra/eval/data/decompressed_61.raw',
    '/Users/yetchi/Desktop/vizStudy/project_libra/libra/eval/data/decompressed_62.raw',
    '/Users/yetchi/Desktop/vizStudy/project_libra/libra/eval/data/decompressed_63.raw',
    '/Users/yetchi/Desktop/vizStudy/project_libra/libra/eval/data/decompressed_64.raw',
    '/Users/yetchi/Desktop/vizStudy/project_libra/libra/eval/data/decompressed_65.raw',
    '/Users/yetchi/Desktop/vizStudy/project_libra/libra/eval/data/decompressed_66.raw',
    '/Users/yetchi/Desktop/vizStudy/project_libra/libra/eval/data/decompressed_67.raw',
    '/Users/yetchi/Desktop/vizStudy/project_libra/libra/eval/data/decompressed_68.raw',
    '/Users/yetchi/Desktop/vizStudy/project_libra/libra/eval/data/decompressed_69.raw'
]


# Define the directory where screenshots will be saved
output_directory = '/Users/yetchi/Desktop/vizStudy/project_libra/libra/eval/images/'

# Create the output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Define a function to process each file and save a screenshot
def process_file(file_name):
    # ----------------------------------------------------------------
    # setup views used in the visualization
    # ----------------------------------------------------------------

    # get the material library
    materialLibrary1 = GetMaterialLibrary()

    # Create a new 'Render View'
    renderView1 = CreateView('RenderView')
    renderView1.ViewSize = [2009, 1148]
    renderView1.AxesGrid = 'Grid Axes 3D Actor'
    renderView1.CenterOfRotation = [127.5, 127.5, 127.5]
    renderView1.StereoType = 'Crystal Eyes'
    renderView1.CameraPosition = [-204.15009215341286, 697.5548521293967, 668.8644735525904]
    renderView1.CameraFocalPoint = [127.4999999999999, 127.5, 127.5]
    renderView1.CameraViewUp = [0.1853435701228487, 0.7312441027016987, -0.6564524531739555]
    renderView1.CameraFocalDisk = 1.0
    renderView1.CameraParallelScale = 220.83647796503186
    renderView1.LegendGrid = 'Legend Grid Actor'
    renderView1.BackEnd = 'OSPRay raycaster'
    renderView1.OSPRayMaterialLibrary = materialLibrary1

    SetActiveView(None)

    # ----------------------------------------------------------------
    # setup view layouts
    # ----------------------------------------------------------------

    # create new layout object 'Layout #1'
    layout1 = CreateLayout(name='Layout #1')
    layout1.AssignView(0, renderView1)
    layout1.SetSize(2009, 1148)

    # ----------------------------------------------------------------
    # restore active view
    SetActiveView(renderView1)
    # ----------------------------------------------------------------

    # ----------------------------------------------------------------
    # setup the data processing pipelines
    # ----------------------------------------------------------------

    # create a new 'Image Reader'
    image_reader = ImageReader(registrationName='image_reader', FileNames=[file_name])
    image_reader.DataScalarType = 'float'
    image_reader.DataByteOrder = 'LittleEndian'
    image_reader.DataExtent = [0, 255, 0, 255, 0, 255]

    # ----------------------------------------------------------------
    # setup the visualization in view 'renderView1'
    # ----------------------------------------------------------------

    # show data from image_reader
    image_readerDisplay = Show(image_reader, renderView1, 'UniformGridRepresentation')

    # get 2D transfer function for 'ImageFile'
    imageFileTF2D = GetTransferFunction2D('ImageFile')
    imageFileTF2D.ScalarRangeInitialized = 1
    imageFileTF2D.Range = [1.4065108189242892e-07, 150.66188049316406, 0.0, 1.0]

    # get color transfer function/color map for 'ImageFile'
    imageFileLUT = GetColorTransferFunction('ImageFile')
    imageFileLUT.TransferFunction2D = imageFileTF2D
    imageFileLUT.RGBPoints = [1.4065108189242892e-07, 0.23137254902, 0.298039215686, 0.752941176471, 75.33094031690757, 0.865, 0.865, 0.865, 150.66188049316406, 0.705882352941, 0.0156862745098, 0.149019607843]
    imageFileLUT.ScalarRangeInitialized = 1.0

    # get opacity transfer function/opacity map for 'ImageFile'
    imageFilePWF = GetOpacityTransferFunction('ImageFile')
    imageFilePWF.Points = [1.4065108189242892e-07, 0.0, 0.5, 0.0, 5.169770240783691, 0.125, 0.5, 0.0, 8.862462997436523, 0.6473214626312256, 0.5, 0.0, 35.819122314453125, 0.2723214328289032, 0.5, 0.0, 138.8452606201172, 0.1517857164144516, 0.5, 0.0, 150.66188049316406, 1.0, 0.5, 0.0]
    imageFilePWF.ScalarRangeInitialized = 1

    # trace defaults for the display properties.
    image_readerDisplay.Representation = 'Volume'
    image_readerDisplay.ColorArrayName = ['POINTS', 'ImageFile']
    image_readerDisplay.LookupTable = imageFileLUT
    image_readerDisplay.SelectTCoordArray = 'None'
    image_readerDisplay.SelectNormalArray = 'None'
    image_readerDisplay.SelectTangentArray = 'None'
    image_readerDisplay.OSPRayScaleArray = 'ImageFile'
    image_readerDisplay.OSPRayScaleFunction = 'Piecewise Function'
    image_readerDisplay.Assembly = ''
    image_readerDisplay.SelectOrientationVectors = 'None'
    image_readerDisplay.ScaleFactor = 25.5
    image_readerDisplay.SelectScaleArray = 'ImageFile'
    image_readerDisplay.GlyphType = 'Arrow'
    image_readerDisplay.GlyphTableIndexArray = 'ImageFile'
    image_readerDisplay.GaussianRadius = 1.2750000000000001
    image_readerDisplay.SetScaleArray = ['POINTS', 'ImageFile']
    image_readerDisplay.ScaleTransferFunction = 'Piecewise Function'
    image_readerDisplay.OpacityArray = ['POINTS', 'ImageFile']
    image_readerDisplay.OpacityTransferFunction = 'Piecewise Function'
    image_readerDisplay.DataAxesGrid = 'Grid Axes Representation'
    image_readerDisplay.PolarAxes = 'Polar Axes Representation'
    image_readerDisplay.ScalarOpacityUnitDistance = 1.7320508075688774
    image_readerDisplay.ScalarOpacityFunction = imageFilePWF
    image_readerDisplay.TransferFunction2D = imageFileTF2D
    image_readerDisplay.OpacityArrayName = ['POINTS', 'ImageFile']
    image_readerDisplay.ColorArray2Name = ['POINTS', 'ImageFile']
    image_readerDisplay.Shade = 1
    image_readerDisplay.IsosurfaceValues = [75.33094031690757]
    image_readerDisplay.SliceFunction = 'Plane'
    image_readerDisplay.Slice = 127
    image_readerDisplay.SelectInputVectors = [None, '']
    image_readerDisplay.WriteLog = ''

    # init the 'Piecewise Function' selected for 'ScaleTransferFunction'
    image_readerDisplay.ScaleTransferFunction.Points = [1.4065108189242892e-07, 0.0, 0.5, 0.0, 150.66188049316406, 1.0, 0.5, 0.0]

    # init the 'Piecewise Function' selected for 'OpacityTransferFunction'
    image_readerDisplay.OpacityTransferFunction.Points = [1.4065108189242892e-07, 0.0, 0.5, 0.0, 150.66188049316406, 1.0, 0.5, 0.0]

    # init the 'Plane' selected for 'SliceFunction'
    image_readerDisplay.SliceFunction.Origin = [127.5, 127.5, 127.5]

    # setup the color legend parameters for each legend in this view

    # get color legend/bar for imageFileLUT in view renderView1
    imageFileLUTColorBar = GetScalarBar(imageFileLUT, renderView1)
    imageFileLUTColorBar.Title = 'ImageFile'
    imageFileLUTColorBar.ComponentTitle = ''

    # set color bar visibility
    imageFileLUTColorBar.Visibility = 1

    # show color legend
    image_readerDisplay.SetScalarBarVisibility(renderView1, True)

    # ----------------------------------------------------------------
    # setup color maps and opacity maps used in the visualization
    # note: the Get..() functions create a new object, if needed
    # ----------------------------------------------------------------

    # ----------------------------------------------------------------
    # setup animation scene, tracks and keyframes
    # note: the Get..() functions create a new object, if needed
    # ----------------------------------------------------------------

    # get the time-keeper
    timeKeeper1 = GetTimeKeeper()

    # initialize the timekeeper

    # get time animation track
    timeAnimationCue1 = GetTimeTrack()

    # initialize the animation track

    # get animation scene
    animationScene1 = GetAnimationScene()

    # initialize the animation scene
    animationScene1.ViewModules = renderView1
    animationScene1.Cues = timeAnimationCue1
    animationScene1.AnimationTime = 0.0

    # initialize the animation scene

    # ----------------------------------------------------------------
    # restore active source
    SetActiveSource(None)
    # ----------------------------------------------------------------

    ## Save a screenshot of the active view
    screenshot_filename = os.path.join(output_directory, os.path.basename(file_name).replace('.raw', '.png'))
    SaveScreenshot(screenshot_filename)

# Loop over the list of file names
for file_name in file_names:
    process_file(file_name)
