
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
 
#def bin2np(fileName, channelNum, frameNum):
    
#    #Convert DAS data into numpy array
#    #Input: .bin das file
    
#    #re-read das binary given channel/frame information
#    dasDataType = np.dtype([('preamb',np.int64),
#        ('version',np.int16),
#        ('mode',np.int16),
#        ('softwareame',np.int8,32),
#        ('content',np.int32),
#        ('blocksize',np.int64),
#        ('frameorientation',np.int32),
#        ('framedatatype',np.int32),
#        ('frameoffset',np.int64),
#        ('qualityorientation',np.int32),
#        ('qualitydatatype',np.int32),
#        ('qualityoffset',np.int64),
#        ('qualityblocksize',np.int64),
#        ('year',np.int16),
#        ('month',np.int16),
#        ('day',np.int16),
#        ('hour',np.int16),
#        ('min',np.int16),
#        ('sec',np.int16),
#        ('microsecond',np.int32),
#        ('tzoffset',np.int16),
#        ('samplingrate',np.dtype('d')),
#        ('framecapacity',np.int64),
#        ('numberofframes',np.int64),
#        ('compression',np.int64),
#        ('numberofchannels',np.int32),
#        ('numberofzones',np.int16),
#        ('dphase',np.int16,(channelNum,frameNum))])
    
#    dasData = np.fromfile(fileName,dtype=dasDataType,count=1)
#    dasData = np.squeeze(dasData['dphase'])
#    dasData = dasData.astype('float32')
#    return dasData

#def bin2np4iq(fileName, channelNum, frameNum):
    
#    #Convert DAS data into numpy array
#    #Input: .bin das file
    
#    #re-read das binary given channel/frame information
    
#    dasDataType = np.dtype([('preamb',np.int64),
#        ('version',np.int16),
#        ('mode',np.int16),
#        ('softwarename',np.int8,32),
#        ('content',np.int32),
#        ('blocksize',np.int64),
#        ('frameorientation',np.int32),
#        ('framedatatype',np.int32),
#        ('frameoffset',np.int64),
#        ('qualityorientation',np.int32),
#        ('qualitydatatype',np.int32),
#        ('qualityoffset',np.int64),
#        ('qualityblocksize',np.int64),
#        ('year',np.int16),
#        ('month',np.int16),
#        ('day',np.int16),
#        ('hour',np.int16),
#        ('min',np.int16),
#        ('sec',np.int16),
#        ('microsecond',np.int32),
#        ('tzoffset',np.int16),
#        ('samplingrate',np.dtype('d')),
#        ('framecapacity',np.int64),
#        ('numberofframes',np.int64),
#        ('compression',np.int64),
#        ('numberofchannels',np.int32),
#        ('numberofzones',np.int16),
#        ('iq',np.int16,2*channelNum*frameNum)])
#    dasData = np.fromfile(fileName,dtype=dasDataType,count=1)
#    dasData = dasData['iq']
#    qData = dasData[np.s_[0,1::2]]
#    iData = dasData[np.s_[0,0::2]]
    
#    iData = iData.reshape(channelNum,-1).astype(np.float32)
#    qData = qData.reshape(channelNum,-1).astype(np.float32)

##    iData = dasData[:,0].reshape(channelNum,frameNum).astype('float32')
##    quad = dasData[:,1].reshape(channelNum,frameNum).astype('float32')
##    inPhase = inPhase.reshape(channelNum,frameNum).astype('float32')
##    quad = quad.reshape(channelNum,frameNum).astype('float32')
##    iData = dasData[0::2].reshape(channelNum,-1).astype(np.float)
##    qData = dasData[1::2].reshape(channelNum,-1).astype(np.float)
##    dasData = np.arctan2(qData,iData)
##    dasData = np.unwrap(dasData)
#    return iData, qData

#def bin2np0(fileName):
    
#    #Convert DAS data into numpy array
#    #Input: .bin das file
    
#    #read header from das binary
#    dasDataType = np.dtype([('preamb',np.int64),
#            ('version',np.int16),
#            ('mode',np.int16),
#            ('softwarename',np.int8,32),
#            ('content',np.int32),
#            ('blocksize',np.int64),
#            ('frameorientation',np.int32),
#            ('framedatatype',np.int32),
#            ('frameoffset',np.int64),
#            ('qualityorientation',np.int32),
#            ('qualitydatatype',np.int32),
#            ('qualityoffset',np.int64),
#            ('qualityblocksize',np.int64),
#            ('year',np.int16),
#            ('month',np.int16),
#            ('day',np.int16),
#            ('hour',np.int16),
#            ('min',np.int16),
#            ('sec',np.int16),
#            ('microsecond',np.int32),
#            ('tzoffset',np.int16),
#            ('samplingrate',np.dtype('d')),
#            ('framecapacity',np.int64),
#            ('numberofframes',np.int64),
#            ('compression',np.int64),
#            ('numberofchannels',np.int32),
#            ('numberofzones',np.int16),
#            ])
    
