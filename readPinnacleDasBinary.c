//
//* C-MEX to load pinnacle DAS binaries
//*
//* input is a full path to a binary file on disk
//*
//* The calling syntax is:
//* 
//* v3 header calling syntax (from MATLAB)
//* frameData = readPinnacleDasBinary(fullFilePath);
//* [header, frameData] = readPinnacleDasBinary(fullFilePath);
//* [header, frameData, qualityData] = readPinnacleDasBinary(fullFilePath);
//* [header, zones, frameData] = readPinnacleDasBinary(fullFilePath);
//* [header, zones, frameData, qualityData] = readPinnacleDasBinary(fullFilePath);
//* 
//* v4 header calling syntax (from MATLAB)
//* frameData = readPinnacleDasBinary(fullFilePath);
//* [header, frameData] = readPinnacleDasBinary(fullFilePath);
//* [header, frameData, qualityData] = readPinnacleDasBinary(fullFilePath);
//* [header, zones, frameData] = readPinnacleDasBinary(fullFilePath);
//* [header, zones, depthCal, nominalDepth, measuredDepth, frameData] = readPinnacleDasBinary(fullFilePath);
//* [header, zones, depthCal, nominalDepth, measuredDepth, frameData, qualityData] = readPinnacleDasBinary(fullFilePath);
//*
//* Peter Cook 2018. revised 2021


#include <stdlib.h>
#include <stdint.h>
#include <float.h>
#include <string.h>
//#include <math.h>
#include "mex.h"
#include "matrix.h"
#include "readPinnacleDasBinary.h"


/*
NONE	0			No data
ABC_INT16	1	int16_t[3]	12	Triple sensor raw data
IQ_INT16	2	int16_t[2]	4	Each sample represents an I & Q pair.
DPHASE_INT16	3	int16_t	2	Differential phase, scaled by 10,430 (2^15-1 / pi) to span the dynamic range of the 16-bit integer
AMPLITUDE_INT16	4	int16_t	2
AMPLITUDE_FLOAT	5	float	4
PHASE_FLOAT	6	float	4
INTENSITY_FLOAT	7	float	4	Also used for phase power
VSP_SINGLE_SWEEP_FLOAT	8	float	4
VSP_STACKED_SWEEP_FLOAT	9	float	4
FLOW_FLOAT	10	float	4
INTENSITY_SPECTROGRAM_FLOAT	11	float	4	Complete frequency domain data
ABCD_INT16	12	int16_t[4]	4	Quad sensor raw data
FLOW_INJECTION	13	???	?
FLOW_RELATIVE	14	????	?
FLOW_PRODUCTION	15	????	?
AMPLITUDE_QUAD	16	float[4]	16	Quality data stored as a composite of four values: average, minimum, maximum amplitude, and amplitude standard deviation, respectively
DPHASE_FLOAT	17	float	2	Differential phase
MINMAX_FLOAT	18	float	2	Differential phase
IQ_FLOAT	19	float[2]	8	Each sample represents an I & Q pair
COMPLEX_FLOAT	20	float[2]	8	Differential phase
ABCD_INT16_RAW	21	int16_t[4]	8	Differential phase
IQ_INT16_RAW	22	int16_t[2]	4	Differential phase
IQIQ_INT16_RAW	23	int16_t[4]	8	Differential phase
REAL_FLOAT	24	float	4	Differential phase
FLOW_EROSION	25	????	?	Differential phase
STATIC_PHASE_FLOAT	26	float	4	Differential phase integrated from 0 over specified block size
PHASE_VARIANCE_FLOAT	27	float	4	Standard deviation of phase
PHASE_POWER_FLOAT	28	float	4	Frequency domain from only selected bands.
QUALITY_FLOAT	29	float	4	Quality (amplitude) data
STRAIN_FLOAT	30	float	4	Differential phase integrated from 0 over the specified block size scaled with an optical strain coefficient.
*/
size_t sizeOfDataType(int32_t frameDataType)
{
	size_t numBytes = 0;
	switch (frameDataType) 
	{
	case 1:
		// ABC_INT16 int16_t[3]
		//numBytes = 12;
		numBytes = sizeof(int16_t[3]);
		break;
	case 2:
		// IQ_INT16 int16_t[2]
		//numBytes = 4;
		numBytes = sizeof(int16_t[2]);
		break;
	case 3:
		// DPHASE_INT16 int16_t
		//numBytes = 2;
		numBytes = sizeof(int16_t);
		break;
	case 4:
		// AMPLITUDE_INT16 int16_t
		//numBytes = 2;
		numBytes = sizeof(int16_t);
		break;
	case 5:
		// AMPLITUDE_FLOAT float
		//numBytes = 4;
		numBytes = sizeof(float);
		break;
	case 6:
		// PHASE_FLOAT float
		//numBytes = 4;
		numBytes = sizeof(float);
		break;
	case 7:
		// INTENSITY_FLOAT float
		//numBytes = 4;
		numBytes = sizeof(float);
		break;
	case 8:
		// VSP_SINGLE_SWEEP_FLOAT float
		//numBytes = 4;
		numBytes = sizeof(float);
		break;
	case 9:
		// VSP_STACKED_SWEEP_FLOAT float
		//numBytes = 4;
		numBytes = sizeof(float);
		break;
	case 10:
		// FLOW_FLOAT float
		//numBytes = 4;
		numBytes = sizeof(float);
		break;
	case 11:
		// INTENSITY_SPECTROGRAM_FLOAT float
		//numBytes = 4;
		numBytes = sizeof(float);
		break;
	case 12:
		// ABCD_INT16 int16_t[4]
		//numBytes = 8;
		numBytes = sizeof(int16_t[4]);
		break;
	case 13:
		// FLOW_INJECTION float
		//numBytes = 4;
		numBytes = sizeof(float);
		break;
	case 14:
		// FLOW_RELATIVE float
		//numBytes = 4;
		numBytes = sizeof(float);
		break;
	case 15:
		// FLOW_PRODUCTION float
		//numBytes = 4;
		numBytes = sizeof(float);
		break;
	case 16:
		// AMPLITUDE_QUAD float[4]
		//numBytes = 16;
		numBytes = sizeof(float[4]);
		break;
	case 17:
		// DPHASE_FLOAT float
		//numBytes = 2;
		numBytes = sizeof(float);
		break;
	case 18:
		// MINMAX_FLOAT float
		//numBytes = 2;
		numBytes = sizeof(float);
		break;
	case 19:
		// IQ_FLOAT float[2]
		//numBytes = 8;
		numBytes = sizeof(float[2]);
		break;
	case 20:
		// COMPLEX_FLOAT float[2]
		//numBytes = 8;
		numBytes = sizeof(float[2]);
		break;
	case 21:
		// ABCD_INT16_RAW int16_t[4]
		//numBytes = 8;
		numBytes = sizeof(int16_t[4]);
		break;
	case 22:
		// IQ_INT16_RAW int16_t[2]
		//numBytes = 4;
		numBytes = sizeof(int16_t[2]);
		break;
	case 23:
		// IQIQ_INT16_RAW int16_t[4]
		//numBytes = 8;
		numBytes = sizeof(int16_t[4]);
		break;
	case 24:
		// REAL_FLOAT float
		//numBytes = 4;
		numBytes = sizeof(float);
		break;
	case 25:
		// FLOW_EROSION float
		//numBytes = 4;
		numBytes = sizeof(float);
		break;
	case 26:
		// STATIC_PHASE_FLOAT float
		//numBytes = 4;
		numBytes = sizeof(float);
		break;
	case 27:
		// PHASE_VARIANCE_FLOAT float
		//numBytes = 4;
		numBytes = sizeof(float);
		break;
	case 28:
		// PHASE_POWER_FLOAT
		//numBytes = 4;
		numBytes = sizeof(float);
		break;
	case 29:
		// QUALITY_FLOAT float
		//numBytes = 4;
		numBytes = sizeof(float);
		break;
	case 30:
		// STRAIN_FLOAT float
		//numBytes = 4;
		numBytes = sizeof(float);
		break;
	default:
		// NONE
		numBytes = 0;
	}
	return numBytes;
}

