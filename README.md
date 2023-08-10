# Big Data Visualization
## Assignment-1

We were provided with a dataset in the VTK (Visualization Toolkit) format containing 2D data representing pressure values. Our task was to perform various operations on this dataset to extract information and visualize it using VTK. <br>

Load the dataset from the file 'Isabel_2D.vti' and create a data object from the reader's output.<br>
Retrieve and print the following information about the dataset:<br>
a) The number of cells in the dataset<br>
b) The number of dimensions (width, height) in the dataset<br>
c) The number of points in the dataset<br>
d) The range of pressure values present in the dataset<br>
e) The average pressure value of the entire dataset<br>

Prompt the user to input a cell ID and then:<br>
a) Extract a specific cell based on the given cell ID<br>
b) Retrieve and print the 1D indices of the cell's corner points<br>
c) Retrieve and print the 3D coordinates and data values (pressure) of the cell's corner points<br>
d) Calculate and print the 3D coordinate of the cell center using its four corner vertices<br>
e) Retrieve and print the pressure values for all four vertices of the extracted cell<br>
f) Calculate and print the average pressure value at the cell center<br>
Visualize the extracted cell using VTK. The visualization should display four points representing the cell's corner vertices, each with a different color (Red, Lime, Coral, and Blue).<br>


## Assignment-2
### Part-1
Written a program to extract isocontour from a 2D uniform grid. The dataset was given in VTKImageData format. The program generates the isocontour as a VTKPolyData object and write it out to disk as a VTKPolyData file (*.vtp file). This file can be easily loaded in ParaView for visualizing the extracted contour (May have to change the color of the contour to something other than white if you have set white background in ParaView). This assignment is a simplified version of the Marching Squares algorithm.

### Part-2
Written a Python script to implement the volume rendering algorithm from the VTK library. VTK has already implemented the ray-casting algorithm. However, in this assignment, we have used the vtkSmartVolumeMapper() to render 3D scalar data and set a specific color and opacity transfer function. We have also used VTK’s Phong Shading feature to produce advanced lighting effects to make volume rendering more realistic. The ambient, diffuse, and specular parameters for Phong are given below. Here are the steps that were followed for this task:

+  Load the 3D data provided with the assignment.
          
+  Create instances of vtkColorTransferFunction and vtkPiecewiseFunction (this will work as Opacity transfer function) and set them up with the values provided below in the tables.
+  Use vtkSmartVolumeMapper() class to perform the volume rendering
+  Use vtkOutlineFilter to add an outline to the volume rendered data
+  By default, advanced shading feature, i.e., Phong shading will be off. Create an input parameter
and take input from user if the user wants to use Phong shading. If yes, then your program should
turn on Phong shading while rendering.
+  Create a 1000x1000 sized render window to show the rendering result
<img width="885" alt="Screenshot 2023-08-11 at 02 42 34" src="https://github.com/sudikshanavik/Big_Data_Visualization_Techniques/assets/100257642/ff032ad1-5033-4b2e-aac6-8a385fb274e8">

## Assignment-3
Created a simple interactive interface using Plotly and Jupyter Widgets. Plotly is used for generating visualizations and Jupyter Widgets are used to add sliders and buttons.<br>
Here is what interface does:
+  In the left side,the interface shows an interactive Isosurface visualization of the 3D dataset
provided. Plotly has an API to draw Isosurfaces. <br>
+  On the right side, the interface plots a histogram visualization of the 3D dataset. Histogram has labels and markers for axes. Plotly has an API to draw histograms.
+  The interface contains a slider that allows changing the isovalue for the Isosurface. This slider value range is mapped to the entire data range and by sliding to through different scalar values, the Isosurface plot should get updated automatically. We also colored the Isosurface using a standard Python/Plotly colormap so that the color of your Isosurface changes as you change the isovalue.
+  At the beginning, we show Isosurface of isovalue=0.0 and the histogram of the entire volume data set.
+  When we change the slider, we also update the histogram plot. Let’s say, we have selected the isovalue = x in from the slider by changing it. Then the histogram plot contains data points with the following conditions: (x - 0.25) <= points with data values in histogram <= (x + 0.25). So, essentially, we update the histogram plot with data values around (within +/- 0.25) your current selected isovalue from the slider. This is the histogram of a subset of the data and histogram axes labels should get updated with the new data range. 
  +  Finally, we added a button called ‘Reset’. When this button is clicked, the plot gets reset to its initial/beginning configuration, i.e., the slider value is set back to 0.0, Isosurface plot gets updated with the isovalue = 0.0, the histogram plot shows the histogram of the entire data set and not of a subset. 

## Assignment-4
+ Implemented a simple random sampling (SRS) function. Function takes a sampling percentage as an input parameter and return a set of sampled points. We preserved the data values for each sampled point so that later you can reconstruct the entire volume data. We preserved the data values by attaching an array with your point locations containing data values for each selected point. Output the sampled points as a VTKPolyData (*.vtp) file and write it to disk. We can load the *.vtp file in ParaView and use point Gaussian representation to visualize the sampled points.
+ Next, We reconstructed the volume data from the sampled points using ‘scipy.interpolate.griddata’ method. The griddata() method provides a few ways to reconstruct data values in missing locations and you will use nearest neighbor, and linear interpolation methods.
    + First reconstructed the volume using ‘nearest’ as your interpolation method. Stored the reconstructed volume data as a *.vti file into disk.
  +  Next, reconstructed the volume data using ‘linear’ as your interpolation method. In this case, the method may result in some locations with ‘nan’ values as we may have to extrapolate some locations, and this method does not work for such cases. So, we first perform reconstruction with the ‘linear’ interpolation method, and then the locations where you find ‘nan’ values,we replaced those locations with their nearest neighbor value. You can use ‘np.isnan’ method to check if a value is ‘nan’. So, after doing this, you will produce a reconstructed data set and then store it as a *.vti file on disk. Reconstructed volume files are readable by ParaView.
+  Finally, we evaluated the reconstruction quality of our data set by comparing it with the original raw volume data. Used Signal-to-Noise (SNR) ratio as a metric for quality comparison. We evaluated the quality for reconstruction using the ‘nearest’ and ‘linear’ methods and further measure the reconstruction time. Also performed this study for the following sampling percentages: {1%, 3%, and 5%}. We produce a table where you should present comparison results of quality and reconstruction time for both ‘nearest’ and ‘linear’ methods for the three different sampling percentages mentioned above.

       
Used the following function to compute SNR. The first parameter is a numpy array containing ground truth data values and the second parameter is a numpy array that contains reconstructed data values in same order.


<img width="769" alt="Screenshot 2023-08-11 at 02 45 00" src="https://github.com/sudikshanavik/Big_Data_Visualization_Techniques/assets/100257642/997260bb-7ad9-4c78-8d42-2c5a0d924421">
