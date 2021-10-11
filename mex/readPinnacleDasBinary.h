#pragma once

#include <stdlib.h>
#include <stdint.h>
#include <float.h>
//#include <math.h>
#include "mex.h"
#include "matrix.h"

const static double ScaleFactor = 10430.0;
const static double MetersPerChannel = 1.0209523838714072;
const static size_t SoftwareNameLength = 32;
const static size_t PadLength0 = 202;
const static size_t PadLength3 = 378;
const static size_t PadLength4 = 330;

#pragma pack(push, 1)
typedef struct DASFileHeader_0
{
	uint64_t Preamble;
	uint16_t Version;
	uint16_t Format;
	uint16_t Year;
	uint16_t Month;
	uint16_t Day;
	uint16_t Hour;
	uint16_t Minute;
	uint16_t Second;
	uint16_t Millisecond;
	int16_t TZOffset;
	uint32_t Reserved1;
	uint32_t Reserved2;
	uint16_t Reserved3;
	uint32_t NumberOfFrames;
	uint32_t FrameCapacity;
	uint32_t Compression;
	uint32_t Reserved4;
	uint8_t  Padding[202];
} DASFileHeader0_T;
#pragma pack(pop)

const int nField0 = 19;
static const char* FieldName0[] = {
	"Preamble",
	"Version",
	"Format",
	"Year",
	"Month",
	"Day",
	"Hour",
	"Minute",
	"Second",
	"Millisecond",
	"TZOffset",
	"Reserved1",
	"Reserved2",
	"Reserved3",
	"NumberOfFrames",
	"FrameCapacity",
	"Compression",
	"Reserved4",
	"Padding"
};

#pragma pack(push, 1)
typedef struct DASFileHeader_1
{
	int64_t Preamble;
	int16_t Version;
	int16_t Mode;
	int8_t SoftwareName[32];
	int32_t Content;
	int64_t BlockSize;
	int32_t FrameOrientation;
	int32_t FrameDataType;
	int64_t FrameOffset;
	int32_t QualityOrientation;
	int32_t QualityDataType;
	int64_t QualityOffset;
	int64_t QualityBlockSize;
	int16_t Year;
	int16_t Month;
	int16_t Day;
	int16_t Hour;
	int16_t Minute;
	int16_t Second;
	int32_t Microsecond;
	int16_t TZOffset;
	double SamplingRate;
	int64_t FrameCapacity;
	int64_t NumberOfFrames;
	int64_t Compression;
	int32_t NumberOfChannels;
	int16_t NumberOfZones;
	int32_t Zones[3 * 32];
} DASFileHeader1_T;
#pragma pack(pop)

const int nField1 = 28;
static const char* FieldName1[] = {
	"Preamble",
	"Version",
	"Mode",
	"SoftwareName",
	"Content",
	"BlockSize",
	"FrameOrientation",
	"FrameDataType",
	"FrameOffset",
	"QualityOrientation",
	"QualityDataType",
	"QualityOffset",
	"QualityBlockSize",
	"Year",
	"Month",
	"Day",
	"Hour",
	"Minute",
	"Second",
	"Microsecond",
	"TZOffset",
	"SamplingRate",
	"FrameCapacity",
	"NumberOfFrames",
	"Compression",
	"NumberOfChannels",
	"NumberOfZones",
	"Zones"
};

#pragma pack(push, 1)
typedef struct DASFileHeader_2
{
	int64_t Preamble;
	int16_t Version;
	int16_t Mode;
	int8_t SoftwareName[32];
	int32_t Content;
	int64_t BlockSize;
	int32_t FrameOrientation;
	int32_t FrameDataType;
	int64_t FrameOffset;
	int32_t QualityOrientation;
	int32_t QualityDataType;
	int64_t QualityOffset;
	int64_t QualityBlockSize;
	int16_t Year;
	int16_t Month;
	int16_t Day;
	int16_t Hour;
	int16_t Minute;
	int16_t Second;
	int32_t Microsecond;
	int16_t TZOffset;
	double SamplingRate;
	int64_t FrameCapacity;
	int64_t NumberOfFrames;
	int64_t Compression;
	int32_t NumberOfChannels;
	int16_t NumberOfZones;
	int32_t Zones[3 * 32];
	int16_t LocalYear;
	int16_t LocalMonth;
	int16_t LocalDay;
	int16_t LocalHour;
	int16_t LocalMinute;
	int16_t LocalSecond;
	int32_t LocalMicrosecond;
} DASFileHeader2_T;
#pragma pack(pop)

const int nField2 = 35;
static const char* FieldName2[] = {
	"Preamble",
	"Version",
	"Mode",
	"SoftwareName",
	"Content",
	"BlockSize",
	"FrameOrientation",
	"FrameDataType",
	"FrameOffset",
	"QualityOrientation",
	"QualityDataType",
	"QualityOffset",
	"QualityBlockSize",
	"Year",
	"Month",
	"Day",
	"Hour",
	"Minute",
	"Second",
	"Microsecond",
	"TZOffset",
	"SamplingRate",
	"FrameCapacity",
	"NumberOfFrames",
	"Compression",
	"NumberOfChannels",
	"NumberOfZones",
	"Zones",
	"LocalYear",
	"LocalMonth",
	"LocalDay",
	"LocalHour",
	"LocalMinute",
	"LocalSecond",
	"LocalMicrosecond"
};