void readBinaryDataBlock(FILE* fptr,
	void* A, const size_t LDA, const size_t LDB, const size_t sampleSize)
{
	fread(A, sampleSize, LDA * LDB, fptr);
}

int16_t getHeaderVersion(FILE* fptr) 
{
	int64_t Preamble;
	int16_t Version;
	if (fptr == NULL) {
		return -1;
	}
	fread(&Preamble, sizeof(int64_t), 1, fptr);
	fread(&Version, sizeof(int16_t), 1, fptr);
	if (Preamble != 0x4441535F46696C65) {
		fclose(fptr);
		return -1;
	}
	else 
	{
		return Version;
	}
}

void makeMexHeader3(mxArray* plhs[], DASFileHeader3_T* dasHeader)
{
	plhs[0] = mxCreateStructMatrix(1, 1, nField3, FieldName3);
	// Allocate memory for header data
	mxArray* preamble = mxCreateNumericMatrix(1, 1, mxINT64_CLASS, mxREAL);
	mxArray* version = mxCreateNumericMatrix(1, 1, mxINT16_CLASS, mxREAL);
	mxArray* mode = mxCreateNumericMatrix(1, 1, mxINT16_CLASS, mxREAL);
	mxArray* software_name = mxCreateNumericMatrix(1, SoftwareNameLength, mxINT8_CLASS, mxREAL);
	mxArray* content = mxCreateNumericMatrix(1, 1, mxINT32_CLASS, mxREAL);
	mxArray* block_size = mxCreateNumericMatrix(1, 1, mxINT64_CLASS, mxREAL);
	mxArray* frame_orientation = mxCreateNumericMatrix(1, 1, mxINT32_CLASS, mxREAL);
	mxArray* frame_datatype = mxCreateNumericMatrix(1, 1, mxINT32_CLASS, mxREAL);
	mxArray* frame_offset = mxCreateNumericMatrix(1, 1, mxINT64_CLASS, mxREAL);
	mxArray* quality_orientation = mxCreateNumericMatrix(1, 1, mxINT32_CLASS, mxREAL);
	mxArray* quality_datatype = mxCreateNumericMatrix(1, 1, mxINT32_CLASS, mxREAL);
	mxArray* quality_offset = mxCreateNumericMatrix(1, 1, mxINT64_CLASS, mxREAL);
	mxArray* quality_block_size = mxCreateNumericMatrix(1, 1, mxINT64_CLASS, mxREAL);
	mxArray* year = mxCreateNumericMatrix(1, 1, mxINT16_CLASS, mxREAL);
	mxArray* month = mxCreateNumericMatrix(1, 1, mxINT16_CLASS, mxREAL);
	mxArray* day = mxCreateNumericMatrix(1, 1, mxINT16_CLASS, mxREAL);
	mxArray* hour = mxCreateNumericMatrix(1, 1, mxINT16_CLASS, mxREAL);
	mxArray* minute = mxCreateNumericMatrix(1, 1, mxINT16_CLASS, mxREAL);
	mxArray* second = mxCreateNumericMatrix(1, 1, mxINT16_CLASS, mxREAL);
	mxArray* microsecond = mxCreateNumericMatrix(1, 1, mxINT32_CLASS, mxREAL);
	mxArray* tz_offset = mxCreateNumericMatrix(1, 1, mxINT16_CLASS, mxREAL);
	mxArray* sampling_rate = mxCreateNumericMatrix(1, 1, mxDOUBLE_CLASS, mxREAL);
	mxArray* frame_capacity = mxCreateNumericMatrix(1, 1, mxINT64_CLASS, mxREAL);
	mxArray* number_of_frames = mxCreateNumericMatrix(1, 1, mxINT64_CLASS, mxREAL);
	mxArray* compression = mxCreateNumericMatrix(1, 1, mxINT64_CLASS, mxREAL);
	mxArray* number_of_channels = mxCreateNumericMatrix(1, 1, mxINT32_CLASS, mxREAL);
	mxArray* zones_offset = mxCreateNumericMatrix(1, 1, mxINT64_CLASS, mxREAL);
	mxArray* reserved = mxCreateNumericMatrix(1, PadLength3, mxINT8_CLASS, mxREAL);
	mxArray* local_year = mxCreateNumericMatrix(1, 1, mxINT16_CLASS, mxREAL);
	mxArray* local_month = mxCreateNumericMatrix(1, 1, mxINT16_CLASS, mxREAL);
	mxArray* local_day = mxCreateNumericMatrix(1, 1, mxINT16_CLASS, mxREAL);
	mxArray* local_hour = mxCreateNumericMatrix(1, 1, mxINT16_CLASS, mxREAL);
	mxArray* local_minute = mxCreateNumericMatrix(1, 1, mxINT16_CLASS, mxREAL);
	mxArray* local_second = mxCreateNumericMatrix(1, 1, mxINT16_CLASS, mxREAL);
	mxArray* local_microsecond = mxCreateNumericMatrix(1, 1, mxINT32_CLASS, mxREAL);

	*((int64_t*)mxGetData(preamble)) = dasHeader->Preamble;
	*((int16_t*)mxGetData(version)) = dasHeader->Version;
	*((int16_t*)mxGetData(mode)) = dasHeader->Mode;
	*((char**)mxGetData(software_name)) = dasHeader->SoftwareName;
	*((int32_t*)mxGetData(content)) = dasHeader->Content;
	*((int64_t*)mxGetData(block_size)) = dasHeader->BlockSize;
	*((int32_t*)mxGetData(frame_orientation)) = dasHeader->FrameOrientation;
	*((int32_t*)mxGetData(frame_datatype)) = dasHeader->FrameDataType;
	*((int64_t*)mxGetData(frame_offset)) = dasHeader->FrameOffset;
	*((int32_t*)mxGetData(quality_orientation)) = dasHeader->QualityOrientation;
	*((int32_t*)mxGetData(quality_datatype)) = dasHeader->QualityDataType;
	*((int64_t*)mxGetData(quality_offset)) = dasHeader->QualityOffset;
	*((int64_t*)mxGetData(quality_block_size)) = dasHeader->QualityBlockSize;
	*((int16_t*)mxGetData(year)) = dasHeader->Year;
	*((int16_t*)mxGetData(month)) = dasHeader->Month;
	*((int16_t*)mxGetData(day)) = dasHeader->Day;
	*((int16_t*)mxGetData(hour)) = dasHeader->Hour;
	*((int16_t*)mxGetData(minute)) = dasHeader->Minute;
	*((int16_t*)mxGetData(second)) = dasHeader->Second;
	*((int32_t*)mxGetData(microsecond)) = dasHeader->Microsecond;
	*((int16_t*)mxGetData(tz_offset)) = dasHeader->TZOffset;
	*((double*)mxGetData(sampling_rate)) = dasHeader->SamplingRate;
	*((int64_t*)mxGetData(frame_capacity)) = dasHeader->FrameCapacity;
	*((int64_t*)mxGetData(number_of_frames)) = dasHeader->NumberOfFrames;
	*((int64_t*)mxGetData(compression)) = dasHeader->Compression;
	*((int16_t*)mxGetData(number_of_channels)) = dasHeader->NumberOfChannels;
	*((int64_t*)mxGetData(zones_offset)) = dasHeader->ZonesOffset;
	*((int8_t**)mxGetData(reserved)) = dasHeader->Reserved;
	*((int16_t*)mxGetData(local_year)) = dasHeader->LocalYear;
	*((int16_t*)mxGetData(local_month)) = dasHeader->LocalMonth;
	*((int16_t*)mxGetData(local_day)) = dasHeader->LocalDay;
	*((int16_t*)mxGetData(local_hour)) = dasHeader->LocalHour;
	*((int16_t*)mxGetData(local_minute)) = dasHeader->LocalMinute;
	*((int16_t*)mxGetData(local_second)) = dasHeader->LocalSecond;
	*((int32_t*)mxGetData(local_microsecond)) = dasHeader->LocalMicrosecond;

	mxSetFieldByNumber(plhs[0], 0, 0, preamble);
	mxSetFieldByNumber(plhs[0], 0, 1, version);
	mxSetFieldByNumber(plhs[0], 0, 2, mode);
	mxSetFieldByNumber(plhs[0], 0, 3, software_name);
	mxSetFieldByNumber(plhs[0], 0, 4, content);
	mxSetFieldByNumber(plhs[0], 0, 5, block_size);
	mxSetFieldByNumber(plhs[0], 0, 6, frame_orientation);
	mxSetFieldByNumber(plhs[0], 0, 7, frame_datatype);
	mxSetFieldByNumber(plhs[0], 0, 8, frame_offset);
	mxSetFieldByNumber(plhs[0], 0, 9, quality_orientation);
	mxSetFieldByNumber(plhs[0], 0, 10, quality_datatype);
	mxSetFieldByNumber(plhs[0], 0, 11, quality_offset);
	mxSetFieldByNumber(plhs[0], 0, 12, quality_block_size);
	mxSetFieldByNumber(plhs[0], 0, 13, year);
	mxSetFieldByNumber(plhs[0], 0, 14, month);
	mxSetFieldByNumber(plhs[0], 0, 15, day);
	mxSetFieldByNumber(plhs[0], 0, 16, hour);
	mxSetFieldByNumber(plhs[0], 0, 17, minute);
	mxSetFieldByNumber(plhs[0], 0, 18, second);
	mxSetFieldByNumber(plhs[0], 0, 19, microsecond);
	mxSetFieldByNumber(plhs[0], 0, 20, tz_offset);
	mxSetFieldByNumber(plhs[0], 0, 21, sampling_rate);
	mxSetFieldByNumber(plhs[0], 0, 22, frame_capacity);
	mxSetFieldByNumber(plhs[0], 0, 23, number_of_frames);
	mxSetFieldByNumber(plhs[0], 0, 24, compression);
	mxSetFieldByNumber(plhs[0], 0, 25, number_of_channels);
	mxSetFieldByNumber(plhs[0], 0, 26, zones_offset);
	mxSetFieldByNumber(plhs[0], 0, 27, reserved);
	mxSetFieldByNumber(plhs[0], 0, 28, local_year);
	mxSetFieldByNumber(plhs[0], 0, 29, local_month);
	mxSetFieldByNumber(plhs[0], 0, 30, local_day);
	mxSetFieldByNumber(plhs[0], 0, 31, local_hour);
	mxSetFieldByNumber(plhs[0], 0, 32, local_minute);
	mxSetFieldByNumber(plhs[0], 0, 33, local_second);
	mxSetFieldByNumber(plhs[0], 0, 34, local_microsecond);
}

