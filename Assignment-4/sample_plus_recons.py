import numpy as np
import vtk
from vtk.util import numpy_support
from scipy.interpolate import griddata
import time
import vtk.util.numpy_support as npvtk
import numpy as np
from vtk.util import numpy_support


def simple_random_sampling(vti_file, sampling_percentage):
    # Load VTI file
    vti_reader = vtk.vtkXMLImageDataReader()
    vti_reader.SetFileName("Isabel_3D.vti")
    vti_reader.Update()

    # Get image dimensions
    extent = vti_reader.GetOutput().GetExtent()
    dim_x = extent[1] + 1
    dim_y = extent[3] + 1
    dim_z = extent[5] + 1

    # Generate random indices for sampling
    num_points = int(dim_x * dim_y * dim_z * sampling_percentage / 100)
    indices = np.random.randint(0, dim_x * dim_y * dim_z, num_points)

    # Convert indices to 3D coordinates
    sampled_points = []
    for index in indices:
        z = index // (dim_x * dim_y)
        y = (index // dim_x) % dim_y
        x = index % dim_x
        sampled_points.append([x, y, z])

    # Convert sampled points to NumPy array
    sampled_points = np.array(sampled_points)

    # Get voxel values at sampled points
    sampled_data = []
    for point in sampled_points:
        voxel_value = vti_reader.GetOutput().GetScalarComponentAsDouble(int(point[0]), int(point[1]), int(point[2]), 0)
        sampled_data.append(voxel_value)

    # Convert sampled data to NumPy array
    sampled_data = np.array(sampled_data)

    # Create VTKPolyData for sampled points
    points_polydata = vtk.vtkPolyData()
    points_polydata.SetPoints(vtk.vtkPoints())

    # Add sampled points to VTKPolyData
    for point in sampled_points:
        points_polydata.GetPoints().InsertNextPoint(point[0], point[1], point[2])

    # Add data values to VTKPolyData as point data
    data_array = vtk.vtkDoubleArray()
    data_array.SetName("values")
    data_array.SetNumberOfComponents(1)
    for value in sampled_data:
        data_array.InsertNextTuple1(value)

    points_polydata.GetPointData().AddArray(data_array)

    # Write VTKPolyData to VTP file
    writer = vtk.vtkXMLPolyDataWriter()
    writer.SetFileName(f"sampled_{sampling_percentage:.0f}.vtp")
    writer.SetInputData(points_polydata)
    writer.Write()
    return sampled_points, sampled_data


def reconstruct_volume(sampled_points, sampled_data, extent, interpolation_method):
    # Create grid coordinates for volume
    dim_x = extent[1] + 1
    dim_y = extent[3] + 1
    dim_z = extent[5] + 1
    grid_x, grid_y, grid_z = np.meshgrid(np.arange(dim_x), np.arange(dim_y), np.arange(dim_z), indexing='ij')

    # Reconstruct volume data
    volume_data = griddata(sampled_points, sampled_data, (grid_x, grid_y, grid_z), method=interpolation_method)

    if interpolation_method == "linear":
        mask = np.isnan(volume_data)
        volume_data[mask] = griddata(sampled_points, sampled_data, (grid_x[mask], grid_y[mask], grid_z[mask]), method="nearest")

    # Convert volume data to VTKImageData
    volume = vtk.vtkImageData()
    volume.SetExtent(extent)
    volume.SetSpacing(1, 1, 1)
    volume.SetOrigin(0, 0, 0)
    volume.AllocateScalars(vtk.VTK_DOUBLE, 1)

    # Set volume data values
    for z in range(dim_z):
        for y in range(dim_y):
            for x in range(dim_x):
                voxel_value = volume_data[x, y, z]
                volume.SetScalarComponentFromDouble(x, y, z, 0, voxel_value)

    return volume


def snr(arrgt, arr_recon):
    gt = npvtk.vtk_to_numpy(arrgt.GetPointData().GetScalars())
    recon = npvtk.vtk_to_numpy(arr_recon.GetPointData().GetScalars())
    diff= gt- recon
    sqd_max_diff= (np.max(gt)-np.min(gt))**2
    snr= 10*np.log10(sqd_max_diff/np.mean(diff**2))
    return snr

def load_vti_file(file_path):
    reader = vtk.vtkXMLImageDataReader()
    reader.SetFileName(file_path)
    reader.Update()

    # Get the loaded data
    data = reader.GetOutput()

    return data



def save_vti(volume, sp, method):
# Write reconstructed volume to VTI file
    vti_writer = vtk.vtkXMLImageDataWriter()
    vti_writer.SetFileName(f"reconstructed_{method}_{sp:.0f}.vti")
    vti_writer.SetInputData(volume)
    vti_writer.Write()



# Load the original volume data
volume_data = load_vti_file("Isabel_3D.vti")

sampling_percentages = [1, 3, 5]
methods = ["nearest", "linear"]

# Load VTI file and get extent
vti_reader = vtk.vtkXMLImageDataReader()
vti_reader.SetFileName("Isabel_3D.vti")
vti_reader.Update()
extent = vti_reader.GetOutput().GetExtent()

#Contain the SNR and Reconstruction Time Values
results = []

for sp in sampling_percentages:
    sampled_points, sampled_values = simple_random_sampling(volume_data, sp)
    # save_vtp_file(sampled_points, sampled_values, f"sampled_{sp:.0f}.vtp")
    
    for method in methods:
        start_time = time.time()
        reconstructed_volume = reconstruct_volume(sampled_points, sampled_values, extent, method)
        save_vti(reconstructed_volume,sp, method)
        reconstruction_time = time.time() - start_time
        
        quality = snr(volume_data, reconstructed_volume)
        results.append((sp, method, quality, reconstruction_time))

# Save the results in a table
with open("results.txt", "w") as f:
    f.write("Sampling % | Method | SNR | Reconstruction Time\n")
    for result in results:
        f.write(f"{result[0]:.0f} % | {result[1]} | {result[2]:.2f} dB | {result[3]:.2f} s\n")