#    h = np.fromfile(fileName,dtype=dasDataType,count=1)
#    frameNum = h['numberofframes'][0]
#    channelNum = h['numberofchannels'][0]
    
#    #re-read das binary given channel/frame information
#    dasDataType = np.dtype([('preamb',np.int64),
#        ('version',np.int16),
#        ('mode',np.int16),
#        ('softwarename',np.int8,32),
#        ('content',np.int32),
#        ('blocksize',np.int64),
#        ('frameorientation',np.int32),
#        ('framedatatype',np.int32),
#        ('frameoffset',np.int64),
#        ('qualityorientation',np.int32),
#        ('qualitydatatype',np.int32),
#        ('qualityoffset',np.int64),
#        ('qualityblocksize',np.int64),
#        ('year',np.int16),
#        ('month',np.int16),
#        ('day',np.int16),
#        ('hour',np.int16),
#        ('min',np.int16),
#        ('sec',np.int16),
#        ('microsecond',np.int32),
#        ('tzoffset',np.int16),
#        ('samplingrate',np.dtype('d')),
#        ('framecapacity',np.int64),
#        ('numberofframes',np.int64),
#        ('compression',np.int64),
#        ('numberofchannels',np.int32),
#        ('numberofzones',np.int16),
#        ('dphase',np.int16,(channelNum,frameNum))])
    
#    dasData = np.fromfile(fileName,dtype=dasDataType,count=1)
##    dasData = np.squeeze(dasData['phase'])
#    return dasData

# return bytes per data point for each data type
# NONE	0			No data
# ABC_INT16	1	int16_t[3]	12	Triple sensor raw data
# IQ_INT16	2	int16_t[2]	4	Each sample represents an I & Q pair.
# DPHASE_INT16	3	int16_t	2	Differential phase, scaled by 10,430 (2^15-1 / pi) to span the dynamic range of the 16-bit integer
# AMPLITUDE_INT16	4	int16_t	2
# AMPLITUDE_FLOAT	5	float	4
# PHASE_FLOAT	6	float	4
# INTENSITY_FLOAT	7	float	4	Also used for phase power
# VSP_SINGLE_SWEEP_FLOAT	8	float	4
# VSP_STACKED_SWEEP_FLOAT	9	float	4
# FLOW_FLOAT	10	float	4
# INTENSITY_SPECTROGRAM_FLOAT	11	float	4	Complete frequency domain data
# ABCD_INT16	12	int16_t[4]	4	Quad sensor raw data
# FLOW_INJECTION	13	???	?
# FLOW_RELATIVE	14	????	?
# FLOW_PRODUCTION	15	????	?
# AMPLITUDE_QUAD	16	float[4]	16	Quality data stored as a composite of four values: average, minimum, maximum amplitude, and amplitude standard deviation, respectively
# DPHASE_FLOAT	17	float	2	Differential phase
# MINMAX_FLOAT	18	float	2	Differential phase
# IQ_FLOAT	19	float[2]	8	Each sample represents an I & Q pair
# COMPLEX_FLOAT	20	float[2]	8	Differential phase
# ABCD_INT16_RAW	21	int16_t[4]	8	Differential phase
# IQ_INT16_RAW	22	int16_t[2]	4	Differential phase
# IQIQ_INT16_RAW	23	int16_t[4]	8	Differential phase
# REAL_FLOAT	24	float	4	Differential phase
# FLOW_EROSION	25	????	?	Differential phase
# STATIC_PHASE_FLOAT	26	float	4	Differential phase integrated from 0 over specified block size
# PHASE_VARIANCE_FLOAT	27	float	4	Standard deviation of phase
# PHASE_POWER_FLOAT	28	float	4	Frequency domain from only selected bands.
# QUALITY_FLOAT	29	float	4	Quality (amplitude) data
# STRAIN_FLOAT	30	float	4	Differential phase integrated from 0 over the specified block size scaled with an optical strain coefficient.
#sizeOfDataType = {0: 0,
#                  1: 12,
#                  2: 4,
#                  3: 2,
#                  4: 2,
#                  5: 4,
#                  6: 4,
#                  7: 4,
#                  8: 4,
#                  9: 4,
#                  10: 4,
#                  11: 4,
#                  12: 4,
#                  13: 4,
#                  14: 4,
#                  15: 4,
#                  16: 16,
#                  17: 2,
#                  18: 2,
#                  19: 8,
#                  20: 8,
#                  21: 8,
#                  22: 4,
#                  23: 8,
#                  24: 4,
#                  25: 4,
#                  26: 4,
#                  27: 4,
#                  28: 4,
#                  29: 4,
#                  30: 4}