void makeMexHeader4(mxArray* plhs[], DASFileHeader4_T* dasHeader)
{

	plhs[0] = mxCreateStructMatrix(1, 1, nField4, FieldName4);
	// Allocate memory for header data
	mxArray* preamble = mxCreateNumericMatrix(1, 1, mxINT64_CLASS, mxREAL);
	mxArray* version = mxCreateNumericMatrix(1, 1, mxINT16_CLASS, mxREAL);
	mxArray* mode = mxCreateNumericMatrix(1, 1, mxINT16_CLASS, mxREAL);
	mxArray* software_name = mxCreateNumericMatrix(1, SoftwareNameLength, mxINT8_CLASS, mxREAL);
	mxArray* content = mxCreateNumericMatrix(1, 1, mxINT32_CLASS, mxREAL);
	mxArray* block_size = mxCreateNumericMatrix(1, 1, mxINT64_CLASS, mxREAL);
	mxArray* frame_orientation = mxCreateNumericMatrix(1, 1, mxINT32_CLASS, mxREAL);
	mxArray* frame_datatype = mxCreateNumericMatrix(1, 1, mxINT32_CLASS, mxREAL);
	mxArray* frame_offset = mxCreateNumericMatrix(1, 1, mxINT64_CLASS, mxREAL);
	mxArray* quality_orientation = mxCreateNumericMatrix(1, 1, mxINT32_CLASS, mxREAL);
	mxArray* quality_datatype = mxCreateNumericMatrix(1, 1, mxINT32_CLASS, mxREAL);
	mxArray* quality_offset = mxCreateNumericMatrix(1, 1, mxINT64_CLASS, mxREAL);
	mxArray* quality_block_size = mxCreateNumericMatrix(1, 1, mxINT64_CLASS, mxREAL);
	mxArray* year = mxCreateNumericMatrix(1, 1, mxINT16_CLASS, mxREAL);
	mxArray* month = mxCreateNumericMatrix(1, 1, mxINT16_CLASS, mxREAL);
	mxArray* day = mxCreateNumericMatrix(1, 1, mxINT16_CLASS, mxREAL);
	mxArray* hour = mxCreateNumericMatrix(1, 1, mxINT16_CLASS, mxREAL);
	mxArray* minute = mxCreateNumericMatrix(1, 1, mxINT16_CLASS, mxREAL);
	mxArray* second = mxCreateNumericMatrix(1, 1, mxINT16_CLASS, mxREAL);
	mxArray* microsecond = mxCreateNumericMatrix(1, 1, mxINT32_CLASS, mxREAL);
	mxArray* tz_offset = mxCreateNumericMatrix(1, 1, mxINT16_CLASS, mxREAL);
	mxArray* sampling_rate = mxCreateNumericMatrix(1, 1, mxDOUBLE_CLASS, mxREAL);
	mxArray* frame_capacity = mxCreateNumericMatrix(1, 1, mxINT64_CLASS, mxREAL);
	mxArray* number_of_frames = mxCreateNumericMatrix(1, 1, mxINT64_CLASS, mxREAL);
	mxArray* compression = mxCreateNumericMatrix(1, 1, mxINT64_CLASS, mxREAL);
	mxArray* number_of_channels = mxCreateNumericMatrix(1, 1, mxINT32_CLASS, mxREAL);
	mxArray* zones_offset = mxCreateNumericMatrix(1, 1, mxINT64_CLASS, mxREAL);
	// these 3 fields differ from v3 header
	mxArray* depth_calibration_offset = mxCreateNumericMatrix(1, 1, mxINT64_CLASS, mxREAL);
	mxArray* nominal_depth_offset = mxCreateNumericMatrix(1, 1, mxINT64_CLASS, mxREAL);
	mxArray* measured_depth_offset = mxCreateNumericMatrix(1, 1, mxINT64_CLASS, mxREAL);
	// end diff
	mxArray* reserved = mxCreateNumericMatrix(1, PadLength4, mxINT8_CLASS, mxREAL);
	// these 3 field differ from v3 header
	mxArray* digitizer_rate = mxCreateNumericMatrix(1, 1, mxDOUBLE_CLASS, mxREAL);
	mxArray* delay_coil_length = mxCreateNumericMatrix(1, 1, mxDOUBLE_CLASS, mxREAL);
	mxArray* index_of_refraction = mxCreateNumericMatrix(1, 1, mxDOUBLE_CLASS, mxREAL);
	// end diff
	mxArray* local_year = mxCreateNumericMatrix(1, 1, mxINT16_CLASS, mxREAL);
	mxArray* local_month = mxCreateNumericMatrix(1, 1, mxINT16_CLASS, mxREAL);
	mxArray* local_day = mxCreateNumericMatrix(1, 1, mxINT16_CLASS, mxREAL);
	mxArray* local_hour = mxCreateNumericMatrix(1, 1, mxINT16_CLASS, mxREAL);
	mxArray* local_minute = mxCreateNumericMatrix(1, 1, mxINT16_CLASS, mxREAL);
	mxArray* local_second = mxCreateNumericMatrix(1, 1, mxINT16_CLASS, mxREAL);
	mxArray* local_microsecond = mxCreateNumericMatrix(1, 1, mxINT32_CLASS, mxREAL);

	*((int64_t*)mxGetData(preamble)) = dasHeader->Preamble;
	*((int16_t*)mxGetData(version)) = dasHeader->Version;
	*((int16_t*)mxGetData(mode)) = dasHeader->Mode;
	*((char**)mxGetData(software_name)) = dasHeader->SoftwareName;
	*((int32_t*)mxGetData(content)) = dasHeader->Content;
	*((int64_t*)mxGetData(block_size)) = dasHeader->BlockSize;
	*((int32_t*)mxGetData(frame_orientation)) = dasHeader->FrameOrientation;
	*((int32_t*)mxGetData(frame_datatype)) = dasHeader->FrameDataType;
	*((int64_t*)mxGetData(frame_offset)) = dasHeader->FrameOffset;
	*((int32_t*)mxGetData(quality_orientation)) = dasHeader->QualityOrientation;
	*((int32_t*)mxGetData(quality_datatype)) = dasHeader->QualityDataType;
	*((int64_t*)mxGetData(quality_offset)) = dasHeader->QualityOffset;
	*((int64_t*)mxGetData(quality_block_size)) = dasHeader->QualityBlockSize;
	*((int16_t*)mxGetData(year)) = dasHeader->Year;
	*((int16_t*)mxGetData(month)) = dasHeader->Month;
	*((int16_t*)mxGetData(day)) = dasHeader->Day;
	*((int16_t*)mxGetData(hour)) = dasHeader->Hour;
	*((int16_t*)mxGetData(minute)) = dasHeader->Minute;
	*((int16_t*)mxGetData(second)) = dasHeader->Second;
	*((int32_t*)mxGetData(microsecond)) = dasHeader->Microsecond;
	*((int16_t*)mxGetData(tz_offset)) = dasHeader->TZOffset;
	*((double*)mxGetData(sampling_rate)) = dasHeader->SamplingRate;
	*((int64_t*)mxGetData(frame_capacity)) = dasHeader->FrameCapacity;
	*((int64_t*)mxGetData(number_of_frames)) = dasHeader->NumberOfFrames;
	*((int64_t*)mxGetData(compression)) = dasHeader->Compression;
	*((int16_t*)mxGetData(number_of_channels)) = dasHeader->NumberOfChannels;
	*((int64_t*)mxGetData(zones_offset)) = dasHeader->ZonesOffset;
	// +diff
	*((int64_t*)mxGetData(depth_calibration_offset)) = dasHeader->DepthCalibrationOffset;
	*((int64_t*)mxGetData(nominal_depth_offset)) = dasHeader->NominalDepthOffset;
	*((int64_t*)mxGetData(measured_depth_offset)) = dasHeader->MeasuredDepthOffset;
	// +diff
	*((int8_t**)mxGetData(reserved)) = dasHeader->Reserved;
	// +diff
	*((double*)mxGetData(digitizer_rate)) = dasHeader->DigitizerRate;
	*((double*)mxGetData(delay_coil_length)) = dasHeader->DelayCoilLength;
	*((double*)mxGetData(index_of_refraction)) = dasHeader->IndexOfRefraction;
	// +diff
	*((int16_t*)mxGetData(local_year)) = dasHeader->LocalYear;
	*((int16_t*)mxGetData(local_month)) = dasHeader->LocalMonth;
	*((int16_t*)mxGetData(local_day)) = dasHeader->LocalDay;
	*((int16_t*)mxGetData(local_hour)) = dasHeader->LocalHour;
	*((int16_t*)mxGetData(local_minute)) = dasHeader->LocalMinute;
	*((int16_t*)mxGetData(local_second)) = dasHeader->LocalSecond;
	*((int32_t*)mxGetData(local_microsecond)) = dasHeader->LocalMicrosecond;

	//kField = 0;
	mxSetFieldByNumber(plhs[0], 0, 0, preamble);
	mxSetFieldByNumber(plhs[0], 0, 1, version);
	mxSetFieldByNumber(plhs[0], 0, 2, mode);
	mxSetFieldByNumber(plhs[0], 0, 3, software_name);
	mxSetFieldByNumber(plhs[0], 0, 4, content);
	mxSetFieldByNumber(plhs[0], 0, 5, block_size);
	mxSetFieldByNumber(plhs[0], 0, 6, frame_orientation);
	mxSetFieldByNumber(plhs[0], 0, 7, frame_datatype);
	mxSetFieldByNumber(plhs[0], 0, 8, frame_offset);
	mxSetFieldByNumber(plhs[0], 0, 9, quality_orientation);
	mxSetFieldByNumber(plhs[0], 0, 10, quality_datatype);
	mxSetFieldByNumber(plhs[0], 0, 11, quality_offset);
	mxSetFieldByNumber(plhs[0], 0, 12, quality_block_size);
	mxSetFieldByNumber(plhs[0], 0, 13, year);
	mxSetFieldByNumber(plhs[0], 0, 14, month);
	mxSetFieldByNumber(plhs[0], 0, 15, day);
	mxSetFieldByNumber(plhs[0], 0, 16, hour);
	mxSetFieldByNumber(plhs[0], 0, 17, minute);
	mxSetFieldByNumber(plhs[0], 0, 18, second);
	mxSetFieldByNumber(plhs[0], 0, 19, microsecond);
	mxSetFieldByNumber(plhs[0], 0, 20, tz_offset);
	mxSetFieldByNumber(plhs[0], 0, 21, sampling_rate);
	mxSetFieldByNumber(plhs[0], 0, 22, frame_capacity);
	mxSetFieldByNumber(plhs[0], 0, 23, number_of_frames);
	mxSetFieldByNumber(plhs[0], 0, 24, compression);
	mxSetFieldByNumber(plhs[0], 0, 25, number_of_channels);
	mxSetFieldByNumber(plhs[0], 0, 26, zones_offset);
	// +diff
	mxSetFieldByNumber(plhs[0], 0, 27, depth_calibration_offset);
	mxSetFieldByNumber(plhs[0], 0, 28, nominal_depth_offset);
	mxSetFieldByNumber(plhs[0], 0, 29, measured_depth_offset);
	// +diff
	mxSetFieldByNumber(plhs[0], 0, 30, reserved);
	// +diff
	mxSetFieldByNumber(plhs[0], 0, 31, digitizer_rate);
	mxSetFieldByNumber(plhs[0], 0, 32, delay_coil_length);
	mxSetFieldByNumber(plhs[0], 0, 33, index_of_refraction);
	// +diff
	mxSetFieldByNumber(plhs[0], 0, 34, local_year);
	mxSetFieldByNumber(plhs[0], 0, 35, local_month);
	mxSetFieldByNumber(plhs[0], 0, 36, local_day);
	mxSetFieldByNumber(plhs[0], 0, 37, local_hour);
	mxSetFieldByNumber(plhs[0], 0, 38, local_minute);
	mxSetFieldByNumber(plhs[0], 0, 39, local_second);
	mxSetFieldByNumber(plhs[0], 0, 40, local_microsecond);
}

