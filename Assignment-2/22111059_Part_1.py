import vtk
from vtk import *

#loading the dataset
reader = vtkXMLImageDataReader()
reader.SetFileName('Isabel_2D.vti')         
reader.Update() 

#creating data object from the reader's output
data = reader.GetOutput()
#print(data, "\n")

dataArr= data.GetPointData().GetArray('Pressure')
#print(dataArr.GetTuple.GetCell(0))

#Getting isoValue as input from user
#Finding Pressure Range
x,y=data.GetScalarRange()
print("Enter the isovalue that you want to extract in the range ( " , x, "to ", y ," ): ")
isoVal= float(input())

#Getting no. of cells
n= data.GetNumberOfCells()

#Converting vtk array to numpy array
import numpy as np
from vtk.util.numpy_support import vtk_to_numpy

width, height, _ = data .GetDimensions()
vtk_array = data.GetPointData().GetScalars()
components = vtk_array.GetNumberOfComponents()

arr = vtk_to_numpy(vtk_array).reshape(height, width, components)

#print(arr[0][1])


#Interpolation Function in order to find points on the active edges of the cell
def linear_interpolation(val1, val2, C, vertex1, vertex2):
   slope = (val1 - C) / (val1 - val2)
   x = vertex1[0] + slope * (vertex2[0] - vertex1[0])
   y = vertex1[1] + slope * (vertex2[1] - vertex1[1])
   return (x, y)


#Iterating through the dataset
isoContour=[]
for i in range (arr.shape[0]-1):
  for j in range (arr.shape[1]-1):

    #Quering vertices in the counterclockwise direction
    v1=arr[i,j]
    v2=arr[i+1,j]
    v3=arr[i+1,j+1]
    v4=arr[i,j+1]
    #print(v1,v2,v3,v4)

    #Defining possible cases from 0 to 15
    case=0
    if(v1>isoVal):
      case+=1
    if(v2>isoVal):
      case+=2
    if(v3>isoVal):
      case+=4
    if(v4>isoVal):
      case+=8
      
    #Defining coordinates of cell
    x1=i
    y1=j
    x2=i+1
    y2=j
    x3=i+1
    y3=j+1
    x4=i
    y4=j+1

    p1=x1,y1
    p2=x2,y2
    p3=x3,y3
    p4=x4,y4

    #No active edges
    if(case==0 or case== 15):
       continue
      
    #Interpolating in cases of active edge found
    if(case == 1):
       isoContour.append(linear_interpolation(v1, v2, isoVal, p1, p2))
       isoContour.append(linear_interpolation(v1, v4, isoVal, p1, p4))
    elif(case==2):
       isoContour.append(linear_interpolation(v2, v3, isoVal, p2, p3))
       isoContour.append(linear_interpolation(v1, v2, isoVal, p1, p2))
    elif(case==3):
       isoContour.append(linear_interpolation(v2, v3, isoVal, p2, p3))
       isoContour.append(linear_interpolation(v1, v4, isoVal, p1, p4))
    elif(case==4):
       isoContour.append(linear_interpolation(v2, v3, isoVal, p2, p3))
       isoContour.append(linear_interpolation(v3, v4, isoVal, p3, p4))

    #Case when two line segments will be found
    elif(case==5):
       isoContour.append(linear_interpolation(v1, v4, isoVal, p1, p4))
       isoContour.append(linear_interpolation(v1, v2, isoVal, p1, p2))
       isoContour.append(linear_interpolation(v3, v2, isoVal, p3, p2))
       isoContour.append(linear_interpolation(v3, v4, isoVal, p3, p4))
    elif(case==6):
       isoContour.append(linear_interpolation(v3, v4, isoVal, p3, p4))
       isoContour.append(linear_interpolation(v1, v2, isoVal, p1, p2))
    elif(case==7):
       isoContour.append(linear_interpolation(v3, v4, isoVal, p3, p4))
       isoContour.append(linear_interpolation(v1, v4, isoVal, p1, p4))
    elif(case==8):
       isoContour.append(linear_interpolation(v3, v4, isoVal, p3, p4))
       isoContour.append(linear_interpolation(v1, v4, isoVal, p1, p4))
    elif(case==9):
       isoContour.append(linear_interpolation(v3, v4, isoVal, p3, p4))
       isoContour.append(linear_interpolation(v1, v2, isoVal, p1, p2))

    #Case when two line segments will be found
    elif(case==10):
       isoContour.append(linear_interpolation(v2, v3, isoVal, p2, p3))
       isoContour.append(linear_interpolation(v1, v2, isoVal, p1, p2))
       isoContour.append(linear_interpolation(v1, v4, isoVal, p1, p4))
       isoContour.append(linear_interpolation(v3, v4, isoVal, p3, p4))
    elif(case==11):
       isoContour.append(linear_interpolation(v2, v3, isoVal, p2, p3))
       isoContour.append(linear_interpolation(v3, v4, isoVal, p3, p4))
    elif(case==12):
       isoContour.append(linear_interpolation(v2, v3, isoVal, p2, p3))
       isoContour.append(linear_interpolation(v1, v4, isoVal, p1, p4))
    elif(case==13):
       isoContour.append(linear_interpolation(v2, v3, isoVal, p2, p3))
       isoContour.append(linear_interpolation(v1, v2, isoVal, p1, p2))
    elif(case==14):
       isoContour.append(linear_interpolation(v1, v4, isoVal, p1, p4))
       isoContour.append(linear_interpolation(v1, v2, isoVal, p1, p2))

#Converting list into numpy array
isoContour= np.array(isoContour)
#for i in isoContour:
  #print(i)
#print(isoContour)


#Creating PolyData object
polyData = vtkPolyData()

#Creating Points Array and setting points to the array
points = vtkPoints()
for vertex in isoContour:
        x, y= vertex
        points.InsertNextPoint(y,x, 25)
polyData.SetPoints(points)


#Setting lines
lines = vtkCellArray()
n = len(isoContour)
for i in range(0,n-1,2):
        line = vtk.vtkLine()
        line.GetPointIds().SetId(0, i)
        line.GetPointIds().SetId(1, i + 1)
        lines.InsertNextCell(line)

polyData.SetLines(lines)

#Writing the VTK XML PolyData file format
writer = vtkXMLPolyDataWriter()

#.vtp file named isoContour will be generated
writer.SetFileName("isoContour.vtp")
writer.SetInputData(polyData)
writer.Write()

print("vtp file generated!")

			
		
		
		
		