#npTypeOfDataType = {0: np.int8,
#                    1: np.int16,
#                    2: np.int16,
#                    3: np.int16,
#                    4: np.int16,
#                    5: np.float,
#                    6: np.float,
#                    7: np.float,
#                    8: np.float,
#                    9: np.float,
#                    10: np.float,
#                    11: np.float,
#                    12: np.int16,
#                    13: np.float,
#                    14: np.float,
#                    15: np.float,
#                    16: np.float,
#                    17: np.float,
#                    18: np.float,
#                    19: np.float,
#                    20: np.float,
#                    21: np.int16,
#                    22: np.int16,
#                    23: np.int16,
#                    24: np.float,
#                    25: np.float,
#                    26: np.float,
#                    27: np.float,
#                    28: np.float,
#                    29: np.float,
#                    30: np.float}

#npLeadingArrayDimension = {0: 1,
#                      1: 3,
#                      2: 2,
#                      3: 1,
#                      4: 1,
#                      5: 1,
#                      6: 1,
#                      7: 1,
#                      8: 1,
#                      9: 1,
#                      10: 1,
#                      11: 1,
#                      12: 4,
#                      13: 1,
#                      14: 1,
#                      15: 1,
#                      16: 4,
#                      17: 1,
#                      18: 1,
#                      19: 2,
#                      20: 2,
#                      21: 4,
#                      22: 2,
#                      23: 4,
#                      24: 1,
#                      25: 1,
#                      26: 1,
#                      27: 1,
#                      28: 1,
#                      29: 1,
#                      30: 1}

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

#def findSomeDasJobs(drive):
#    prog = re.compile('RawData1$|dPhase Data 1$|IQ Data 1$|dPhase Data$|IQ Data$')
#    dasDirList = list()
#    dirList = [x[0] for x in os.walk(drive)]
#    for kDir in dirList:
#        print(kDir)
#        dirMatch = prog.search(kDir)
#        if dirMatch:
#            dasDirList.append(dirMatch.string)
#    return dasDirList

#def getJobName(dirName):
#    prog = re.compile('(?<=\\\\).*(?=\\\\RawData1|\\\\dPhase Data 1||\\\\IQ Data 1|\\\\dPhase Data)')
#    jobName = list()
#    for k in range(len(dirName)):
#        a = prog.search(dirName[k][0])
#        jobName.append(a.group(0))
#    return jobName



#def findDasIntensityDirectories(drive):
#    prog = re.compile('WaterfallIntensityData$|WaterfallData_PV_bs\d*_\d*$|Phase Variance BS\d*$|Phase Power BS\d* \d+\.\d+-\d+\.\d+Hz$')
#    dasDirList = list()
#    dirList = [x[0] for x in os.walk(drive)]
#    for kDir in dirList:
#        dirMatch = prog.search(kDir)
#        if dirMatch:
#            dasDirList.append(dirMatch.string)
#    return dasDirList

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

## test/debug global variables
if __debug__:
    testFileName3 = r"D:\COG_MAB_PROD_MS_MS_OPEN_3.1.2018.0615\Phase Power BS16384 0.00-0.92Hz\16384\UTC_Y2018_M03_D01\H13\M00\DOSS_20180301T130000_762830Z.bin"
    testFileName4 = r"D:\CrestoneFirstBinaries\DOSS_20210901T004421_288968Z.bin"
    testDataRoot3 = r"D:\COG_MAB_PROD_LH_BH_SHUTIN_2.17.2018.0615"
    testDataRoot4 = r"Z:\Crestone_3CH_15M_Offset_0907211452"
    testDataRoot3PV = r"D:\STATOIL_ABE_4H_STG11_FRAC"
    testFileTimeStampDirectory3 = r"D:\COG_MAB_PROD_MS_MS_OPEN_3.1.2018.0615\20190326200754 Phase Power BS16384 0.00-0.92Hz\16384"
    testFileTimeStampDirectory4 = r"Z:\Crestone_3CH_15M_Offset_0907211452\20210907T205823_063908Z\dPhase Data"

