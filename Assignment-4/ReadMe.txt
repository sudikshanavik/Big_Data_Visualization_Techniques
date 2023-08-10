22111059_Sudiksha_Navik
Assignment 4 - CS661A 
Sampling and Reconstruction


The “Navik_22111059_Assignment4.zip” file contains:
1. sample_plus_recons.py : containing the main code 
2. SNR_and_reconsTimes.pdf: containing the results of SNR and Reconstruction times with nearest neighbor and linear interpolation methods on 1%, 3% and 5% sampling.
3. ReadMe.txt file: containing the directory structure instructions on how to run the code and get results.






Instructions:
First move the Isabel_3D.vti dataset to the appropriate/same directory.
1. Run the sample_plus_recons.py file
2. You will get to see the sampled_1.vtp, sampled_3.vtp and sampled_5.vtp files. These are the sampled files. You can view these files in the Paraview. Select “values” instead of “Solid Color” and also “Point Gaussian”. It may take a few seconds to appear.
3. You will also see:
   1. reconstructed_nearest_1.vti
   2. reconstructed_nearest_3.vti
   3. reconstructed_nearest_5.vti
   4. reconstructed_linear_1.vti
   5. reconstructed_linear_3.vti
   6. reconstructed_linear_5.vti
These are the reconstructed data from the sampled version of data. You can view them on Paraview too. View it on "ImageScalars" and "Surface".
4. Also when you run sample_plus_recons.py file, the results are written back on the results.txt file. You can view the SNR and Reconstruction times for every run of the code.