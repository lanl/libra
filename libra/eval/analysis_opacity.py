import os
from paraview.simple import *
import csv

paraview.compatibility.major = 5
paraview.compatibility.minor = 12

paraview.simple._DisableFirstRenderCameraReset()

# Define the list of file names
file_names = [
    '/Users/yetchi/Desktop/analysis/data/input.raw',
    '/Users/yetchi/Desktop/analysis/data/decompressed_35.raw',
    '/Users/yetchi/Desktop/analysis/data/decompressed_36.raw',
    '/Users/yetchi/Desktop/analysis/data/decompressed_37.raw',
    '/Users/yetchi/Desktop/analysis/data/decompressed_38.raw',
    '/Users/yetchi/Desktop/analysis/data/decompressed_39.raw',
    '/Users/yetchi/Desktop/analysis/data/decompressed_40.raw',
    '/Users/yetchi/Desktop/analysis/data/decompressed_41.raw',
    '/Users/yetchi/Desktop/analysis/data/decompressed_42.raw',
    '/Users/yetchi/Desktop/analysis/data/decompressed_43.raw',
    '/Users/yetchi/Desktop/analysis/data/decompressed_44.raw',
    '/Users/yetchi/Desktop/analysis/data/decompressed_45.raw',
    '/Users/yetchi/Desktop/analysis/data/decompressed_46.raw',
    '/Users/yetchi/Desktop/analysis/data/decompressed_47.raw',
    '/Users/yetchi/Desktop/analysis/data/decompressed_48.raw',
    '/Users/yetchi/Desktop/analysis/data/decompressed_49.raw',
    '/Users/yetchi/Desktop/analysis/data/decompressed_50.raw',
    '/Users/yetchi/Desktop/analysis/data/decompressed_51.raw',
    '/Users/yetchi/Desktop/analysis/data/decompressed_52.raw',
    '/Users/yetchi/Desktop/analysis/data/decompressed_53.raw',
    '/Users/yetchi/Desktop/analysis/data/decompressed_54.raw',
    '/Users/yetchi/Desktop/analysis/data/decompressed_55.raw',
    '/Users/yetchi/Desktop/analysis/data/decompressed_56.raw',
    '/Users/yetchi/Desktop/analysis/data/decompressed_57.raw',
    '/Users/yetchi/Desktop/analysis/data/decompressed_58.raw',
    '/Users/yetchi/Desktop/analysis/data/decompressed_59.raw',
    '/Users/yetchi/Desktop/analysis/data/decompressed_60.raw'
]

# Define the directory where screenshots will be saved
output_directory = '/Users/yetchi/Desktop/analysis/output/opacity'

# Create the output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Define opacity levels to test
opacity_levels = [0.2, 0.4, 0.6, 0.8, 1.0]

# Define a function to process each file and save screenshots with different opacity levels
def process_file(file_name, opacity_level):
    # Setup views used in the visualization
    materialLibrary1 = GetMaterialLibrary()
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

    layout1 = CreateLayout(name='Layout #1')
    layout1.AssignView(0, renderView1)
    layout1.SetSize(2009, 1148)

    SetActiveView(renderView1)

    image_reader = ImageReader(registrationName='image_reader', FileNames=[file_name])
    image_reader.DataScalarType = 'float'
    image_reader.DataByteOrder = 'LittleEndian'
    image_reader.DataExtent = [0, 255, 0, 255, 0, 255]

    image_readerDisplay = Show(image_reader, renderView1, 'UniformGridRepresentation')

    imageFileTF2D = GetTransferFunction2D('ImageFile')
    imageFileTF2D.ScalarRangeInitialized = 1
    imageFileTF2D.Range = [1.4065108189242892e-07, 150.66188049316406, 0.0, 1.0]

    imageFileLUT = GetColorTransferFunction('ImageFile')
    imageFileLUT.TransferFunction2D = imageFileTF2D
    imageFileLUT.RGBPoints = [1.4065108189242892e-07, 0.23137254902, 0.298039215686, 0.752941176471, 75.33094031690757, 0.865, 0.865, 0.865, 150.66188049316406, 0.705882352941, 0.0156862745098, 0.149019607843]
    imageFileLUT.ScalarRangeInitialized = 1.0

    imageFilePWF = GetOpacityTransferFunction('ImageFile')
    imageFilePWF.Points = [1.4065108189242892e-07, 0.0, 0.5, 0.0, 5.169770240783691, opacity_level, 0.5, 0.0, 8.862462997436523, 0.6473214626312256, 0.5, 0.0, 35.819122314453125, 0.2723214328289032, 0.5, 0.0, 138.8452606201172, 0.1517857164144516, 0.5, 0.0, 150.66188049316406, 1.0, 0.5, 0.0]
    imageFilePWF.ScalarRangeInitialized = 1

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

    image_readerDisplay.ScaleTransferFunction.Points = [1.4065108189242892e-07, 0.0, 0.5, 0.0, 150.66188049316406, 1.0, 0.5, 0.0]
    image_readerDisplay.OpacityTransferFunction.Points = [1.4065108189242892e-07, 0.0, 0.5, 0.0, 150.66188049316406, 1.0, 0.5, 0.0]

    image_readerDisplay.SliceFunction.Origin = [127.5, 127.5, 127.5]

    imageFileLUTColorBar = GetScalarBar(imageFileLUT, renderView1)
    imageFileLUTColorBar.Title = 'ImageFile'
    imageFileLUTColorBar.ComponentTitle = ''
    imageFileLUTColorBar.Visibility = 1

    image_readerDisplay.SetScalarBarVisibility(renderView1, True)

    screenshot_filename = os.path.join(output_directory, f"{os.path.basename(file_name).replace('.raw', '')}_opacity_{int(opacity_level*100)}.png")
    SaveScreenshot(screenshot_filename)

# Create CSV file to save image paths and configurations
csv_file = os.path.join(output_directory, "opacity_levels.csv")
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["FileName", "OpacityLevel", "ImagePath"])

    for file_name in file_names:
        for opacity_level in opacity_levels:
            process_file(file_name, opacity_level)
            image_path = os.path.join(output_directory, f"{os.path.basename(file_name).replace('.raw', '')}_opacity_{int(opacity_level*100)}.png")
            writer.writerow([os.path.basename(file_name), opacity_level, image_path])