// convert a v3 das header to a v4 das header
DASFileHeader4_T convertHeaderV3ToHeaderV4(DASFileHeader3_T* dasHeader3)
{
	//int8_t _reserved[PadLength4] = { 0 };
	// TODO: is it possible to access and write the correct gauge length?
	DASFileHeader4_T dasHeader4 = {
		.Preamble = dasHeader3->Preamble,
		.Version = dasHeader3->Version,
		.Mode = dasHeader3->Mode,
		//.SoftwareName = dasHeader3->SoftwareName,
		.Content = dasHeader3->Content,
		.FrameOrientation = dasHeader3->FrameOrientation,
		.FrameDataType = dasHeader3->FrameDataType,
		.FrameOffset = dasHeader3->FrameOffset,
		.QualityOrientation = dasHeader3->QualityOrientation,
		.QualityDataType = dasHeader3->QualityDataType,
		.QualityOffset = dasHeader3->QualityOffset,
		.QualityBlockSize = dasHeader3->QualityBlockSize,
		.Year = dasHeader3->Year,
		.Month = dasHeader3->Month,
		.Day = dasHeader3->Day,
		.Hour = dasHeader3->Hour,
		.Minute = dasHeader3->Minute,
		.Second = dasHeader3->Second,
		.Microsecond = dasHeader3->Microsecond,
		.TZOffset = dasHeader3->TZOffset,
		.SamplingRate = dasHeader3->SamplingRate,
		.FrameCapacity = dasHeader3->FrameCapacity,
		.NumberOfFrames = dasHeader3->NumberOfFrames,
		.Compression = dasHeader3->Compression,
		.NumberOfChannels = dasHeader3->NumberOfChannels,
		.ZonesOffset = dasHeader3->ZonesOffset,
		.DepthCalibrationOffset = 0,
		.NominalDepthOffset = 0,
		.NominalDepthOffset = 0,
		//.Reserved = _reserved,
		.DigitizerRate = 100000000.0,
		.DelayCoilLength = 5.0,
		.IndexOfRefraction = 1.4682,
		.LocalYear = dasHeader3->LocalYear,
		.LocalMonth = dasHeader3->LocalMonth,
		.LocalDay = dasHeader3->LocalDay,
		.LocalHour = dasHeader3->LocalHour,
		.LocalMinute = dasHeader3->LocalMinute,
		.LocalSecond = dasHeader3->LocalSecond,
		.LocalMicrosecond = dasHeader3->LocalMicrosecond
	};
	memcpy(&(dasHeader4.SoftwareName), &(dasHeader3->SoftwareName), SoftwareNameLength);
	memset(&(dasHeader4.Reserved), 0, PadLength4 * sizeof(int8_t));
	//memcpy(&(dasHeader4.Reserved), &_reserved, PadLength4);
	return dasHeader4;
}

