import os
import csv
import argparse
import paraview
from paraview.simple import *
import numpy as np

paraview.compatibility.major = 5
paraview.compatibility.minor = 12

#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

def fibonacci_sphere(samples=8, radius=700):
    points = []
    phi = np.pi * (3. - np.sqrt(5.))  # golden angle in radians

    for i in range(samples):
        y = 1 - (i / float(samples - 1)) * 2  # y goes from 1 to -1
        r = np.sqrt(1 - y * y)  # radius at y

        theta = phi * i  # golden angle increment

        x = np.cos(theta) * r
        z = np.sin(theta) * r

        points.append((x * radius, y * radius, z * radius))

    return points

def process_file(file_name, output_directory):
    # Get the material library
    materialLibrary1 = GetMaterialLibrary()

    # Create a new 'Render View'
    renderView1 = CreateView('RenderView')
    renderView1.ViewSize = [2009, 1148]
    renderView1.AxesGrid = 'Grid Axes 3D Actor'
    renderView1.CenterOfRotation = [127.5, 127.5, 127.5]
    renderView1.StereoType = 'Crystal Eyes'
    renderView1.CameraFocalPoint = [127.5, 127.5, 127.5]
    renderView1.CameraFocalDisk = 1.0
    renderView1.CameraParallelScale = 220.83647796503186
    renderView1.LegendGrid = 'Legend Grid Actor'
    renderView1.BackEnd = 'OSPRay raycaster'
    renderView1.OSPRayMaterialLibrary = materialLibrary1

    SetActiveView(None)

    # Create new layout object 'Layout #1'
    layout1 = CreateLayout(name='Layout #1')
    layout1.AssignView(0, renderView1)
    layout1.SetSize(2009, 1148)

    # Restore active view
    SetActiveView(renderView1)

    # Create a new 'Image Reader'
    image_reader = ImageReader(registrationName='image_reader', FileNames=[file_name])
    image_reader.DataScalarType = 'float'
    image_reader.DataByteOrder = 'LittleEndian'
    image_reader.DataExtent = [0, 255, 0, 255, 0, 255]

    # Show data from image_reader
    image_readerDisplay = Show(image_reader, renderView1, 'UniformGridRepresentation')

    # Get 2D transfer function for 'ImageFile'
    imageFileTF2D = GetTransferFunction2D('ImageFile')
    imageFileTF2D.ScalarRangeInitialized = 1
    imageFileTF2D.Range = [1.4065108189242892e-07, 150.66188049316406, 0.0, 1.0]

    # Get color transfer function/color map for 'ImageFile'
    imageFileLUT = GetColorTransferFunction('ImageFile')
    imageFileLUT.TransferFunction2D = imageFileTF2D
    imageFileLUT.RGBPoints = [1.4065108189242892e-07, 0.23137254902, 0.298039215686, 0.752941176471, 75.33094031690757, 0.865, 0.865, 0.865, 150.66188049316406, 0.705882352941, 0.0156862745098, 0.149019607843]
    imageFileLUT.ScalarRangeInitialized = 1.0

    # Get opacity transfer function/opacity map for 'ImageFile'
    imageFilePWF = GetOpacityTransferFunction('ImageFile')
    imageFilePWF.Points = [1.4065108189242892e-07, 0.0, 0.5, 0.0, 5.169770240783691, 0.125, 0.5, 0.0, 8.862462997436523, 0.6473214626312256, 0.5, 0.0, 35.819122314453125, 0.2723214328289032, 0.5, 0.0, 138.8452606201172, 0.1517857164144516, 0.5, 0.0, 150.66188049316406, 1.0, 0.5, 0.0]
    imageFilePWF.ScalarRangeInitialized = 1

    # Display properties
    image_readerDisplay.Representation = 'Volume'
    image_readerDisplay.ColorArrayName = ['POINTS', 'ImageFile']
    image_readerDisplay.LookupTable = imageFileLUT
    image_readerDisplay.SelectTCoordArray = 'None'
    image_readerDisplay.SelectNormalArray = 'None'
    image_readerDisplay.SelectTangentArray = 'None'
    image_readerDisplay.OSPRayScaleArray = 'ImageFile'
    image_readerDisplay.OSPRayScaleFunction = 'Piecewise Function'
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

    # Initialize the 'Piecewise Function' selected for 'ScaleTransferFunction'
    image_readerDisplay.ScaleTransferFunction.Points = [1.4065108189242892e-07, 0.0, 0.5, 0.0, 150.66188049316406, 1.0, 0.5, 0.0]

    # Initialize the 'Piecewise Function' selected for 'OpacityTransferFunction'
    image_readerDisplay.OpacityTransferFunction.Points = [1.4065108189242892e-07, 0.0, 0.5, 0.0, 150.66188049316406, 1.0, 0.5, 0.0]

    # Initialize the 'Plane' selected for 'SliceFunction'
    image_readerDisplay.SliceFunction.Origin = [127.5, 127.5, 127.5]

    # Setup the color legend parameters for each legend in this view
    imageFileLUTColorBar = GetScalarBar(imageFileLUT, renderView1)
    imageFileLUTColorBar.Title = 'ImageFile'
    imageFileLUTColorBar.ComponentTitle = ''

    # Set color bar visibility
    imageFileLUTColorBar.Visibility = 1

    # Show color legend
    image_readerDisplay.SetScalarBarVisibility(renderView1, True)

    # Generate camera positions using Fibonacci lattice
    camera_positions = fibonacci_sphere(samples=12, radius=700)

    screenshot_filenames = []
    
    camera_infos = []
    for i, (x, y, z) in enumerate(camera_positions):
        renderView1.CameraPosition = [127.5 + x, 127.5 + y, 127.5 + z]
        renderView1.CameraViewUp = [0, 1, 0]
        camera_infos.append((renderView1.CameraPosition))

        screenshot_filename = os.path.join(output_directory, os.path.basename(file_name).replace('.raw', f'_{i}.png'))

        SaveScreenshot(screenshot_filename)
        screenshot_filenames.append(screenshot_filename)
        

    return screenshot_filenames, camera_infos

def main():
    parser = argparse.ArgumentParser(description='Generate screenshots from ParaView for a list of raw data files.')
    parser.add_argument('-o', '--output', type=str, required=True,
                        help='Directory where screenshots will be saved')
    parser.add_argument('-p', '--paths', type=str, required=True,
                        help='CSV file containing paths to raw data files')
    parser.add_argument('-t', '--table', type=str, required=True,
                        help='Name of the table in CSV file to grab paths from')
    args = parser.parse_args()

    output_directory = args.output
    csv_path = args.paths
    table_name = args.table

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Read the entire CSV file
    with open(csv_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames + [f'image_path_{i}' for i in range(12)] + [f'camera_info_{i}' for i in range(12)]
        rows = list(reader)

    # Process each row
    for row in rows:
        file_name = row[table_name]
        image_paths, camera_infos = process_file(file_name, output_directory)
        for i, (path, info) in enumerate(zip(image_paths, camera_infos)):
            row[f'image_path_{i}'] = path
            row[f'camera_info_{i}'] = str(info)

    # Save updated CSV file with image paths and camera infos
    csv_output_path = os.path.join(output_directory, 'processed_images.csv')
    with open(csv_output_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

if __name__ == '__main__':
    main()
