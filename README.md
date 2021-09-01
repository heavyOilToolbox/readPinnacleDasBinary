# readPinnacleDasBinary
C and C-MEX Utility for Reading and Converting v3 and v4 DAS Binaries  
`frameData = readPinnacleDasBinary(fullFilePath)` returns Frame Data, a [NumberOfFrames x NumberOfChannels] matrix. The data type will be one of the following:  

|Type                        |ID       | Type(s)    | Size | Description|
|--------------------------- | ------: | ------     | ---- | ---------  |
|NONE                        |       0 |            |      | No data|
|ABC_INT16                   |       1 | int16_t[3] |    12| Triple sensor raw data |
|IQ_INT16                    |       2 | int16_t[2] |     4| Each sample represents an I & Q pair.|
|DPHASE_INT16                |       3 | int16_t    |     2| Differential phase, scaled by 10,430 (2^15-1 / π) to span the dynamic range of the 16-bit integer|
|AMPLITUDE_INT16             |       4 | int16_t    |     2| |
|AMPLITUDE_FLOAT             |       5 | float      |     4| |
|PHASE_FLOAT                 |       6 | float      |     4| |
|INTENSITY_FLOAT             |       7 | float      |     4| Also used for phase power |
|~~VSP_SINGLE_SWEEP_FLOAT~~  |       8 | float      |     4| |
|~~VSP_STACKED_SWEEP_FLOAT~~  |       9 | float      |     4| |
|~~FLOW_FLOAT~~  |      10 | float      |     4| |
|INTENSITY_SPECTROGRAM_FLOAT |      11 | float      |     4| Complete frequency domain data|
|ABCD_INT16                  |      12 | int16_t[4] |     4| Quad sensor raw data |
|~~FLOW_INJECTION~~              |      13 | ???        |     ?| |
|~~FLOW_RELATIVE~~               |      14 | ????       |     ?| |
|~~FLOW_PRODUCTION~~             |      15 | ????       |     ?| |
|AMPLITUDE_QUAD              |      16 | float[4]   |    16| Quality data stored as a composite of four values: average, minimum, maximum amplitude, and amplitude standard deviation, respectively|
|DPHASE_FLOAT                |      17 | float      |     2| Differential phase |
|~~MINMAX_FLOAT~~                |      18 | float      |     2| Differential phase |
|IQ_FLOAT                    |      19 | float[2]   |     8| Each sample represents an I & Q pair|
|~~COMPLEX_FLOAT~~               |      20 | float[2]   |     8| Differential phase |
|ABCD_INT16_RAW              |      21 | int16_t[4] |     8| Differential phase |
|IQ_INT16_RAW                |      22 | int16_t[2] |     4| Differential phase |
|IQIQ_INT16_RAW              |      23 | int16_t[4] |     8| Differential phase |
|REAL_FLOAT                  |      24 | float      |     4| Differential phase |
|~~FLOW_EROSION~~                |      25 | ????       |     ?| Differential phase |
|STATIC_PHASE_FLOAT          |      26 | float      |     4| Differential phase integrated from 0 over specified block size|
|PHASE_VARIANCE_FLOAT        |      27 | float      |     4| Standard deviation of phase|
|PHASE_POWER_FLOAT           |      28 | float      |     4|Frequency domain from only selected bands.|
|QUALITY_FLOAT               |      29 | float      |     4|Quality (amplitude) data|
|STRAIN_FLOAT                |      30 | float      |     4|Differential phase integrated from 0 over the specified block size scaled with an optical strain coefficient.|

In general, it will be uncommon to see FrameDataType other than 2, 3, 7 or 30.   