// convert a v4 das header to a v3 das header 
DASFileHeader3_T convertHeaderV4ToHeaderV3(DASFileHeader4_T* dasHeader4)
{
	//int8_t _reserved[PadLength3] = { 0 };
	DASFileHeader3_T dasHeader3 = {
		.Preamble = dasHeader4->Preamble,
		.Version = dasHeader4->Version,
		.Mode = dasHeader4->Mode,
		//.SoftwareName = dasHeader4->SoftwareName,
		.Content = dasHeader4->Content,
		.FrameOrientation = dasHeader4->FrameOrientation,
		.FrameDataType = dasHeader4->FrameDataType,
		.FrameOffset = dasHeader4->FrameOffset,
		.QualityOrientation = dasHeader4->QualityOrientation,
		.QualityDataType = dasHeader4->QualityDataType,
		.QualityOffset = dasHeader4->QualityOffset,
		.QualityBlockSize = dasHeader4->QualityBlockSize,
		.Year = dasHeader4->Year,
		.Month = dasHeader4->Month,
		.Day = dasHeader4->Day,
		.Hour = dasHeader4->Hour,
		.Minute = dasHeader4->Minute,
		.Second = dasHeader4->Second,
		.Microsecond = dasHeader4->Microsecond,
		.TZOffset = dasHeader4->TZOffset,
		.SamplingRate = dasHeader4->SamplingRate,
		.FrameCapacity = dasHeader4->FrameCapacity,
		.NumberOfFrames = dasHeader4->NumberOfFrames,
		.Compression = dasHeader4->Compression,
		.NumberOfChannels = dasHeader4->NumberOfChannels,
		.ZonesOffset = dasHeader4->ZonesOffset,
		//.Reserved = _reserved,
		.LocalYear = dasHeader4->LocalYear,
		.LocalMonth = dasHeader4->LocalMonth,
		.LocalDay = dasHeader4->LocalDay,
		.LocalHour = dasHeader4->LocalHour,
		.LocalMinute = dasHeader4->LocalMinute,
		.LocalSecond = dasHeader4->LocalSecond,
		.LocalMicrosecond = dasHeader4->LocalMicrosecond
	};
	memcpy(&(dasHeader3.SoftwareName), &(dasHeader4->SoftwareName), SoftwareNameLength);
	memset(&(dasHeader3.Reserved), 0, PadLength3 * sizeof(int8_t));
	//memcpy(&(dasHeader3.Reserved), _reserved, PadLength3);
	return dasHeader3;
}

size_t getNumberOfZones(FILE* fptr, int64_t ZonesOffset)
{
	int32_t NumberOfZones = 0;
	if (fptr != NULL)
	{
		fseek(fptr, ZonesOffset, SEEK_SET);
		fread(&NumberOfZones, sizeof(int32_t), 1, fptr);
	}
	return (size_t)NumberOfZones;
}

size_t getNumberOfDepthCalibrationPoints(FILE* fptr, int64_t DepthCalibrationOffset)
{
	int32_t NumberOfPoints = 0;
	if (fptr != NULL)
	{
		fseek(fptr, DepthCalibrationOffset, SEEK_SET);
		fread(&NumberOfPoints, sizeof(int32_t), 1, fptr);
	}
	return (size_t)NumberOfPoints;
}

int32_t* getZoneData(FILE* fptr, int64_t ZonesOffset, size_t NumberOfZones)
{
	if (fptr == NULL)
	{
		return NULL;
	}
	fseek(fptr, ZonesOffset, SEEK_SET);
	size_t nArrayElem = 3 * NumberOfZones + 1;
	int32_t* Zones = (int32_t*)calloc(nArrayElem, sizeof(int32_t));
	if (Zones != NULL) 
	{
		fread(Zones, sizeof(int32_t), nArrayElem, fptr);
	}
	return Zones; // caller needs to free
}

double* getDepthCalibrationData(FILE* fptr, int64_t DepthCalibrationOffset, size_t NumberOfPoints)
{
	if (fptr == NULL)
	{
		return NULL;
	}
	fseek(fptr, DepthCalibrationOffset + sizeof(int32_t), SEEK_SET);
	size_t nArrayElem = 2 * NumberOfPoints;
	double* DepthCalibration = (double*)calloc(nArrayElem, sizeof(double));
	if (DepthCalibration != NULL)
	{
		fread(DepthCalibration, sizeof(int32_t), nArrayElem, fptr);
	}
	return DepthCalibration; // caller needs to free
}

float* getNominalDepthData(FILE* fptr, int64_t NominalDepthOffset, size_t NumberOfChannels)
{
	if (fptr == NULL)
	{
		return NULL;
	}
	fseek(fptr, NominalDepthOffset, SEEK_SET);
	float* NominalDepths = (float*)calloc(NumberOfChannels, sizeof(float));
	if (NominalDepths != NULL)
	{
		fread(NominalDepths, sizeof(float), NumberOfChannels, fptr);
	}
	return NominalDepths; // caller needs to free
}

