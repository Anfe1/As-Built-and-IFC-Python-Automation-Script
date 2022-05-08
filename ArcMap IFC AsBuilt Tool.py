
"""
Created on Mon May 27 08:27:26 2019
Python Script for IFC and As-Built Analysis
@author: Andy Fernandez 
        GIS Technician

        
"""


#libraries, the arcpy librarie allows for geospatial analysis. 
import os
import arcpy
from datetime import datetime
from arcpy import env
import sys
startTime = datetime.now()





#env.workspace = r"\I:\DN\GIS Resources\Feature Layers\Xcel\Xcel Alignments.gdb" local working space where the data was kept
arcpy.env.workspace = r"I:\DN\GIS Resources\Working GIS\Alignment Exports for Script" 
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
###Known Parameters###
#Alignment location = I:\\DN\\GIS Resources\\Feature Layers\\Xcel\\Xcel Alignments.gdb\\Combined_Xcel_Alignments"
#Buffer location = "I:\\DN\\GIS Resources\\Feature Layers\\Xcel\\Xcel Buffers.gdb\\Name"

#Projection variables
NAD83_CF = "NAD 1983 StatePlane Colorado Central FIPS 0502 (US Feet)"
NAD83_NF = "NAD 1983 StatePlane Colorado North FIPS 0501 (US Feet)"
NAD83_SF = "NAD 1983 StatePlane Colorado South FIPS 0503 (US Feet)"
NAD83_MN_SF = "NAD 1983 StatePlane Minnesota South FIPS 2203 (US Feet)"
NAD83_MN_CF = "NAD 1983 StatePlane Minnesota Central FIPS 2202 (US Feet)"

#buffer geodatabase
Buffer_gdb = 'I:/DN/GIS Resources/Feature Layers/Xcel/Xcel Buffers.gdb'


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#os.startfile(Xcel_IFC_Portrait)


"##Arguments"
"##All variables need to be double quoted, unless specified"
"#This section specifies the parameters that the user will have to input."

#Export file name from civil 3D, no need to change only if you want to change the name of the line dissolve. 
Export_file_name = "AlignmentExport1.shp"

#Coordinates can be changed at the environment section above, if needed the coordinates can be changed. 
#Coordinate_System = 
#Projection colorado projections can be specified from above just copy paste the variable.
Projection = arcpy.GetParameterAsText(0)

#Output location where the files are going to be sent for the Alignment analysis.
#OL_Alignment =""
##Output location where the files are going to be sent for buffer. 
#OL_Buffer = ""
#ENE Code 
ENE_Code = arcpy.GetParameterAsText(1)

# Name of the Project example: '165_Reinforcement there cannot be dots' 
Project_Name = arcpy.GetParameterAsText(2)

#Pipe diameter example: '6'
Pipe_Diameter = arcpy.GetParameterAsText(3)

#Client name example: 'Xcel'
Client = arcpy.GetParameterAsText(4)

#Client billing code example: '1909712'
Xcel_Billing_Code = arcpy.GetParameterAsText(5)

#County example: 'DENVER'
COUNTY_1 = arcpy.GetParameterAsText(6)

#Second county use if need by removing hashtag symbol.
COUNTY_2 = arcpy.GetParameterAsText(7)
if COUNTY_2 == '#' or not COUNTY_2:
    COUNTY_2 = "NA" # provide a default value if unspecified
    
#State example: 'CO'
STATE = arcpy.GetParameterAsText(8)

#Only if needed, script accounts for output projection see above.
#Projection = 'test'
#Date the files are being created, do not touch unless needed date will be created automatically.
Date_Completed = datetime.today().strftime('%Y-%m-%d')

#Notes example: 'Phase 1 of 4', 'Phase: IFC', 'Phase: IFB', 'Phase: As-Built' or 'Anything else'
Notes = arcpy.GetParameterAsText(9)
if Notes == '#' or not Notes:
    Notes = "NA" # provide a default value if unspecified
    
#Phase example: 'Phase: IFC'
Phase = arcpy.GetParameterAsText(10)