#pragma pack(push, 1)
typedef struct DASFileHeader_3
{
	int64_t Preamble;
	int16_t Version;
	int16_t Mode;
	int8_t SoftwareName[32];
	int32_t Content;
	int64_t BlockSize;
	int32_t FrameOrientation;
	int32_t FrameDataType;
	int64_t FrameOffset;
	int32_t QualityOrientation;
	int32_t QualityDataType;
	int64_t QualityOffset;
	int64_t QualityBlockSize;
	int16_t Year;
	int16_t Month;
	int16_t Day;
	int16_t Hour;
	int16_t Minute;
	int16_t Second;
	int32_t Microsecond;
	int16_t TZOffset;
	double SamplingRate;
	int64_t FrameCapacity;
	int64_t NumberOfFrames;
	int64_t Compression;
	int32_t NumberOfChannels;
	int64_t ZonesOffset;
	int8_t Reserved[378];
	int16_t LocalYear;
	int16_t LocalMonth;
	int16_t LocalDay;
	int16_t LocalHour;
	int16_t LocalMinute;
	int16_t LocalSecond;
	int32_t LocalMicrosecond;
} DASFileHeader3_T;
#pragma pack(pop)

const int nField3 = 35;
static const char* FieldName3[] = {
	"Preamble",
	"Version",
	"Mode",
	"SoftwareName",
	"Content",
	"BlockSize",
	"FrameOrientation",
	"FrameDatatype",
	"FrameOffset",
	"QualityOrientation",
	"QualityDatatype",
	"QualityOffset",
	"QualityBlockSize",
	"Year",
	"Month",
	"Day",
	"Hour",
	"Minute",
	"Second",
	"Microsecond",
	"TZOffset",
	"SamplingRate",
	"FrameCapacity",
	"NumberOfFrames",
	"Compression",
	"NumberOfChannels",
	"ZonesOffset",
	"Reserved",
	"LocalYear",
	"LocalMonth",
	"LocalDay",
	"LocalHour",
	"LocalMinute",
	"LocalSecond",
	"LocalMicrosecond"
};

#pragma pack(push, 1)
typedef struct DASFileHeader_4
{
	int64_t Preamble;
	int16_t Version;
	int16_t Mode;
	int8_t SoftwareName[32];
	int32_t Content;
	int64_t BlockSize;
	int32_t FrameOrientation;
	int32_t FrameDataType;
	int64_t FrameOffset;
	int32_t QualityOrientation;
	int32_t QualityDataType;
	int64_t QualityOffset;
	int64_t QualityBlockSize;
	int16_t Year;
	int16_t Month;
	int16_t Day;
	int16_t Hour;
	int16_t Minute;
	int16_t Second;
	int32_t Microsecond;
	int16_t TZOffset;
	double SamplingRate;
	int64_t FrameCapacity;
	int64_t NumberOfFrames;
	int64_t Compression;
	int32_t NumberOfChannels;
	int64_t ZonesOffset;
	int64_t DepthCalibrationOffset;
	int64_t NominalDepthOffset;
	int64_t MeasuredDepthOffset;
	int8_t Reserved[330];
	double DigitizerRate;
	double DelayCoilLength;
	double IndexOfRefraction;
	int16_t LocalYear;
	int16_t LocalMonth;
	int16_t LocalDay;
	int16_t LocalHour;
	int16_t LocalMinute;
	int16_t LocalSecond;
	int32_t LocalMicrosecond;
} DASFileHeader4_T;
#pragma pack(pop)

const int nField4 = 41;
static const char* FieldName4[] = {
	"Preamble",
	"Version",
	"Mode",
	"SoftwareName",
	"Content",
	"BlockSize",
	"FrameOrientation",
	"FrameDataType",
	"FrameOffset",
	"QualityOrientation",
	"QualityDataType",
	"QualityOffset",
	"QualityBlockSize",
	"Year",
	"Month",
	"Day",
	"Hour",
	"Minute",
	"Second",
	"Microsecond",
	"TZOffset",
	"SamplingRate",
	"FrameCapacity",
	"NumberOfFrames",
	"Compression",
	"NumberOfChannels",
	"ZonesOffset",
	"DepthCalibrationOffset",
	"NominalDepthOffset",
	"MeasuredDepthOffset",
	"Reserved",
	"DigitizerRate",
	"DelayCoilLength",
	"IndexOfRefraction",
	"LocalYear",
	"LocalMonth",
	"LocalDay",
	"LocalHour",
	"LocalMinute",
	"LocalSecond",
	"LocalMicrosecond"
};