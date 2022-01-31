
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 20 13:40:01 2017
@author: HB69954
"""

import numpy as np
import os
#import pywin32
import re
import matplotlib.dates as mdates
import glob

#struct DASFileHeader_3
#{
#	int64_t Preamble;
#	int16_t Version;
#	int16_t Mode;
#	int8_t SoftwareName[32];
#	int32_t Content;
#	int64_t BlockSize;
#	int32_t FrameOrientation;
#	int32_t FrameDataType;
#	int64_t FrameOffset;
#	int32_t QualityOrientation;
#	int32_t QualityDataType;
#	int64_t QualityOffset;
#	int64_t QualityBlockSize;
#	int16_t Year;
#	int16_t Month;
#	int16_t Day;
#	int16_t Hour;
#	int16_t Minute;
#	int16_t Second;
#	int32_t Microsecond;
#	int16_t TZOffset;
#	double SamplingRate;
#	int64_t FrameCapacity;
#	int64_t NumberOfFrames;
#	int64_t Compression;
#	int32_t NumberOfChannels;
#	int64_t ZonesOffset;
#	int8_t Reserved[378];
#	int16_t LocalYear;
#	int16_t LocalMonth;
#	int16_t LocalDay;
#	int16_t LocalHour;
#	int16_t LocalMinute;
#	int16_t LocalSecond;
#	int32_t LocalMicrosecond;
#};

#struct DASFileHeader_4
#{
#	int64_t Preamble;
#	int16_t Version;
#	int16_t Mode;
#	int8_t SoftwareName[32];
#	int32_t Content;
#	int64_t BlockSize;
#	int32_t FrameOrientation;
#	int32_t FrameDataType;
#	int64_t FrameOffset;
#	int32_t QualityOrientation;
#	int32_t QualityDataType;
#	int64_t QualityOffset;
#	int64_t QualityBlockSize;
#	int16_t Year;
#	int16_t Month;
#	int16_t Day;
#	int16_t Hour;
#	int16_t Minute;
#	int16_t Second;
#	int32_t Microsecond;
#	int16_t TZOffset;
#	double SamplingRate;
#	int64_t FrameCapacity;
#	int64_t NumberOfFrames;
#	int64_t Compression;
#	int32_t NumberOfChannels;
#	int64_t ZonesOffset;
#	int64_t DepthCalibrationOffset;
#	int64_t NominalDepthOffset;
#	int64_t MeasuredDepthOffset;
#	int8_t Reserved[330];
#	double DigitizerRate;
#	double DelayCoilLength;
#	double IndexOfRefraction;
#	int16_t LocalYear;
#	int16_t LocalMonth;
#	int16_t LocalDay;
#	int16_t LocalHour;
#	int16_t LocalMinute;
#	int16_t LocalSecond;
#	int32_t LocalMicrosecond;
#};

# global variables 
# TODO: verify python gets correct byte allignment - based on c++ #pragma pack(push, 1) ... #pragma pack(pop)
DASFileHeader_3 = np.dtype([('Preamble',np.int64),
        ('Version',np.int16),
        ('Mode',np.int16),
        ('SoftwareName',np.int8,32),
        ('Content',np.int32),
        ('BlockSize',np.int64),
        ('FrameOrientation',np.int32),
        ('FrameDataType',np.int32),
        ('FrameOffset',np.int64),
        ('QualityOrientation',np.int32),
        ('QualityDataType',np.int32),
        ('QualityOffset',np.int64),
        ('QualityBlockSize',np.int64),
        ('Year',np.int16),
        ('Month',np.int16),
        ('Day',np.int16),
        ('Hour',np.int16),
        ('Minute',np.int16),
        ('Second',np.int16),
        ('Microsecond',np.int32),
        ('TZOffset',np.int16),
        ('SamplingRate',np.dtype('d')),
        ('FrameCapacity',np.int64),
        ('NumberOfFrames',np.int64),
        ('Compression',np.int64),
        ('NumberOfChannels',np.int32),
        ('ZonesOffset',np.int64),
        ('Reserved',np.int8,378),
        ('LocalYear',np.int16),
        ('LocalMonth',np.int16),
        ('LocalDay',np.int16),
        ('LocalHour',np.int16),
        ('LocalMinute',np.int16),
        ('LocalSecond',np.int16),
        ('LocalMicrosecond',np.int32)])

DASFileHeader_4 = np.dtype([('Preamble',np.int64),
        ('Version',np.int16),
        ('Mode',np.int16),
        ('SoftwareName',np.int8,32),
        ('Content',np.int32),
        ('BlockSize',np.int64),
        ('FrameOrientation',np.int32),
        ('FrameDataType',np.int32),
        ('FrameOffset',np.int64),
        ('QualityOrientation',np.int32),
        ('QualityDataType',np.int32),
        ('QualityOffset',np.int64),
        ('QualityBlockSize',np.int64),
        ('Year',np.int16),
        ('Month',np.int16),
        ('Day',np.int16),
        ('Hour',np.int16),
        ('Minute',np.int16),
        ('Second',np.int16),
        ('Microsecond',np.int32),
        ('TZOffset',np.int16),
        ('SamplingRate',np.dtype('d')),
        ('FrameCapacity',np.int64),
        ('NumberOfFrames',np.int64),
        ('Compression',np.int64),
        ('NumberOfChannels',np.int32),
        ('ZonesOffset',np.int64),
        ('DepthCalibrationOffset',np.int64),
        ('NominalDepthOffset',np.int64),
        ('MeasuredDepthOffset',np.int64),
        ('Reserved',np.int8,330),
        ('DigitizerRate',np.dtype('d')),
        ('DelayCoilLength',np.dtype('d')),
        ('IndexOfRefraction',np.dtype('d')),
        ('LocalYear',np.int16),
        ('LocalMonth',np.int16),
        ('LocalDay',np.int16),
        ('LocalHour',np.int16),
        ('LocalMinute',np.int16),
        ('LocalSecond',np.int16),
        ('LocalMicrosecond',np.int32)])
 
dataTypeDict = {0: (0, 1, np.dtype('<i1')),
                1: (12, 3, np.dtype('<i2')),
                2: (4, 2, np.dtype('<i2')),
                3: (2, 1, np.dtype('<i2')),
                4: (2, 1, np.dtype('<i2')),
                5: (4, 1, np.dtype(np.float32)),
                6: (4, 1, np.dtype(np.float32)),
                7: (4, 1, np.dtype(np.float32)),
                8: (4, 1, np.dtype(np.float32)),
                9: (4, 1, np.dtype(np.float32)),
                10: (4, 1, np.dtype(np.float32)),
                11: (4, 1, np.dtype(np.float32)),
                12: (4, 4, np.dtype('<i2')),
                13: (4, 1, np.dtype(np.float32)),
                14: (4, 1, np.dtype(np.float32)),
                15: (4, 1, np.dtype(np.float32)),
                16: (16, 4, np.dtype(np.float32)),
                17: (2, 1, np.dtype(np.float32)),
                18: (2, 1, np.dtype(np.float32)),
                19: (8, 2, np.dtype(np.float32)),
                20: (8, 2, np.dtype(np.float32)),
                21: (8, 4, np.dtype('<i2')),
                22: (4, 2, np.dtype('<i2')),
                23: (8, 4, np.dtype('<i2')),
                24: (4, 1, np.dtype(np.float32)),
                25: (4, 1, np.dtype(np.float32)),
                26: (4, 1, np.dtype(np.float32)),
                27: (4, 1, np.dtype(np.float32)),
                28: (4, 1, np.dtype(np.float32)),
                29: (4, 1, np.dtype(np.float32)),
                30: (4, 1, np.dtype(np.float32))}

frameDataTypeEnum = {
                    0: ("NONE", "No data"),
                    1: ("ABC_INT16", "Triple sensor raw data"),
                    2: ("IQ_INT16", "Each sample represents an I & Q pair."),
                    3: ("DPHASE_INT16", "Differential phase, scaled by 10,430 (2^15-1 / π) to span the dynamic range of the 16-bit integer"),
                    4: ("AMPLITUDE_INT16", ""),
                    5: ("AMPLITUDE_FLOAT", ""),
                    6: ("PHASE_FLOAT", ""),
                    7: ("INTENSITY_FLOAT", "Also used for phase power"),
                    8: ("VSP_SINGLE_SWEEP_FLOAT", "deprecated"),
                    9: ("VSP_STACKED_SWEEP_FLOAT", "deprecated"),
                    10: ("FLOW_FLOAT", "deprecated"),
                    11: ("INTENSITY_SPECTROGRAM_FLOAT", "Complete frequency domain data"),
                    12: ("ABCD_INT16", "Quad sensor raw data"),
                    13: ("FLOW_INJECTION", "deprecated"),
                    14: ("FLOW_RELATIVE", "deprecated"),
                    15: ("FLOW_PRODUCTION", "deprecated"),
                    16: ("AMPLITUDE_QUAD", "Quality data stored as a composite of four values: average, minimum, maximum amplitude, and amplitude standard deviation, respectively"),
                    17: ("DPHASE_FLOAT", "Differential phase"),
                    18: ("MINMAX_FLOAT", "deprecated"),
                    19: ("IQ_FLOAT", "Each sample represents an I & Q pair"),
                    20: ("COMPLEX_FLOAT", "deprecated"),
                    21: ("ABCD_INT16_RAW", "Differential phase"),
                    22: ("IQ_INT16_RAW", "Differential phase"),
                    23: ("IQIQ_INT16_RAW", "Differential phase"),
                    24: ("REAL_FLOAT", "Differential phase"),
                    25: ("FLOW_EROSION", "deprecated"),
                    26: ("STATIC_PHASE_FLOAT", "Differential phase integrated from 0 over specified block size"),
                    27: ("PHASE_VARIANCE_FLOAT", "Standard deviation of phase"),
                    28: ("PHASE_POWER_FLOAT", "Frequency domain from only selected bands"),
                    29: ("QUALITY_FLOAT", "Quality (amplitude) data"),
                    30: ("STRAIN_FLOAT", "Differential phase integrated from 0 over the specified block size scaled with an optical strain coefficient")}

def readDasBinary(fileName):
    """
    Read a Pinnacle DAS binary file and return a 2-tuple (header, frame data) for a v3 Pinnacle DAS binary 
    or 3-tuple (header, frame data, measured depth) for a v4 Pinnacle DAS binary 

    Args:
        fileName (string): full file path to a v3 or v4 Pinnacle DAS binary file (.bin extension)

    Returns:
        dasHeader: file header, typeof DASFileHeader_3 or DASFileHeader_4 depending on binary file version
        dasFrameData: numpy ndarray of DAS frame data. the class and shape of frameData will depend on the frame datatype indicated in the 
            header (see dataTypeDict for more information)
        measuredDepth: (header version 4 only) array of calibrated measured depth values with shape (NumberOfChannels x 1)
    """
    headerVersion = checkHeaderVersion(fileName)
    if headerVersion == 3:
        return readV3DasBinary(fileName)
    elif headerVersion == 4:
        return readV4DasBinary(fileName)
    else:
        raise ValueError("Unsupported DAS Header Version")

# TODO: add zones, quality
def readV3DasBinary(fileName):
    """
    Read a Pinnacle v3 DAS binary and return a 2-tuple (header, frame data)

    Args:
        fileName (string): full file path to a v3 Pinnacle DAS binary file (.bin extension)

    Returns:
        dasHeader: file header, typeof DASFileHeader_3
        dasFrameData: numpy ndarray of DAS frame data. the class and shape of frameData will depend on the frame datatype indicated in the 
            header (see dataTypeDict for more information)
    """
    dasHeader = np.fromfile(fileName, dtype=DASFileHeader_3, count=1)
    numberOfFrames = dasHeader['NumberOfFrames'][0]
    numberOfChannels = dasHeader['NumberOfChannels'][0]
    # zonesOffset = dasHeader['ZonesOffset'][0]
    frameOffset = dasHeader['FrameOffset'][0]
    frameDataType = dasHeader['FrameDataType'][0]

    # get number of bytes to read from array size and data type
    frameDataInfo = dataTypeDict[frameDataType]
    frameDataSize = frameDataInfo[0]
    frameDataArrayLeadingDim = frameDataInfo[1]
    frameDataNumpyDataType = frameDataInfo[2]
    if frameDataArrayLeadingDim == 1:
        #frameDataShape = (numberOfFrames, numberOfChannels)
        frameDataShape = (numberOfChannels, numberOfFrames)
    else:
        #frameDataShape = (frameDataArrayLeadingDim, numberOfFrames, numberOfChannels)
        frameDataShape = (numberOfChannels, numberOfFrames, frameDataArrayLeadingDim)

    nByte = numberOfFrames * numberOfChannels * frameDataSize

    with open(fileName, 'rb') as fptr:
        # read frame data from binary
        fptr.seek(frameOffset, os.SEEK_SET)
        frameDataBytes = fptr.read(nByte)
        frameDataFlat = np.frombuffer(frameDataBytes, dtype=frameDataNumpyDataType)
        dasFrameData = np.reshape(frameDataFlat, newshape=frameDataShape)
    return dasHeader, dasFrameData

# TODO: add zones, quality, nominal depth, depth calibration
def readV4DasBinary(fileName):
    """
    Read a Pinnacle v4 DAS binary and return a 3-tuple (header, frame data, measured depth)
    The class and shape of frameData will depend on the frame datatype indicated in the 
    header (see dataTypeDict for more information)

    Args:
        fileName (string): full file path to a v4 Pinnacle DAS binary file (.bin extension)

    Returns:
        dasHeader: file header, typeof DASFileHeader_4
        dasFrameData: numpy ndarray of DAS frame data. the class and shape of frameData will depend on the frame datatype indicated in the 
            header (see dataTypeDict for more information)
        measuredDepth: array of calibrated measured depth values with shape (NumberOfChannels x 1)
    """
    dasHeader = np.fromfile(fileName, dtype=DASFileHeader_4, count=1)
    numberOfFrames = dasHeader['NumberOfFrames'][0]
    numberOfChannels = dasHeader['NumberOfChannels'][0]
    # zonesOffset = dasHeader['ZonesOffset'][0]
    frameOffset = dasHeader['FrameOffset'][0]
    frameDataType = dasHeader['FrameDataType'][0]
    measuredDepthOffset = dasHeader['MeasuredDepthOffset'][0]
    
    qualityOffset = dasHeader['QualityOffset'][0]
    qualityBlockSize = dasHeader['QualityBlockSize'][0]
    qualityDataType = dasHeader['QualityDataType'][0]
    qualityDataInfo = dataTypeDict[qualityDataType]
    qualityDataSize = qualityDataInfo[0]
    qualityDataNumpyDataType = qualityDataInfo[2]
    nQualityByte = numberOfFrames * numberOfChannels * qualityDataSize // qualityBlockSize
    # TODO: quality orientation
    #qualityDataShape = (4, numberOfFrames // qualityBlockSize, numberOfChannels)
    qualityDataShape = (numberOfChannels, numberOfFrames // qualityBlockSize, 4)
        
    # get number of bytes to read from array size and data type
    frameDataInfo = dataTypeDict[frameDataType]
    frameDataSize = frameDataInfo[0]
    frameDataArrayLeadingDim = frameDataInfo[1]
    frameDataNumpyDataType = frameDataInfo[2]
    if frameDataArrayLeadingDim == 1:
        #frameDataShape = (numberOfFrames, numberOfChannels)
        frameDataShape = (numberOfChannels, numberOfFrames)
    else:
        #frameDataShape = (frameDataArrayLeadingDim, numberOfFrames, numberOfChannels)
        frameDataShape = (numberOfChannels, numberOfFrames, frameDataArrayLeadingDim)

    nByte = numberOfFrames * numberOfChannels * frameDataSize
    nMeasuredDepthByte = numberOfChannels * 4

    with open(fileName, 'rb') as fptr:
        # read measured depth data from binary
        fptr.seek(measuredDepthOffset, os.SEEK_SET)
        measuredDepthBuffer = fptr.read(nMeasuredDepthByte)
        measuredDepthData = np.frombuffer(measuredDepthBuffer, dtype=np.float32)

        # read frame data from binary
        fptr.seek(frameOffset, os.SEEK_SET)
        frameDataBytes = fptr.read(nByte)
        frameDataFlat = np.frombuffer(frameDataBytes, dtype=frameDataNumpyDataType)
        dasFrameData = np.reshape(frameDataFlat, newshape=frameDataShape)

        # read quality data from DAS binary
        fptr.seek(qualityOffset, os.SEEK_SET)
        qualityDataBytes = fptr.read(nQualityByte)
        qualityDataFlat = np.frombuffer(qualityDataBytes, dtype=qualityDataNumpyDataType)
        dasQualityData = np.reshape(qualityDataFlat, qualityDataShape)
        
    return dasHeader, dasFrameData, measuredDepthData, dasQualityData


def walkDasDataTree(dataRoot, searchExpression):
    """
    Return a list of directories contained in dataRoot and its subdirectories matching searchExpression

    Args:
        dataRoot (string): full path to root directory for search
        searchExpression (string): string pattern to match during directory search (e.g. dPhase, Phase Power, etc)
    """
    if __debug__:
        print("Searching Directory: " + dataRoot)
    childDirectories = filter(lambda z: os.path.isdir(z), glob.glob(dataRoot + "\\*")) 
    ans = [None]
    for child in childDirectories:
        if child.find("\\UTC_Y") != -1:
            continue
        elif child.find(searchExpression) != -1:
            if __debug__:
                print("Match: " + child)
            ans.append(child)
        else:
            ans += walkDasDataTree(child, searchExpression)
    if len(ans) is 0:
        return None
    return list(filter(None, ans))

def findIQDirectories(dataRoot):
    """Return a list of in-phase/quadrature (IQ) data directories contained in dataRoot and its subdirectories"""
    return walkDasDataTree(dataRoot, "IQ Data")

def findDPhaseDirectories(dataRoot):
    """Return a list of differential phase (dPhase) data directories contained in dataRoot and its subdirectories"""
    return walkDasDataTree(dataRoot, "dPhase") + walkDasDataTree(dataRoot, "RawData")

def findStaticPhaseDirectories(dataRoot):
    """Return a list of static phase data directories contained in dataRoot and its subdirectories"""
    return walkDasDataTree(dataRoot, "Phase BS")

def findPhasePowerDirectories(dataRoot):
    """Return a list of phase power data directories contained in dataRoot and its subdirectories"""
    return walkDasDataTree(dataRoot, "Phase Power BS")

def findPhaseVarianceDirectories(dataRoot):
    """Return a list of phase variance data directories contained in dataRoot and its subdirectories"""
    return walkDasDataTree(dataRoot, "Phase Variance BS") + walkDasDataTree(dataRoot, "WaterfallData_PV_") + walkDasDataTree(dataRoot, "WaterfallIntensityData")

#def findSomeDasJobs(dataRoot):
#    dPhaseDataList = glob.glob(dirName+"\\*dPhase Data*", recursive=True)
#    RawDataList = glob.glob(dirName+"\\*RawData*", recursive=True)
#    IQDataList = glob.glob(dirName+"\\*IQ Data*")

def dirRecursive(rootDir):
    """Return a list of DAS binary files (.bin extension) contained in rootDir and its subdirectories"""
    fileList = list()
    for (dir, _, files) in os.walk(rootDir):
         for f in files:
             path = os.path.join(dir, f)
             if os.path.exists(path):
                 fileList.append(path)
                 
    fList = list()
    prog = re.compile('.bin$')
    for k in range(len(fileList)):
        binMatch = prog.search(fileList[k])
        if binMatch:
            fList.append(binMatch.string)
            
    return fList

def getFileTimeStamps(fileList):
    """
    Get timestamps for each DAS binary file in fileList

    Args:
        fileList (:obj:`list` of :obj:`str`): list of strings containing either DAS binary file names or full file paths

    Returns:
        fileTimeStamps (:obj:`list` of :obj:`float`): list of file time stamps in matplotlib epoch time (since 1970-01-01 UTC)

    """
    prog = re.compile('(\d{8}T\d{6})_(\d{6})Z\.bin$')
    return [mdates.datestr2num(ts.group(1)) + (float(ts.group(2)) / 86400000000.0) for ts in [prog.search(f) for f in fileList]]

def checkHeaderVersion(fileName):
    """
    Get header version from a Pinnacle DAS binary file (.bin extension)

    Args:
        fileName (string): full file path to DAS binary file

    Returns:
        headerVersion (int): Pinnacle DAS binary version (currently only v3 and v4 are supported in pyReadPinnacleDasBinary)
    """
    with open(fileName, 'rb') as fptr:
        fptr.seek(8, os.SEEK_SET)
        headerVersion = int.from_bytes(fptr.read(2), byteorder='little')
        if __debug__:
            print(fileName + ": Header Version " + str(headerVersion))
        return headerVersion

def displayHelpDocumentation():
    print("Hint: Shift + Alt + F5 Executes .py File in Visual Studio Interactive Python\n")
    ## custom data types
    print("Documentation for pyReadPinnacleDasBinary data types")
    print("######################################## Frame DataTypes Explained ###########################################")
    for k in frameDataTypeEnum.keys():
        print("Frame DataType " + str(k) + ": " + frameDataTypeEnum[k][0])
        desc = frameDataTypeEnum[k][1]
        if desc is not "":
            print("\t" + frameDataTypeEnum[k][1] + "\n")
        else:
            print("\n")
    print("In practice, it will be highly uncommon to see FrameDataType other than 2, 3, 7 or 30.\n")
    print("######################################## DASFileHeader_3 dtype ###############################################")
    print("numpy dtype containing v3 Pinnacle DAS binary file header information with the following fields:")
    for fn in DASFileHeader_3.names:
        print("\t" + fn)
    print("\n")
    print("######################################## DASFileHeader_4 dtype ###############################################")
    print("numpy dtype containing v4 Pinnacle DAS binary file header information")
    print("Contains all the fields from a v3 header, but with different byte allignment and additional header fields:")
    for fn in (set(DASFileHeader_3.names) ^ set(DASFileHeader_4.names)):
        print("\t" + fn)
    print("\n")
    print("DASFileHeader information is accessed by name. e.g. `samplingRate = dasHeader['SamplingRate'][0]`\n\n")
    ## methods
    print("Documentation for pyReadPinnacleDasBinary functions")
    print("######################################## checkHeaderVersion ##################################################")
    print(checkHeaderVersion.__doc__ + "\n")
    print("######################################## dirRecursive ########################################################")
    print(dirRecursive.__doc__ + "\n")
    print("######################################## findDPhaseDirectories ###############################################")
    print(findDPhaseDirectories.__doc__ + "\n")
    print("######################################## findIQDirectories ###################################################")
    print(findIQDirectories.__doc__ + "\n")
    print("######################################## findPhasePowerDirectories ###########################################")
    print(findPhasePowerDirectories.__doc__ + "\n")
    print("######################################## findPhaseVarianceDirectories ########################################")
    print(findPhaseVarianceDirectories.__doc__ + "\n")
    print("######################################## findStaticPhaseDirectories ##########################################")
    print(findStaticPhaseDirectories.__doc__ + "\n")
    print("######################################## readV3DasBinary #####################################################")
    print(readV3DasBinary.__doc__ + "\n")
    print("######################################## readV4DasBinary #####################################################")
    print(readV4DasBinary.__doc__ + "\n")
    print("######################################## walkDasDataTree #####################################################")
    print(walkDasDataTree.__doc__ + "\n")
    print("######################################## readDasBinary #######################################################")
    print(readDasBinary.__doc__ + "\n")
    print("######################################## getFileTimeStamps ###################################################")
    print(getFileTimeStamps.__doc__ + "\n")

if __name__ == "__main__":
    displayHelpDocumentation()