float* getMeasuredDepthData(FILE* fptr, int64_t MeasuredDepthOffset, size_t NumberOfChannels)
{
	if (fptr == NULL)
	{
		return NULL;
	}
	fseek(fptr, MeasuredDepthOffset, SEEK_SET);
	float* MeasuredDepths = (float*)calloc(NumberOfChannels, sizeof(float));

	if (MeasuredDepths != NULL)
	{
		fread(MeasuredDepths, sizeof(float), NumberOfChannels, fptr);
	}

	return MeasuredDepths; // caller needs to free
}

void getMexZoneData(mxArray* plhs[], size_t arrayIdx, FILE* fptr, int64_t ZonesOffset)
{
	size_t NumberOfZones = getNumberOfZones(fptr, ZonesOffset);
	size_t nArrayElem = 3 * NumberOfZones + 1;
	int32_t* Zones = getZoneData(fptr, ZonesOffset, NumberOfZones);
	
	if (Zones == NULL)
	{
		return;
	}

	// allocate matlab output array
	plhs[arrayIdx] = mxCreateNumericMatrix(1, nArrayElem, mxINT32_CLASS, mxREAL);
	
	int32_t* mxZones = (int32_t*)mxGetData(plhs[arrayIdx]);

	// TODO: determine if memcpy will work for C array into mxArray
	for (size_t k = 0; k < nArrayElem; k++)
	{
		*(mxZones + k) = *(Zones + k);
	}

	free(Zones);
}

void getMexDepthCalData(mxArray* plhs[], size_t arrayIdx, FILE* fptr, int64_t DepthCalibrationOffset)
{
	size_t NumberOfPoints = getNumberOfDepthCalibrationPoints(fptr, DepthCalibrationOffset);
	double* DepthCalibration = getDepthCalibrationData(fptr, DepthCalibrationOffset, NumberOfPoints);
	
	if (DepthCalibration == NULL)
	{
		return;
	}

	plhs[arrayIdx] = mxCreateNumericMatrix(NumberOfPoints, 2, mxDOUBLE_CLASS, mxREAL);

	double* mxDepthCal = (double*)mxGetData(plhs[arrayIdx]);

	// TODO: determine if memcpy will work for C array into mxArray
	for (size_t k = 0; k < NumberOfPoints; k++)
	{
		*(mxDepthCal + k) = *(DepthCalibration + 2 * k);
		*(mxDepthCal + k + NumberOfPoints) = *(DepthCalibration + 2 * k + 1);
	}

	free(DepthCalibration);
}

void getMexNominalDepthData(mxArray* plhs[], size_t arrayIdx, FILE* fptr, int64_t NominalDepthOffset, size_t NumberOfChannels)
{
	float* NominalDepths = getNominalDepthData(fptr, NominalDepthOffset, NumberOfChannels);
	
	if (NominalDepths == NULL)
	{
		return;
	}

	plhs[arrayIdx] = mxCreateNumericMatrix(NumberOfChannels, 1, mxSINGLE_CLASS, mxREAL);

	float* mxNominalDepths = (float*)mxGetData(plhs[arrayIdx]);

	// TODO: determine if memcpy will work for C array into mxArray
	for (size_t k = 0; k < NumberOfChannels; k++)
	{
		*(mxNominalDepths + k) = *(NominalDepths + k);
	}

	free(NominalDepths);
}

void getMexMeasuredDepthData(mxArray* plhs[], size_t arrayIdx, FILE* fptr, int64_t MeasuredDepthOffset, size_t NumberOfChannels)
{
	float* MeasuredDepths = getMeasuredDepthData(fptr, MeasuredDepthOffset, NumberOfChannels);

	if (MeasuredDepths == NULL)
	{
		return;
	}

	plhs[arrayIdx] = mxCreateNumericMatrix(NumberOfChannels, 1, mxSINGLE_CLASS, mxREAL);

	float* mxMeasuredDepths = (float*)mxGetData(plhs[arrayIdx]);

	// TODO: determine if memcpy will work for C array into mxArray
	for (size_t k = 0; k < NumberOfChannels; k++)
	{
		*(mxMeasuredDepths + k) = *(MeasuredDepths + k);
	}

	free(MeasuredDepths);
}

int32_t makeEmptyDepthCalibrationBlock()
{
	return 0;
}

float* makeNominalDepthBlock(size_t NumberOfChannels)
{
	float* NominalDepths = calloc(NumberOfChannels, sizeof(float));
	if (NominalDepths != NULL)
	{
		for (size_t k = 0; k < NumberOfChannels; k++)
		{
			NominalDepths[k] = k * MetersPerChannel;
		}
	}
	return NominalDepths;
}

float* makeMeasuredDepthBlock(size_t NumberOfChannels)
{
	return makeNominalDepthBlock(NumberOfChannels);
	// TODO: inhale depth calibration as parameters in future
}

void getHeaderData(void* dasHeader, int16_t headerVersion,
	size_t* NumberOfFrames, size_t* NumberOfChannels, 
	size_t* frameCapacity, int32_t* frameOrientation, int32_t* frameDataType, size_t* frameOffset,
	int32_t* qualityOrientation, int32_t* qualityDataType, size_t* qualityOffset, int64_t* qualityBlockSize)
{
	switch (headerVersion) 
	{
	case 0:
		*NumberOfFrames = ((DASFileHeader0_T*)dasHeader)->NumberOfFrames;
		*frameCapacity = ((DASFileHeader0_T*)dasHeader)->FrameCapacity;
		// use defaults except for number of channels
		*frameOrientation = 1;
		*frameDataType = 3;
		*qualityOrientation = 0;
		*qualityDataType = 0;
		*qualityOffset = 0;
		*qualityBlockSize = 0;

		break;
	case 1:
		*NumberOfFrames = ((DASFileHeader1_T*)dasHeader)->NumberOfFrames;
		*NumberOfChannels = ((DASFileHeader1_T*)dasHeader)->NumberOfChannels;
		
		*frameOrientation = ((DASFileHeader1_T*)dasHeader)->FrameOrientation;
		*frameDataType = ((DASFileHeader1_T*)dasHeader)->FrameDataType;
		*frameCapacity = ((DASFileHeader1_T*)dasHeader)->FrameCapacity;
		*frameOffset = ((DASFileHeader1_T*)dasHeader)->FrameOffset;

		*qualityOrientation= ((DASFileHeader1_T*)dasHeader)->QualityOrientation;
		*qualityDataType = ((DASFileHeader1_T*)dasHeader)->QualityDataType;
		*qualityOffset = ((DASFileHeader1_T*)dasHeader)->QualityOffset;
		*qualityBlockSize = ((DASFileHeader1_T*)dasHeader)->QualityBlockSize;

		break;
	case 2: 
		*NumberOfFrames = ((DASFileHeader2_T*)dasHeader)->NumberOfFrames;
		*NumberOfChannels = ((DASFileHeader2_T*)dasHeader)->NumberOfChannels;

		*frameOrientation = ((DASFileHeader2_T*)dasHeader)->FrameOrientation;
		*frameDataType = ((DASFileHeader2_T*)dasHeader)->FrameDataType;
		*frameCapacity = ((DASFileHeader2_T*)dasHeader)->FrameCapacity;
		*frameOffset = ((DASFileHeader2_T*)dasHeader)->FrameOffset;

		*qualityOrientation = ((DASFileHeader2_T*)dasHeader)->QualityOrientation;
		*qualityDataType = ((DASFileHeader2_T*)dasHeader)->QualityDataType;
		*qualityOffset = ((DASFileHeader2_T*)dasHeader)->QualityOffset;
		*qualityBlockSize = ((DASFileHeader2_T*)dasHeader)->QualityBlockSize;

		break;
	case 3: 
		*NumberOfFrames = ((DASFileHeader3_T*)dasHeader)->NumberOfFrames;
		*NumberOfChannels = ((DASFileHeader3_T*)dasHeader)->NumberOfChannels;

		*frameOrientation = ((DASFileHeader3_T*)dasHeader)->FrameOrientation;
		*frameDataType = ((DASFileHeader3_T*)dasHeader)->FrameDataType;
		*frameCapacity = ((DASFileHeader3_T*)dasHeader)->FrameCapacity;
		*frameOffset = ((DASFileHeader3_T*)dasHeader)->FrameOffset;

		*qualityOrientation = ((DASFileHeader3_T*)dasHeader)->QualityOrientation;
		*qualityDataType = ((DASFileHeader3_T*)dasHeader)->QualityDataType;
		*qualityOffset = ((DASFileHeader3_T*)dasHeader)->QualityOffset;
		*qualityBlockSize = ((DASFileHeader3_T*)dasHeader)->QualityBlockSize;

		break;
	case 4: 
		*NumberOfFrames = ((DASFileHeader4_T*)dasHeader)->NumberOfFrames;
		*NumberOfChannels = ((DASFileHeader4_T*)dasHeader)->NumberOfChannels;

		*frameOrientation = ((DASFileHeader4_T*)dasHeader)->FrameOrientation;
		*frameDataType = ((DASFileHeader4_T*)dasHeader)->FrameDataType;
		*frameCapacity = ((DASFileHeader4_T*)dasHeader)->FrameCapacity;
		*frameOffset = ((DASFileHeader4_T*)dasHeader)->FrameOffset;

		*qualityOrientation = ((DASFileHeader4_T*)dasHeader)->QualityOrientation;
		*qualityDataType = ((DASFileHeader4_T*)dasHeader)->QualityDataType;
		*qualityOffset = ((DASFileHeader4_T*)dasHeader)->QualityOffset;
		*qualityBlockSize = ((DASFileHeader4_T*)dasHeader)->QualityBlockSize;

		break;
	default:
		// e.g. -1
		// TODO: error handling
		return;
	}
}