#Sender name
SENDER = arcpy.GetParameterAsText(11) #"EN Engineering Andy Fernandez"
if SENDER == '#' or not SENDER:
    STATE = "EN Engineering Andy Fernandez" # provide a default value if unspecified

#Buffer size in Feet
Buffer_size = arcpy.GetParameterAsText(12)
#Disolved field for the buffer if applicable remove hashtag mark
#Dissolve_Fields = ""

#layout for the map
Layout_mxd = arcpy.GetParameterAsText(13)

project_file_name = Project_Name.replace(" ","_") # The file name of the project will be pulled from here adding underscores
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(Projection)# Project the entire project from the start

"Templates for MXD files, depending on the type of analysis it will change the formating of the MXD. 
#SW_GasFieldNoting_Landscape = r'I:\DN\GIS Resources\Tools\As-Built and IFB and IFC Submittal Resources\MXD Document Templates\SW_GasFieldNoting_Landscape.mxd'
#SW_GasFieldNoting_Landscape_11x17 = r'I:\DN\GIS Resources\Tools\As-Built and IFB and IFC Submittal Resources\MXD Document Templates\SW_GasFieldNoting_Landscape_11x17.mxd'
#SW_GasFieldNoting_Portrai_11x17t = r'I:\DN\GIS Resources\Tools\As-Built and IFB and IFC Submittal Resources\MXD Document Templates\SW_GasFieldNoting_Portrai_11x17t.mxd'
#SW_GasFieldNoting_Portrait = r'I:\DN\GIS Resources\Tools\As-Built and IFB and IFC Submittal Resources\MXD Document Templates\SW_GasFieldNoting_Portrait.mxd'
#Xcel_AsBuilt_Landscape = r'I:\DN\GIS Resources\Tools\As-Built and IFB and IFC Submittal Resources\MXD Document Templates\Xcel_AsBuilt_Landscape.mxd'
#Xcel_AsBuilt_Landscape_MULTI_PAGE = r'I:\DN\GIS Resources\Tools\As-Built and IFB and IFC Submittal Resources\MXD Document Templates\Xcel_AsBuilt_Landscape_MULTI-PAGE.mxd'
#Xcel_AsBuilt_Landscape_MULTI_PAGE2 = r'I:\DN\GIS Resources\Tools\As-Built and IFB and IFC Submittal Resources\MXD Document Templates\Xcel_AsBuilt_Landscape_MULTI-PAGE.mxd'
#Xcel_AsBuilt_Landscape_TWO_FRAMES = r'I:\DN\GIS Resources\Tools\As-Built and IFB and IFC Submittal Resources\MXD Document Templates\Xcel_AsBuilt_Landscape_TWO_FRAMES.mxd'
#Xcel_AsBuilt_Portrait = r'I:\DN\GIS Resources\Tools\As-Built and IFB and IFC Submittal Resources\MXD Document Templates\Xcel_AsBuilt_Portrait.mxd'
#Xcel_IFC_Landscape = r'I:\DN\GIS Resources\Tools\As-Built and IFB and IFC Submittal Resources\MXD Document Templates\Xcel_IFC_Landscape.mxd'
#Xcel_IFC_Landscape_TWO_FRAMES = r'I:\DN\GIS Resources\Tools\As-Built and IFB and IFC Submittal Resources\MXD Document Templates\Xcel_IFC_Landscape_TWO_FRAMES.mxt'
#Xcel_IFC_Portrait = r'I:\DN\GIS Resources\Tools\As-Built and IFB and IFC Submittal Resources\MXD Document Templates\Xcel_IFC_Portrait.mxd'
#Xcel_Minnesota_AsBuilt_Landscape = r'I:\DN\GIS Resources\Tools\As-Built and IFB and IFC Submittal Resources\MXD Document Templates\Xcel_Minnesota_AsBuilt_Landscape.mxd'
#Xcel_Minnesota_AsBuilt_Portrait = r'I:\DN\GIS Resources\Tools\As-Built and IFB and IFC Submittal Resources\MXD Document Templates\Xcel_Minnesota_AsBuilt_Portrait.mxd'
#Xcel_Minnesota_IFC_Portrait = r'I:\DN\GIS Resources\Tools\As-Built and IFB and IFC Submittal Resources\MXD Document Templates\Xcel_Minnesota_IFC_Portrait.mxd'
#Xcel_IFC_Portrait2 = r'I:\DN\GIS Resources\Tools\As-Built and IFB and IFC Submittal Resources\MXD Document Templates\Xcel_IFC_Portrait2.mxd'


