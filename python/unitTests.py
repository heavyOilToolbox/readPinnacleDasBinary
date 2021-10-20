
import pyReadPinnacleDasBinary
import numpy as np

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
    header3Version = pyReadPinnacleDasBinary.checkHeaderVersion(testFileName3)
    header4Version = pyReadPinnacleDasBinary.checkHeaderVersion(testFileName4)
    assert(header3Version == 3)
    assert(header4Version == 4)
    dasHeader3 = np.fromfile(testFileName3, dtype=pyReadPinnacleDasBinary.DASFileHeader_3, count=1)
    dasHeader4 = np.fromfile(testFileName4, dtype=pyReadPinnacleDasBinary.DASFileHeader_4, count=1)

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
    rawJobList = pyReadPinnacleDasBinary.findDPhaseDirectories(testDataRoot4)
    assert(r"Z:\Crestone_3CH_15M_Offset_0907211452\20210907T205823_063908Z\dPhase Data" in rawJobList)
    assert(r"Z:\Crestone_3CH_15M_Offset_0907211452\20210907T213257_211464Z\dPhase Data" in rawJobList)
    assert(r"Z:\Crestone_3CH_15M_Offset_0907211452\20210907T233716_917553Z\dPhase Data" in rawJobList)

def testIntensityDirectorySearch():
    phaseVarianceJobList3 = pyReadPinnacleDasBinary.findPhaseVarianceDirectories(testDataRoot3PV)
    phaseVarianceJobList4 = pyReadPinnacleDasBinary.findPhaseVarianceDirectories(testDataRoot4)
    phasePowerJobList3 = pyReadPinnacleDasBinary.findPhasePowerDirectories(testDataRoot3)
    phasePowerJobList4 = pyReadPinnacleDasBinary.findPhasePowerDirectories(testDataRoot4)
    staticPhaseJobList4 = pyReadPinnacleDasBinary.findStaticPhaseDirectories(testDataRoot4)

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
    fileList3 = pyReadPinnacleDasBinary.dirRecursive(testFileTimeStampDirectory3)
    fileList4 = pyReadPinnacleDasBinary.dirRecursive(testFileTimeStampDirectory4)
    timeStamps3 = pyReadPinnacleDasBinary.getFileTimeStamps(fileList3)
    timeStamps4 = pyReadPinnacleDasBinary.getFileTimeStamps(fileList4)
    for k in range(10):
        print(fileList3[k] + " : " + str(timeStamps3[k]))
    for k in range(10):
        print(fileList4[k] + " : " + str(timeStamps4[k]))

def testReadDasBinary():
    dasHeader3, dasFrameData3 = pyReadPinnacleDasBinary.readDasBinary(testFileName3)
    dasHeader4, dasFrameData4, measuredDepthData4 = pyReadPinnacleDasBinary.readDasBinary(testFileName4)
    #TODO validate returned data
    return None

if __name__ == "__main__":
    if __debug__:
        testHeaderReader()
        testRawDirectorySearch()
        testIntensityDirectorySearch()
        testGetTimeStamps()
        testReadDasBinary()
        print(dir(pyReadPinnacleDasBinary))