void allocateOutputMxArray(mxArray* plhs[], size_t arrayIdx, int32_t frameDataType, size_t LDA, size_t LDB)
{
	//plhs[0] = mxCreateNumericMatrix(LDA, LDB, mxSINGLE_CLASS, mxREAL);
	size_t nDim = 3;
	size_t dims[3] = { 1, LDA, LDB };
	mxClassID dataType = mxSINGLE_CLASS; // mxFLOAT_CLASS
	mxComplexity complexityType = mxREAL;
	switch (frameDataType)
	{
	case 1:
		// ABC_INT16 int16_t[3]
		dims[0] = 3;
		dataType = mxINT16_CLASS;
		plhs[arrayIdx] = mxCreateNumericArray(nDim, dims, dataType, complexityType);
		break;
	case 2:
		// IQ_INT16 int16_t[2]
		dims[0] = 2;
		dataType = mxINT16_CLASS;
		plhs[arrayIdx] = mxCreateNumericArray(nDim, dims, dataType, complexityType);
		break;
	case 3:
		// DPHASE_INT16 int16_t
		dataType = mxINT16_CLASS;
		plhs[arrayIdx] = mxCreateNumericMatrix(LDA, LDB, dataType, complexityType);
		break;
	case 4:
		// AMPLITUDE_INT16 int16_t
		dataType = mxINT16_CLASS;
		plhs[arrayIdx] = mxCreateNumericMatrix(LDA, LDB, dataType, complexityType);
		break;
	case 5:
		// AMPLITUDE_FLOAT float
		plhs[arrayIdx] = mxCreateNumericMatrix(LDA, LDB, dataType, complexityType);
		break;
	case 6:
		// PHASE_FLOAT float
		plhs[arrayIdx] = mxCreateNumericMatrix(LDA, LDB, dataType, complexityType);
		break;
	case 7:
		// INTENSITY_FLOAT float
		plhs[arrayIdx] = mxCreateNumericMatrix(LDA, LDB, dataType, complexityType);
		break;
	case 8:
		// VSP_SINGLE_SWEEP_FLOAT float
		plhs[arrayIdx] = mxCreateNumericMatrix(LDA, LDB, dataType, complexityType);
		break;
	case 9:
		// VSP_STACKED_SWEEP_FLOAT float
		plhs[arrayIdx] = mxCreateNumericMatrix(LDA, LDB, dataType, complexityType);
		break;
	case 10:
		// FLOW_FLOAT float
		plhs[arrayIdx] = mxCreateNumericMatrix(LDA, LDB, dataType, complexityType);
		break;
	case 11:
		// INTENSITY_SPECTROGRAM_FLOAT float
		plhs[arrayIdx] = mxCreateNumericMatrix(LDA, LDB, dataType, complexityType);
		break;
	case 12:
		// ABCD_INT16 int16_t[4]
		dims[0] = 4;
		dataType = mxINT16_CLASS;
		plhs[arrayIdx] = mxCreateNumericArray(nDim, dims, dataType, complexityType);
		break;
	case 13:
		// FLOW_INJECTION float
		plhs[arrayIdx] = mxCreateNumericMatrix(LDA, LDB, dataType, complexityType);
		break;
	case 14:
		// FLOW_RELATIVE float
		plhs[arrayIdx] = mxCreateNumericMatrix(LDA, LDB, dataType, complexityType);
		break;
	case 15:
		// FLOW_PRODUCTION float
		plhs[arrayIdx] = mxCreateNumericMatrix(LDA, LDB, dataType, complexityType);
		break;
	case 16:
		// AMPLITUDE_QUAD float[4]
		dims[0] = 4;
		plhs[arrayIdx] = mxCreateNumericArray(nDim, dims, dataType, complexityType);
		break;
	case 17:
		// DPHASE_FLOAT float
		plhs[arrayIdx] = mxCreateNumericMatrix(LDA, LDB, dataType, complexityType);
		break;
	case 18:
		// MINMAX_FLOAT float
		plhs[arrayIdx] = mxCreateNumericMatrix(LDA, LDB, dataType, complexityType);
		break;
	case 19:
		// IQ_FLOAT float[2]
		dims[0] = 2;
		plhs[arrayIdx] = mxCreateNumericArray(nDim, dims, dataType, complexityType);
		break;
	case 20:
		// COMPLEX_FLOAT float[2]
		dims[0] = 2;
		plhs[arrayIdx] = mxCreateNumericArray(nDim, dims, dataType, complexityType);
		break;
	case 21:
		// ABCD_INT16_RAW int16_t[4]
		dims[0] = 4;
		dataType = mxINT16_CLASS;
		plhs[arrayIdx] = mxCreateNumericArray(nDim, dims, dataType, complexityType);
		break;
	case 22:
		// IQ_INT16_RAW int16_t[2]
		dims[0] = 2;
		dataType = mxINT16_CLASS;
		plhs[arrayIdx] = mxCreateNumericArray(nDim, dims, dataType, complexityType);
		break;
	case 23:
		// IQIQ_INT16_RAW int16_t[4]
		dims[0] = 4;
		dataType = mxINT16_CLASS;
		plhs[arrayIdx] = mxCreateNumericArray(nDim, dims, dataType, complexityType);
		break;
	case 24:
		// REAL_FLOAT float
		plhs[arrayIdx] = mxCreateNumericMatrix(LDA, LDB, dataType, complexityType);
		break;
	case 25:
		// FLOW_EROSION float
		plhs[arrayIdx] = mxCreateNumericMatrix(LDA, LDB, dataType, complexityType);
		break;
	case 26:
		// STATIC_PHASE_FLOAT float
		plhs[arrayIdx] = mxCreateNumericMatrix(LDA, LDB, dataType, complexityType);
		break;
	case 27:
		// PHASE_VARIANCE_FLOAT float
		plhs[arrayIdx] = mxCreateNumericMatrix(LDA, LDB, dataType, complexityType);
		break;
	case 28:
		// PHASE_POWER_FLOAT
		plhs[arrayIdx] = mxCreateNumericMatrix(LDA, LDB, dataType, complexityType);
		break;
	case 29:
		// QUALITY_FLOAT float
		plhs[arrayIdx] = mxCreateNumericMatrix(LDA, LDB, dataType, complexityType);
		break;
	case 30:
		// STRAIN_FLOAT float
		plhs[arrayIdx] = mxCreateNumericMatrix(LDA, LDB, dataType, complexityType);
		break;
	default:
		// NONE
		return;
	}
}