def testHeaderReader():
    header3Version = checkHeaderVersion(testFileName3)
    header4Version = checkHeaderVersion(testFileName4)
    assert(header3Version == 3)
    assert(header4Version == 4)
    dasHeader3 = np.fromfile(testFileName3, dtype=DASFileHeader_3, count=1)
    dasHeader4 = np.fromfile(testFileName4, dtype=DASFileHeader_4, count=1)

    # v3 header asserts
    assert(dasHeader3['Preamble'][0] == 0x4441535F46696C65)
    assert(dasHeader3['Version'][0] == 3)
    assert(dasHeader3['Mode'][0] == 0)
    assert(dasHeader3['Content'][0] == 2)
    assert(dasHeader3['BlockSize'][0] == 1)
    assert(dasHeader3['FrameOrientation'][0] == 1)
    assert(dasHeader3['FrameDataType'][0] == 7)
    assert(dasHeader3['FrameOffset'][0] == 1040)
    assert(dasHeader3['QualityOrientation'][0] == 0)
    assert(dasHeader3['QualityDataType'][0] == 0)
    assert(dasHeader3['QualityOffset'][0] == 0)
    assert(dasHeader3['QualityBlockSize'][0] == 0)
    assert(dasHeader3['Year'][0] == 2018)
    assert(dasHeader3['Month'][0] == 3)
    assert(dasHeader3['Day'][0] == 1)
    assert(dasHeader3['Hour'][0] == 13)
    assert(dasHeader3['Minute'][0] == 0)
    assert(dasHeader3['Second'][0] == 0)
    assert(dasHeader3['Microsecond'][0] == 762830)
    assert(dasHeader3['TZOffset'][0] == -360)
    assert(dasHeader3['SamplingRate'][0] == 10000)
    assert(dasHeader3['FrameCapacity'][0] == 1)
    assert(dasHeader3['NumberOfFrames'][0] == 1)
    assert(dasHeader3['Compression'][0] == 16384)
    assert(dasHeader3['NumberOfChannels'][0] == 3445)
    assert(dasHeader3['ZonesOffset'][0] == 1024)
    assert(dasHeader3['LocalYear'][0] == 2018)
    assert(dasHeader3['LocalMonth'][0] == 3)
    assert(dasHeader3['LocalDay'][0] == 1)
    assert(dasHeader3['LocalHour'][0] == 7)
    assert(dasHeader3['LocalMinute'][0] == 0)
    assert(dasHeader3['LocalSecond'][0] == 0)
    assert(dasHeader3['LocalMicrosecond'][0] == 762830)

    # v4 header asserts
    assert(dasHeader4['Preamble'][0] == 0x4441535F46696C65)
    assert(dasHeader4['Version'][0] == 4)
    assert(dasHeader4['Mode'][0] == 0)
    assert(dasHeader4['Content'][0] == 1)
    assert(dasHeader4['BlockSize'][0] == 1)
    assert(dasHeader4['FrameOrientation'][0] == 1)
    assert(dasHeader4['FrameDataType'][0] == 3)
    assert(dasHeader4['FrameOffset'][0] == 51564)
    assert(dasHeader4['QualityOrientation'][0] == 1)
    assert(dasHeader4['QualityDataType'][0] == 16)
    assert(dasHeader4['QualityOffset'][0] == 206850412)
    assert(dasHeader4['QualityBlockSize'][0] == 256)
    assert(dasHeader4['Year'][0] == 2021)
    assert(dasHeader4['Month'][0] == 9)
    assert(dasHeader4['Day'][0] == 1)
    assert(dasHeader4['Hour'][0] == 0)
    assert(dasHeader4['Minute'][0] == 44)
    assert(dasHeader4['Second'][0] == 21)
    assert(dasHeader4['Microsecond'][0] == 288968)
    assert(dasHeader4['TZOffset'][0] == -360)
    assert(dasHeader4['SamplingRate'][0] == 10000)
    assert(dasHeader4['FrameCapacity'][0] == 16384)
    assert(dasHeader4['NumberOfFrames'][0] == 16384)
    assert(dasHeader4['Compression'][0] == 1)
    assert(dasHeader4['NumberOfChannels'][0] == 6311)
    assert(dasHeader4['ZonesOffset'][0] == 1024)
    assert(dasHeader4['DepthCalibrationOffset'][0] == 1040)
    assert(dasHeader4['NominalDepthOffset'][0] == 1076)
    assert(dasHeader4['MeasuredDepthOffset'][0] == 26320)
    assert(dasHeader4['DigitizerRate'][0] == 100000000)
    assert(dasHeader4['DelayCoilLength'][0] == 5)
    assert(dasHeader4['IndexOfRefraction'][0] == 1.4682)
    assert(dasHeader4['LocalYear'][0] == 2021)
    assert(dasHeader4['LocalMonth'][0] == 8)
    assert(dasHeader4['LocalDay'][0] == 31)
    assert(dasHeader4['LocalHour'][0] == 18)
    assert(dasHeader4['LocalMinute'][0] == 44)
    assert(dasHeader4['LocalSecond'][0] == 21)
    assert(dasHeader4['LocalMicrosecond'][0] == 288968)