"""-------------------------------------------------------------------------------"""
##File name automatic naming schemes, to change refer to the variables above. 
#ENE_File_Name created automatically, if needed the 'Alignment' portion can be changed here.
EFN = [Client, ENE_Code, project_file_name, Phase]
Name_join = '_'.join(EFN)
ENE_File_Name = Name_join + '_Alignment'

#Name of the buffer output
Buffer_Name = Name_join + '_Buffer'
#Dissolved output name, created automatically. Refer to the 
Dissolve_Name = Name_join + '_Dissolve'
CF = Name_join
kmzbuffername = Project_Name + " " + Buffer_size + " " + "Feet" + " " + "Buffer"
 
#location of the initial shapefiles after Civil 3D export to be used for the alignment and buffer. example: "I://DN//GIS Resources//Working GIS" 
Alignment_Input = env.workspace + "\\"
input_dissolve = Alignment_Input + Export_file_name

###VARIABLES###
##Variables for the analysis tools, no need to change any of these unless analysis changes. 
#Memory variable to write temporary data in, for desktop use in_memory. For Pro use memory.
in_memory = "in_memory"

#Temporary file locations for the analysis
tfc = "I:\\DN\\GIS Resources\\Feature Layers\\Xcel\\Xcel Alignments.gdb\\TemplateFeatureClass"
Xcel_Alignments_gdb = "I:/DN/GIS Resources/Feature Layers/Xcel/Xcel Alignments.gdb"
Combined_Xcel_Alignments = "I:/DN/GIS Resources/Feature Layers/Xcel/Xcel Alignments.gdb/Combined_Xcel_Alignments"

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
##Dissolve geometry##
#Dissolve the polylines into a single geometry.#
try:
    ml = arcpy.Dissolve_management(input_dissolve, Alignment_Input + Dissolve_Name + ".shp", "")
except Exception:
    e = sys.exc_info()[1]
    print (e.args[0])
    arcpy.AddError(e.args[0])
    
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

#Create the Folders where the files will be stored locally
path3 = "I:\\DN\\GIS Resources\\Working GIS\\" + ENE_Code + " - " + Project_Name 
path0 = path3 + "\\" + " Zip Contents"
path1 = path0 + "\\" + "Shapefiles"
path2 = path0 + "\\" + "KMZ"

try:
    os.mkdir(path3)
except OSError:
    print ("Creation of the directory %s failed" % path3)
else:
    print("Successfully created the directory %s" % path3)

try:
    os.mkdir(path0)
except OSError:
    print ("Creation of the directory %s failed" % path0)
else:
    print ("Successfully created the directory %s " % path0)

try:
    os.mkdir(path1)
except OSError:
    print ("Creation of the directory %s failed" % path1)
else:
    print ("Successfully created the directory %s " % path1)

try:
    os.mkdir(path2)
except OSError:
    print ("Creation of the directory %s failed" % path2)
else:
    print ("Successfully created the directory %s " % path2)


    
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

###Processing###

