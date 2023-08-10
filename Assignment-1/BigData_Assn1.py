import vtk
from vtk import *

#loading the dataset

reader = vtkXMLImageDataReader()
reader.SetFileName('Isabel_2D.vti')         
reader.Update() 

#creating data object from the reader's output
                        
data = reader.GetOutput()
print(data, "\n")

#Q-1
#1
numCells = data.GetNumberOfCells()
print("The number of cells in the dataset: ", numCells, "\n")

#2
numDimensions= data.GetDimensions()
print("The Number of dimensions in the dataset: ", numDimensions, "\n")

#3
numPoints= data.GetNumberOfPoints()
print("The number of points in the dataset: ", numPoints, "\n")

#4
range=data.GetScalarRange()
print("The range of Pressure values present in the dataset: ",range, "\n")

#5
#converting vtk array to numpy array

import numpy as np
from vtk.util.numpy_support import vtk_to_numpy

width, height, _ = data.GetDimensions()
vtk_array = data.GetPointData().GetScalars()
components = vtk_array.GetNumberOfComponents()

arr = vtk_to_numpy(vtk_array).reshape(height, width, components)

#accessing array elements
#for i in arr : 
    #for j in i : 
        #print(j)

#finding mean of numpy array

mean= np.mean(arr)
print("The average Pressure value of the entire dataset: ",mean, "\n")


#6-7-8
print("Extract a vtkCell object with cell id: ")
cellId= int(input())

#extracting a cell

cell = data.GetCell(cellId)
pid1 = cell.GetPointId(0)
pid2 = cell.GetPointId(1)
pid3 = cell.GetPointId(3)
pid4 = cell.GetPointId(2)

print('1D indices of the cell corner points:')
print(pid1, pid2, pid3, pid4, "\n")

#getting the location

print('Point 3-D coordinates of cell corners in counter clockwise order and their data values:')
print(data.GetPoint(pid1))
print(data.GetPoint(pid2))
print(data.GetPoint(pid3))
print(data.GetPoint(pid4), "\n")

#9
list1= data.GetPoint(pid1)
list2= data.GetPoint(pid2)
list3= data.GetPoint(pid3)
list4= data.GetPoint(pid4)

#averaging the corner vertices

cellCenter=[]
cellCenter.append((list1[0]+list2[0]+list3[0]+list4[0])/4)
cellCenter.append((list1[1]+list2[1]+list3[1]+list4[1])/4)
cellCenter.append((list1[2]+list2[2]+list3[2]+list4[2])/4)


cellCenter=tuple(cellCenter)
print("The 3D coordinate of the cell center using its four corner vertices: ")
print(cellCenter, "\n")



#10
dataArr= data.GetPointData().GetArray('Pressure')

#values of pressure for the extracted cell 

val1 = dataArr.GetTuple1(pid1)
val2 = dataArr.GetTuple1(pid2)
val3 = dataArr.GetTuple1(pid3)
val4 = dataArr.GetTuple1(pid4)
print("The Pressure for all the four vertices of the extracted cell: " )
print(val1,val2,val3,val4, "\n")



#11
#mean pressure

avgP= (val1+val2+val3+val4)/4
print("The average pressure value at the cell center: ",avgP, "\n")




#Q-2

points = vtkPoints()
points.InsertNextPoint(data.GetPoint(pid1))
points.InsertNextPoint(data.GetPoint(pid2))
points.InsertNextPoint(data.GetPoint(pid3))
points.InsertNextPoint(data.GetPoint(pid4))


colors = vtkNamedColors()
Colors = vtkUnsignedCharArray()
Colors.SetNumberOfComponents(3)
Colors.SetName('Colors')
Colors.InsertNextTuple3(*colors.GetColor3ub('Red'))
Colors.InsertNextTuple3(*colors.GetColor3ub('Lime'))
Colors.InsertNextTuple3(*colors.GetColor3ub('Coral'))
Colors.InsertNextTuple3(*colors.GetColor3ub('Blue'))


polydata = vtkPolyData()
polydata.SetPoints(points)
#print(polydata)

polydata.GetPointData().SetScalars(Colors)
polydata.Modified()


vertexGlyphFilter = vtkVertexGlyphFilter()
vertexGlyphFilter.AddInputData(polydata)
vertexGlyphFilter.Update()

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(vertexGlyphFilter.GetOutputPort())
mapper.Update()


actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetPointSize(40)
#actor.GetProperty().SetColor(colors.GetColor3d('Blue'))



renderer = vtkRenderer()
renderWindow = vtkRenderWindow()
renderWindow.AddRenderer(renderer)
renderWindowInteractor = vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)


renderer.AddActor(actor)
renderer.SetBackground(colors.GetColor3d('White'))


renderWindow.SetWindowName('VertexGlyphFilter')
renderWindow.Render()
renderWindowInteractor.Start()











