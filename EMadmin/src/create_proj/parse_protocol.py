import os
from django.conf import settings

def parse_ProtImportMovies(protocol, acquisition2):
    acquisition = acquisition2.acquisition
    # get root directory
    dataPath = acquisition.microscope.dataFolder
    projname = acquisition.projname
    projectPath = os.path.join(dataPath, projname)

    if settings.CAMARA != 'Falcon IV':
        protocol['filesPath'] = projectPath + \
                                        '/GRID_??/DATA/Images-Disc1/GridSquare_*/DATA/'
    else:
        protocol['filesPath'] = projectPath + '_DATA_1/Images-Disc1/GridSquare_*/Data/'
        protocol['gainFile'] = projectPath + '_DATA_1/*EER_GainReference.gain'
    protocol['voltage'] = acquisition.voltage
    protocol["sphericalAberration"] = acquisition.microscope.cs
    protocol["magnification"] = acquisition2.nominal_magnification
    protocol["samplingRate"] = acquisition2.sampling_rate
    protocol["dosePerFrame"] = acquisition2.dose_per_fraction

def parse_ProtImportMicrographs(protocol, acquisition2):
    acquisition = acquisition2.acquisition
    # get root directory
    dataPath = acquisition.microscope.dataFolder
    projname = acquisition.projname
    alignedMoviesPath = os.path.join(dataPath, 'exportData', 'Athena_Exported_Datasets', projname + '_1')
    protocol['filesPath'] = alignedMoviesPath + '_*/*/'
    protocol['voltage'] = acquisition.voltage
    protocol["sphericalAberration"] = acquisition.microscope.cs
    protocol["magnification"] = acquisition2.nominal_magnification
    protocol["samplingRate"] = acquisition2.sampling_rate
    protocol["dosePerFrame"] = acquisition2.dose_per_fraction

def parse_ProtMonitorSummary(protocol, acquisition2=None):
    protocol["emailFrom"] = settings.EMAILFROM
    protocol["emailTo"] = settings.EMAILTO
    protocol["smtp"] = settings.SMTP
    protocol["publishCmd"] = settings.PUBLISHCMD

def parse_protocol(protocol, acquisition2):
    key = protocol["object.className"]
    if key=="ProtImportMovies":
        parse_ProtImportMovies(protocol, acquisition2)
    elif key=="ProtMotionCorr":
        pass
    elif key=="ProtCTFFind":
        pass
    elif key=="ProtMonitorSummary":
        parse_ProtMonitorSummary(protocol, acquisition2)
    elif key=="ProtImportMicrographs":
        if settings.CAMARA == 'Falcon IV':
            parse_ProtImportMicrographs(protocol, acquisition2)