`[header, frameData] = readPinnacleDasBinary(fullFilePath)` also returns the file header a struct. Pinnacle v4 File Headers Contain the Following Fields
| Offset |   Field           | Type         | Size (bytes) | Description |
| -----: | :---------------- | :----------- | -----------: | :-----------|
|   0000 | Preamble          | uint8_t[8]   |            8 | A magic number identifying the file as a DASFV file: 0x4441535F46696C65 |
|   0008 | Version           | uint16_t     |            2 | The header version. This document describes version 4.|
|   0010 | Mode              | uint16_t     |            2 | 0, if the file was generated during acquisition, 1 otherwise.|
|   0012 | Software Name     | char[32]     |           32 | A 32 character ASCII string with the name and version of the application used to generate the file.|
|   0044 | Content           | uint32_t     |            4 | Indicates the kind of file (RAW:1, INTENSITY: 2, SPECTROGRAM: 4)|
| ...    |                   |              |              | |
|   0056 | Frame Orientation | uint32_t     |            4 | Orientation of the frame data. See Frame/Quality Data below for more information.|
|   0060 | Frame Data Type   | uint32_t     |            4 | Indicates the data type of the frames section.|
|   0064 | Frame Offset      | uint64_t     |            8 | The offset, in bytes, from the start of the file to the start of the frame data|
|   0072 | Quality Orientation|uint32_t     |            4 | Orientation of the quality data. See Frame/Quality Data below for more information.|
|   0076 | Quality Data Type | uint32_t     |            4 | Indicates the data type of the quality section.|
|   0080 | Quality Offset    | uint64_t     |            8 | The offset, in bytes, from the start of the file to the start of the quality data"|
|   0088 | Quality Block Size| uint64_t     |            8 | The number of frames represented by one quality value|
|   0096 | Year              | uint16_t     |            2 | The timestamp encoded using the UTC time zone.|
|   0098 | Month             | uint16_t     |            2 | Month 1-12 |
|   0100 | Day               | uint16_t     |            2 | Day 1-31 |
|   0102 | Hour              | uint16_t     |            2 | 0-23|
|   0104 | Minute            | uint16_t     |            2 | 0-59|
|   0106 | Second            | uint16_t     |            2 | 0-60 (61 on leap seconds) |
|   0108 | Microsecond       | uint32_t     |            4 | 0-999999|
|   0112 | Time Zone Offset  | int16_t      |            2 | The local time zone offset relative to UTC, in minutes, ±720|
|   0114 | Sampling Rate     | double       |            8 | The rate, in Hz, at which the data was acquired, usually the laser pulse rate.|
|   0122 | Frame Capacity    | uint64_t     |            8 | The number of frames the file is capable of storing.  Usually same as number of frames below, except maybe last file where number of frames may be less.|
|   0130 | Number of Frames  | uint64_t     |            8 | The number of frames written to the file|
|   0138 | Compression       | uint64_t     |            8 | The compression factor, making the effective sample rate Sample Rate / Compression|
|   0146 | Number of Channels| uint32_t     |            4 | The total number of channels in the file.|
|   0150 | Zones Offset      | uint64_t     |            8 | The offset, in bytes, from the start of the file to the start of the zone information.|
|   0158 | Depth Calibration Offset|uint64_t|            8 | The offset, in bytes, from the start of the file to the start of the depth calibration information.|
|   0166 | Nominal Depth Offset|uint64_t    |            8 | The offset, in bytes, from the start of the file to the start of the nominal depth information.|
|   0174 | Measured Depth Offset|uint64_t   |            8 | The offset, in bytes, from the start of the file to the start of the measured depth information.|
|   ...  |                                  |              | Padding              |
|   0512 | Digitizer Rate    | double       |            8 | The sampling rate, in Hz, of the digitizer.|
|   0520 | Gauge Length      | double       |            8 | The length of the delay coil in meters.|
|   0528 | Index of Refraction|double       |            8 | The index of refraction of the sensing fiber.|
|   0536 | Local Year        | uint16_t     |            2 | The timestamp encoded using the local time zone.|
|   0538 | Local Month       | uint16_t     |            2 ||
|   0540 | Local Day         | uint16_t     |            2 ||
|   0542 | Local Hour        | uint16_t     |            2 ||
|   0544 | Local Minute      | uint16_t     |            2 ||
|   0546 | Local Second      | uint16_t     |            2 ||
|   0548 | Local Microsecond | uint32_t     |            4 ||
|    ... |                   |              |              | Padding to make entire length 1024|
|   1024 |                   |              |              | |

Pinnacle v3 File Headers are similar, but do not contain the following 6 fields: `DepthCalibrationOffset, NominalDepthOffset, MeasuredDepthOffset, DigitizerRate, GaugeLength, IndexOfRefraction`  
     
`[header, frameData, qualityData] = readPinnacleDasBinary(fullFilePath)` also returns Quality data, an [4 x nFrame/QualityBlockSize x nChannel] 3D array of 16 bit integers. Quality in this context is an alias for IQ amplitude. The first 4 array dimensions are [avg, min, max, stdev] computed over QualityBlockSize. Quality Data is only valid/returned if the FrameDataType is Differential Phase.
 
`[header, zones, frameData] = readPinnacleDasBinary(fullFilePath)` also returns  
    the Zone block, a [1 + NumberOfZones * 3 elements x 1] vector, with structure  
    `[NumberOfZones, Zone1Start, Zone1End, Zone1Stride, Zone2Start, Zone2End, ...   
     ... ZoneNStart, ZoneNEnd, ZoneNStride]`  
 
`[header, zones, frameData, qualityData] = readPinnacleDasBinary(fullFilePath)`  
    returns the file header, the Zone block, Frame Data, and Quality Data.  
  
Additional Calling Syntax valid only for **v4** Pinnacle DAS Binaries  
 	`[header, zones, depthCal, nominalDepth, measuredDepth, frameData] = readPinnacleDasBinary(fullFilePath)`  
 	`[header, zones, depthCal, nominalDepth, measuredDepth, frameData, qualityData] = readPinnacleDasBinary(fullFilePath)`  
    also return the Depth Calibration block, the Nominal Depth block, and the Measured Depth block.  
    The Depth Calibration block is a 2 x NumberOfDepthKeyPoint matrix of doubles mapping Channels to Measured Depth. For field-collected data, this is most likely a 2 x 2 matrix with structure:
    `[WellheadChannel, WellheadFiberMeasuredDepth;...  
     FiberEndChannel, FiberEndMeasuredDepth]`  
 
The Nominal Depth block is a [NumberOfChannels x 1] vector of Nominal 
Depth, also known as Fiber Distance, stored as single-precision floats.
  
The Measured Depth block, is a [NumberOfChannels x 1] vector of 
shifted-and-scaled Depths. The depth calibration applied is based on 
piecewise linear interpolation between the Key Points in the Depth 
Calibration block.
