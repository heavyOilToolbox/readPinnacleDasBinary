
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

def readDasBinary(fileName):
    headerVersion = checkHeaderVersion(fileName)
    if headerVersion == 3:
        return readV3DasBinary(fileName)
    elif headerVersion == 4:
        return readV4DasBinary(fileName)
    else:
        raise ValueError("Unsupported DAS Header Version")

# for a v3 das binary return a tuple of (dasHeader, frameData)
# TODO: add zones, quality
def readV3DasBinary(fileName):
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
        frameDataShape = (numberOfFrames, numberOfChannels)
    else:
        frameDataShape = (frameDataArrayLeadingDim, numberOfFrames, numberOfChannels)

    nByte = numberOfFrames * numberOfChannels * frameDataSize

    with open(fileName, 'rb') as fptr:
        # read frame data from binary
        fptr.seek(frameOffset, os.SEEK_SET)
        frameDataBytes = fptr.read(nByte)
        frameDataFlat = np.frombuffer(frameDataBytes, dtype=frameDataNumpyDataType)
        dasFrameData = np.reshape(frameDataFlat, newshape=frameDataShape)
    return dasHeader, dasFrameData

# for a v4 das binary return a tuple of (dasHeader, frameData, measuredDepth)
# TODO: add zones, quality, nominal depth, depth calibration
def readV4DasBinary(fileName):
    dasHeader = np.fromfile(fileName, dtype=DASFileHeader_4, count=1)
    numberOfFrames = dasHeader['NumberOfFrames'][0]
    numberOfChannels = dasHeader['NumberOfChannels'][0]
    # zonesOffset = dasHeader['ZonesOffset'][0]
    frameOffset = dasHeader['FrameOffset'][0]
    frameDataType = dasHeader['FrameDataType'][0]
    measuredDepthOffset = dasHeader['MeasuredDepthOffset'][0]

    # get number of bytes to read from array size and data type
    frameDataInfo = dataTypeDict[frameDataType]
    frameDataSize = frameDataInfo[0]
    frameDataArrayLeadingDim = frameDataInfo[1]
    frameDataNumpyDataType = frameDataInfo[2]
    if frameDataArrayLeadingDim == 1:
        frameDataShape = (numberOfFrames, numberOfChannels)
    else:
        frameDataShape = (frameDataArrayLeadingDim, numberOfFrames, numberOfChannels)

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

    return dasHeader, dasFrameData, measuredDepthData


def walkDasDataTree(dataRoot, searchExpression):
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
    return walkDasDataTree(dataRoot, "IQ Data")

def findDPhaseDirectories(dataRoot):
    return walkDasDataTree(dataRoot, "dPhase") + walkDasDataTree(dataRoot, "RawData")

def findStaticPhaseDirectories(dataRoot):
    return walkDasDataTree(dataRoot, "Phase BS")

def findPhasePowerDirectories(dataRoot):
    return walkDasDataTree(dataRoot, "Phase Power BS")

def findPhaseVarianceDirectories(dataRoot):
    return walkDasDataTree(dataRoot, "Phase Variance BS") + walkDasDataTree(dataRoot, "WaterfallData_PV_") + walkDasDataTree(dataRoot, "WaterfallIntensityData")

#def findSomeDasJobs(dataRoot):
#    dPhaseDataList = glob.glob(dirName+"\\*dPhase Data*", recursive=True)
#    RawDataList = glob.glob(dirName+"\\*RawData*", recursive=True)
#    IQDataList = glob.glob(dirName+"\\*IQ Data*")

def dirRecursive(dirName):
    fileList = list()
    for (dir, _, files) in os.walk(dirName):
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
    prog = re.compile('(\d{8}T\d{6})_(\d{6})Z\.bin$')
    return [mdates.datestr2num(ts.group(1)) + (float(ts.group(2)) / 86400000000.0) for ts in [prog.search(f) for f in fileList]]

def checkHeaderVersion(fileName):
    with open(fileName, 'rb') as fptr:
        fptr.seek(8, os.SEEK_SET)
        headerVersion = int.from_bytes(fptr.read(2), byteorder='little')
        if __debug__:
            print(fileName + ": Header Version " + str(headerVersion))
        return headerVersion

if __name__ == "__main__":
    print("Hint: Shift + Alt + F5 Executes .py File in Visual Studio")