// "gateway"
void mexFunction(int nlhs, mxArray* plhs[], int nrhs, const mxArray* prhs[])
{

	char* file_name = mxArrayToString(prhs[0]);
	// read file header
	DASFileHeader0_T dasHeader0;
	DASFileHeader1_T dasHeader1;
	DASFileHeader2_T dasHeader2;
	DASFileHeader3_T dasHeader3;
	DASFileHeader4_T dasHeader4;
	FILE* fptr = fopen(file_name, "rb");
	int16_t headerVersion = getHeaderVersion(fptr);
	rewind(fptr); // necessary?

	// get shape and type of data
	size_t LDA;
	size_t LDB;
	size_t numberOfFrames;
	size_t numberOfChannels;
	size_t frameCapacity;
	int32_t frameOrientation;
	int32_t frameDataType;
	size_t frameOffset;
	int32_t qualityOrientation;
	int32_t qualityDataType;
	size_t qualityOffset;
	int64_t qualityBlockSize;

	size_t outputIdx = 0;

	switch (headerVersion)
	{
	case 0:
		fread(&dasHeader0, sizeof(DASFileHeader0_T), 1, fptr);

		getHeaderData(&dasHeader0, headerVersion, &numberOfFrames, &numberOfChannels,
			&frameCapacity, &frameOrientation, &frameDataType, &frameOffset, 
			&qualityOrientation, &qualityDataType, &qualityOffset, &qualityBlockSize);

		// estimate number of channels from file size
		rewind(fptr);
		fseek(fptr, 0L, SEEK_END);
		size_t fileSize = ftell(fptr);
		frameOffset = sizeof(DASFileHeader0_T);
		size_t nDataByte = fileSize - sizeof(DASFileHeader0_T);
		numberOfChannels = nDataByte / numberOfFrames / sizeof(int16_t);

		// allocate mxStructMatrix for v0 Header
		//plhs[outputIdx] = mxCreateStructMatrix(1, 1, nField0, FieldName0);
		//outputIdx++;

		break;
	case 1:
		fread(&dasHeader1, sizeof(DASFileHeader1_T), 1, fptr);

		getHeaderData(&dasHeader1, headerVersion, &numberOfFrames, &numberOfChannels,
			&frameCapacity, &frameOrientation, &frameDataType, &frameOffset,
			&qualityOrientation, &qualityDataType, &qualityOffset, &qualityBlockSize);

		// allocate mxStructMatrix for v1 Header
		//plhs[outputIdx] = mxCreateStructMatrix(1, 1, nField1, FieldName1);
		//outputIdx++;
		break;
	case 2:
		fread(&dasHeader2, sizeof(DASFileHeader2_T), 1, fptr);

		getHeaderData(&dasHeader2, headerVersion, &numberOfFrames, &numberOfChannels,
			&frameCapacity, &frameOrientation, &frameDataType, &frameOffset,
			&qualityOrientation, &qualityDataType, &qualityOffset, &qualityBlockSize);

		// allocate mxStructMatrix for v2 Header
		//plhs[outputIdx] = mxCreateStructMatrix(1, 1, nField2, FieldName2);
		//outputIdx++;
		break;
	case 3:
		fread(&dasHeader3, sizeof(DASFileHeader3_T), 1, fptr);

		getHeaderData(&dasHeader3, headerVersion, &numberOfFrames, &numberOfChannels,
			&frameCapacity, &frameOrientation, &frameDataType, &frameOffset,
			&qualityOrientation, &qualityDataType, &qualityOffset, &qualityBlockSize);

		// allocate mxStructMatrix for v3 Header
		if (nlhs > 1)
		{
			makeMexHeader3(plhs, &dasHeader3);
			outputIdx++;
		}		
		// add zones
		if ((nlhs == 3 && qualityOffset == 0) || nlhs > 3)
		{
			getMexZoneData(plhs, outputIdx, fptr, dasHeader3.ZonesOffset);
		}
		break;
	case 4:
		fread(&dasHeader4, sizeof(DASFileHeader4_T), 1, fptr);

		getHeaderData(&dasHeader4, headerVersion, &numberOfFrames, &numberOfChannels,
			&frameCapacity, &frameOrientation, &frameDataType, &frameOffset,
			&qualityOrientation, &qualityDataType, &qualityOffset, &qualityBlockSize);

		// allocate mxStructMatrix for v4 Header
		if (nlhs > 1)
		{
			makeMexHeader4(plhs, &dasHeader4);
			outputIdx++;
		}
		// add zones
		if ((nlhs == 3 && qualityOffset == 0) || nlhs > 3)
		{
			getMexZoneData(plhs, outputIdx, fptr, dasHeader4.ZonesOffset);
			outputIdx++;
		}
		// add depth cal, nominal depth, measured depth. TODO: make function calls more user friendly
		if (nlhs > 3)
		{
			getMexDepthCalData(plhs, outputIdx, fptr, dasHeader4.DepthCalibrationOffset);
			outputIdx++;
			getMexNominalDepthData(plhs, outputIdx, fptr, dasHeader4.NominalDepthOffset, numberOfChannels);
			outputIdx++;
			getMexMeasuredDepthData(plhs, outputIdx, fptr, dasHeader4.MeasuredDepthOffset, numberOfChannels);
			outputIdx++;
		}
		break;
	default:
		// e.g. -1
		numberOfFrames = 0;
		numberOfChannels = 0;
		frameCapacity = 0;
		frameOrientation = 0;
		frameDataType = 0;
		frameOffset = 0;
		qualityOrientation = 0;
		qualityDataType = 0;
		qualityOffset = 0;
		qualityBlockSize = 0;
	}

	if (frameOrientation == 1)
	{
		LDA = frameCapacity;
		LDB = numberOfChannels;
	}
	else
	{
		LDA = numberOfChannels;
		LDB = frameCapacity;
	}

	// read main binary data block
	if (frameOffset > 0)
	{
		// allocate memory for main data block
		allocateOutputMxArray(plhs, outputIdx, frameDataType, LDA, LDB);
		fseek(fptr, frameOffset, SEEK_SET);
		readBinaryDataBlock(fptr, mxGetData(plhs[outputIdx]), LDA, LDB, sizeOfDataType(frameDataType));
		outputIdx++;
	}

	// if dPhase & quality, allocate array for quality data
	if (frameDataType == 3 && headerVersion > 0 && qualityOffset > 0 && nlhs > 2)
	{
		allocateOutputMxArray(plhs, outputIdx, qualityDataType, LDA / qualityBlockSize, LDB);
		fseek(fptr, qualityOffset, SEEK_SET);
		readBinaryDataBlock(fptr, mxGetData(plhs[outputIdx]), LDA / qualityBlockSize, LDB, sizeOfDataType(qualityDataType));
	}

	fclose(fptr);

	return;
}