def testRawDirectorySearch():
    rawJobList = findDPhaseDirectories(testDataRoot4)
    assert(r"Z:\Crestone_3CH_15M_Offset_0907211452\20210907T205823_063908Z\dPhase Data" in rawJobList)
    assert(r"Z:\Crestone_3CH_15M_Offset_0907211452\20210907T213257_211464Z\dPhase Data" in rawJobList)
    assert(r"Z:\Crestone_3CH_15M_Offset_0907211452\20210907T233716_917553Z\dPhase Data" in rawJobList)

def testIntensityDirectorySearch():
    phaseVarianceJobList3 = findPhaseVarianceDirectories(testDataRoot3PV)
    phaseVarianceJobList4 = findPhaseVarianceDirectories(testDataRoot4)
    phasePowerJobList3 = findPhasePowerDirectories(testDataRoot3)
    phasePowerJobList4 = findPhasePowerDirectories(testDataRoot4)
    staticPhaseJobList4 = findStaticPhaseDirectories(testDataRoot4)

    # phase variance asserts
    assert(r"D:\STATOIL_ABE_4H_STG11_FRAC\Phase Variance BS256" in phaseVarianceJobList3)
    assert(r"Z:\Crestone_3CH_15M_Offset_0907211452\20210907T205823_063908Z\Phase Variance BS1024" in phaseVarianceJobList4)
    assert(r"Z:\Crestone_3CH_15M_Offset_0907211452\20210907T213257_211464Z\Phase Variance BS1024" in phaseVarianceJobList4)
    assert(r"Z:\Crestone_3CH_15M_Offset_0907211452\20210907T233716_917553Z\Phase Variance BS1024" in phaseVarianceJobList4)

    # phase power asserts
    assert(r"D:\COG_MAB_PROD_LH_BH_SHUTIN_2.17.2018.0615\Phase Power BS16384 0.00-0.92Hz" in phasePowerJobList3)
    assert(r"D:\COG_MAB_PROD_LH_BH_SHUTIN_2.17.2018.0615\Phase Power BS16384 0.00-4.88Hz" in phasePowerJobList3)

    # static phase asserts
    assert(r"Z:\Crestone_3CH_15M_Offset_0907211452\20210907T213257_211464Z\Phase BS8192" in staticPhaseJobList4)
    assert(r"Z:\Crestone_3CH_15M_Offset_0907211452\20210907T233716_917553Z\Phase BS8192" in staticPhaseJobList4)
    assert(r"Z:\Crestone_3CH_15M_Offset_0907211452\20210907T205823_063908Z\Phase BS8" in staticPhaseJobList4)

def testGetTimeStamps():
    fileList3 = dirRecursive(testFileTimeStampDirectory3)
    fileList4 = dirRecursive(testFileTimeStampDirectory4)
    timeStamps3 = getFileTimeStamps(fileList3)
    timeStamps4 = getFileTimeStamps(fileList4)
    for k in range(10):
        print(fileList3[k] + " : " + str(timeStamps3[k]))
    for k in range(10):
        print(fileList4[k] + " : " + str(timeStamps4[k]))

def testReadDasBinary():
    dasHeader3, dasFrameData3 = readDasBinary(testFileName3)
    dasHeader4, dasFrameData4, measuredDepthData4 = readDasBinary(testFileName4)
    return None

if __name__ == "__main__":
    if __debug__:
        testHeaderReader()
        testRawDirectorySearch()
        testIntensityDirectorySearch()
        testGetTimeStamps()
        testReadDasBinary()