##Alignment Tool
#Add the fiels to a feature class in memory
outml = arcpy.FeatureClassToFeatureClass_conversion(ml, in_memory, Dissolve_Name, "")
arcpy.AddField_management(outml, "ENE_CODE", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(outml, "NAME", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(outml, "LINEAR_FT", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(outml, "SIZE", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(outml, "CLIENT", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(outml, "CLIENT_REF", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(outml, "COUNTY1", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(outml, "COUNTY2", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(outml, "STATE", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(outml, "PROJECTION", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(outml, "COMPLETED", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(outml, "NOTES", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(outml, "FILE_NAME", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(outml, "PHASE", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")


#Delete obsolete fiels from the product dissolve
outmldl = arcpy.DeleteField_management(outml, ["Shape*", "Id"])

#Calculate the fields 
arcpy.CalculateField_management(outmldl, "ENE_CODE", "'" + ENE_Code + "'", "PYTHON", "")
arcpy.CalculateField_management(outmldl, "NAME","'" + Project_Name + "'" , "PYTHON", "")
arcpy.CalculateField_management(outmldl, "LINEAR_FT", "!shape.length@feet!", "PYTHON", "")
arcpy.CalculateField_management(outmldl, "SIZE", "'" + Pipe_Diameter + "'", "PYTHON", "")
arcpy.CalculateField_management(outmldl, "CLIENT", "'" + Client + "'", "PYTHON", "")
arcpy.CalculateField_management(outmldl, "CLIENT_REF", "'" + Xcel_Billing_Code + "'", "PYTHON", "")
arcpy.CalculateField_management(outmldl, "COUNTY1", "'" + COUNTY_1 + "'", "PYTHON", "")
arcpy.CalculateField_management(outmldl, "COUNTY2", "'" + COUNTY_2 + "'", "PYTHON", "")
arcpy.CalculateField_management(outmldl, "STATE", "'" + STATE + "'", "PYTHON", "")
arcpy.CalculateField_management(outmldl, "PROJECTION", "'" + Projection + "'", "PYTHON", "")
arcpy.CalculateField_management(outmldl, "COMPLETED", "'" + Date_Completed + "'", "PYTHON", "")
arcpy.CalculateField_management(outmldl, "NOTES", "'" + Notes + "'", "PYTHON", "")
arcpy.CalculateField_management(outmldl, "FILE_NAME", "'" + ENE_File_Name + "'", "PYTHON", "")
arcpy.CalculateField_management(outmldl, "PHASE", "'" + Phase + "'", "PYTHON", "")

#Save the feature class from memory to the GDB
arcpy.FeatureClassToFeatureClass_conversion(outmldl, Xcel_Alignments_gdb, ENE_File_Name, "")
arcpy.Append_management(, Combined_Xcel_Alignments, "NO_TEST","","" )

#Creates the alignment shapefile and sends it to the shapefile folder and layer
A_Layer = arcpy.MakeFeatureLayer_management(outmldl, "Alignment")
arcpy.CopyFeatures_management(A_Layer, path1 + "\\" + ENE_File_Name)

#Delete object in memory
arcpy.Delete_management(in_memory)



###Process: Buffer
#Change the work space location
#env.workspace = 'I://DN//GIS Resources//Feature Layers//Xcel//Xcel Buffers.gdb'
m = "in_memory/" + Buffer_Name;

#create in memory object
outmb = arcpy.FeatureClassToFeatureClass_conversion(ml, in_memory, Dissolve_Name, "")
#Create Buffer
out_buffer = arcpy.Buffer_analysis(outmb, m , Buffer_size, "FULL", "ROUND", "LIST", "", "PLANAR")

#out_buffer = arcpy.ApplySymbologyFromLayer_management(out_buffer, Buffer_symbology)
arcpy.AddField_management(out_buffer, "NAME", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(out_buffer, "SENDER", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(out_buffer, "M_CODE", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(out_buffer, "EFF_DATE", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(out_buffer, "EXP_DATE", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(out_buffer, "COUNTY_1", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(out_buffer, "BUFFER", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(out_buffer, "STATE", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(out_buffer, "COUNTY_2", "TEXT", "", "", "50", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(outml, "PHASE", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

#Calculate field
arcpy.CalculateField_management(out_buffer, "NAME", "'" + kmzbuffername + "'", "PYTHON", "")
arcpy.CalculateField_management(out_buffer, "SENDER", "'" + SENDER + "'", "PYTHON", "")
arcpy.CalculateField_management(out_buffer, "M_CODE", "'0'", "PYTHON", "")
arcpy.CalculateField_management(out_buffer, "EFF_DATE", "'IMMEDIATELY'", "PYTHON", "")
arcpy.CalculateField_management(out_buffer, "EXP_DATE", "'NEVER'", "PYTHON", "")
arcpy.CalculateField_management(out_buffer, "COUNTY_1", "'"+ COUNTY_1 + "'", "PYTHON", "")
arcpy.CalculateField_management(out_buffer, "COUNTY_2", "'" + COUNTY_2 + "'", "PYTHON", "")
arcpy.CalculateField_management(out_buffer, "STATE", "'" + STATE + "'", "PYTHON", "")
arcpy.CalculateField_management(out_buffer, "BUFFER", "'" + Buffer_size + "'", "PYTHON", "")
arcpy.CalculateField_management(outmldl, "PHASE", "'" + Phase + "'", "PYTHON", "")


#final_buffer = arcpy.ApplySymbologyFromLayer_management(out_buffer, buffer_symbology)
f_output = arcpy.FeatureClassToFeatureClass_conversion(out_buffer, Buffer_gdb, Buffer_Name, "")



#Creates the buffer shapefile and sends it to the shapefile folder
buffer_sym_l = arcpy.MakeFeatureLayer_management(out_buffer, "Buffer")
arcpy.CopyFeatures_management(buffer_sym_l, path1 + "\\" + Buffer_Name)
arcpy.Append_management(Buffer_gdb + "/" + Buffer_Name, Combined_Xcel_Alignments, "NO_TEST","","" )

#Clean memory
arcpy.Delete_management(in_memory)

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
##Change Symbology and Create KMZ from MXD document. 


env.workspace = path1 + "\\" 
temp1 = ENE_File_Name
temp2 = Buffer_Name

#Create shapefile
file_a1 = arcpy.MakeFeatureLayer_management(ENE_File_Name + ".shp", temp1)
file_b1 = arcpy.MakeFeatureLayer_management(Buffer_Name + ".shp", temp2)

#Create layer files
file_a2 = arcpy.SaveToLayerFile_management(file_a1, ENE_File_Name + ".lyr", "RELATIVE")
file_b2 = arcpy.SaveToLayerFile_management(file_b1, Buffer_Name + ".lyr", "RELATIVE")

#Copies symbology from template file
s_a = arcpy.ApplySymbologyFromLayer_management(file_a2, "I:\DN\GIS Resources\Feature Layers\Xcel\Xcel Symbology Template\Xcel_Alignment_symbology.lyr")
s_l = arcpy.ApplySymbologyFromLayer_management(file_b2, "I:\DN\GIS Resources\Feature Layers\Xcel\Xcel Symbology Template\Xcel_Buffer_symbology.lyr")

#opens mxd template and takes the layout and layers from work environment for the user to make adjustements before finalizing product.
if Layout_mxd == 'Xcel_AsBuilt_Landscape':
    Layout_mxd = r'I:\DN\GIS Resources\Tools\As-Built and IFB and IFC Submittal Resources\MXD Document Templates\Xcel_AsBuilt_Landscape.mxd'

if Layout_mxd == 'Xcel_AsBuilt_Landscape_MULTI_PAGE':
    Layout_mxd = r'I:\DN\GIS Resources\Tools\As-Built and IFB and IFC Submittal Resources\MXD Document Templates\Xcel_AsBuilt_Landscape_MULTI-PAGE.mxd'
if Layout_mxd == 'Xcel_AsBuilt_Landscape_MULTI_PAGE2': 
    Layout_mxd = r'I:\DN\GIS Resources\Tools\As-Built and IFB and IFC Submittal Resources\MXD Document Templates\Xcel_AsBuilt_Landscape_MULTI-PAGE.mxd'
if Layout_mxd == 'Xcel_AsBuilt_Landscape_TWO_FRAMES':
    Layout_mxd =  r'I:\DN\GIS Resources\Tools\As-Built and IFB and IFC Submittal Resources\MXD Document Templates\Xcel_AsBuilt_Landscape_TWO_FRAMES.mxd'
if Layout_mxd == 'Xcel_AsBuilt_Portrait':
    Layout_mxd = r'I:\DN\GIS Resources\Tools\As-Built and IFB and IFC Submittal Resources\MXD Document Templates\Xcel_AsBuilt_Portrait.mxd'
if Layout_mxd == 'Xcel_IFC_Landscape': 
    Layout_mxd = r'I:\DN\GIS Resources\Tools\As-Built and IFB and IFC Submittal Resources\MXD Document Templates\Xcel_IFC_Landscape.mxd'
if Layout_mxd == 'Xcel_IFC_Landscape_TWO_FRAMES':
    Layout_mxd = r'I:\DN\GIS Resources\Tools\As-Built and IFB and IFC Submittal Resources\MXD Document Templates\Xcel_IFC_Landscape_TWO_FRAMES.mxt'
if Layout_mxd == 'Xcel_IFC_Portrait':
    Layout_mxd = r'I:\DN\GIS Resources\Tools\As-Built and IFB and IFC Submittal Resources\MXD Document Templates\Xcel_IFC_Portrait.mxd'
if Layout_mxd == 'Xcel_Minnesota_AsBuilt_Landscape':
    Layout_mxd = r'I:\DN\GIS Resources\Tools\As-Built and IFB and IFC Submittal Resources\MXD Document Templates\Xcel_Minnesota_AsBuilt_Landscape.mxd'
if Layout_mxd == 'Xcel_Minnesota_AsBuilt_Portrait':
    Layout_mxd = r'I:\DN\GIS Resources\Tools\As-Built and IFB and IFC Submittal Resources\MXD Document Templates\Xcel_Minnesota_AsBuilt_Portrait.mxd'
if Layout_mxd == 'Xcel_Minnesota_IFC_Portrait':
    Layout_mxd = r'I:\DN\GIS Resources\Tools\As-Built and IFB and IFC Submittal Resources\MXD Document Templates\Xcel_Minnesota_IFC_Portrait.mxd'

    
mxd = arcpy.mapping.MapDocument(Layout_mxd)
df = arcpy.mapping.ListDataFrames(mxd, "*")[0]
walk = arcpy.da.Walk(env.workspace, datatype = "Layer")

#Adds layers to created mxd
for dirpath, dirnames, filenames in walk:  
    for filename in filenames:  
        layerfile = os.path.join(dirpath, filename)  
        addlayer = arcpy.mapping.Layer(layerfile)  
        arcpy.mapping.AddLayer(df, addlayer, "BOTTOM") 

#renames the layers for the legend
layers = arcpy.mapping.ListLayers(mxd)

for lyr in layers: 
    if lyr.name == ENE_File_Name:
        lyr.name = "Proposed " + Pipe_Diameter + '"' + " Natural Gas Pipeline"
    else: 
        lyr.name = Buffer_size + "' Buffer"
        
        
for elem in arcpy.mapping.ListLayoutElements(mxd,'TEXT_ELEMENT'):
    elem.text = elem.text.replace('Project:', "Project: " + Pipe_Diameter + '" ' + Project_Name)
    elem.text = elem.text.replace('Xcel Work Order:', "Xcel Work Order: " + Xcel_Billing_Code)
    
#Save result to MXD
fmxd = mxd.saveACopy(Alignment_Input + ENE_File_Name + ".mxd")

##KMZ Conversion
fmxd = arcpy.mapping.MapDocument(Alignment_Input + ENE_File_Name + ".mxd")
df = arcpy.mapping.ListDataFrames(fmxd)[0].name  
outputKML = path2 + "\\" + Name_join.replace("_"," ") + ".kmz"
mapScale = 0
composite = 'NO_COMPOSITE'  
vector = 'VECTOR_TO_IMAGE'  
extent = ''  
imageSize = 1024
dpi = 120  
ignore_z = '' 

arcpy.MapToKML_conversion(fmxd.filePath, df, outputKML, mapScale, composite, vector, extent, imageSize, dpi, ignore_z )

arcpy.LayerToKML_conversion(s_a, path2 +"\\" + ENE_File_Name.replace("_"," ") + ".kmz" )
arcpy.LayerToKML_conversion(s_l, path2 +"\\" + Buffer_Name.replace("_"," ") + ".kmz" )

arcpy.Delete_management(in_memory)

#os.system("TASKKILL /F /IM ArcMap.exe")
os.startfile(Alignment_Input + ENE_File_Name + ".mxd")
# Call the function to retrieve all files and folders of the assigned directory

print datetime.now() - startTime 

sys.exit()
