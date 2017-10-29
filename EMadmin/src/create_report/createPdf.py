import jinja2
import os

def createPdfFile(acquisitionId):
    from jinja2 import Template
    latex_jinja_env = jinja2.Environment(
        block_start_string = '\BLOCK{',
        block_end_string = '}',
        variable_start_string = '\VAR{',
        variable_end_string = '}',
        comment_start_string = '\#{',
        comment_end_string = '}',
        line_statement_prefix = '%%',
        line_comment_prefix = '%#',
        trim_blocks = True,
        autoescape = False,
        loader = jinja2.FileSystemLoader(os.path.abspath('/'))
    )
    template_file="PP_TEAM_EVAL.tex"
    out_file="temp"
    template = latex_jinja_env.get_template(os.path.realpath(template_file))

    options = {}
    # Header
    options['acquisitionDate'] = '2017\_03\_30'
    options['acquisitionUserName'] = 'pepe'
    options['acquisitionId'] = 99
    options['acquisitionProjName'] = '2017\_03\_30\_pepe\_pipper'
    options['acquisitionSample'] = 'pipper'
    options['acquisitionBackupPath'] = '/media/usb0'
    options['acquisitionShiftLength'] = 3

    # Microscope
    options['microscopeName'] = 'Talos'
    options['microscopeModel'] = 'Talos Artica'
    options['microscopeDetector'] = 'Falcon III'
    options['acquisitiondetectorPixelSize'] = 14
    options['acquisitionVoltage'] = 200
    options['microscopeCs'] = 2.7

    # Acquisition Params
    options['acquisitionNominalMagnification'] = 70000
    options['acquisitionSamplingRate'] = 1.34
    options['acquisitionSpotlSize'] = 2
    options['aquisitionIlluminatedArea'] = 1.68

    # Dose & Fractions
    options['acquisitionDosePerFraction'] = 2
    options['acquisitionTotalExptime'] = 15
    options['acquisitionNumFrames'] = 27
    options['acquisitionFramesPerFrac'] = 3

    # EPU parameters
    options['acquisitionNominalDefocusRange'] = '1.1 2.2 3.3'
    options['acquisitionDefocusDistance'] = 5
    options['acquisitionDriftMeassurement'] = 3
    options['acquisitionDelayAfterStageShift'] = 4
    options['acquisitionDelayAfterImageShift'] = 5
    options['acquisitionMaxImageShift'] = 6
    options['acquisitionExposureHole'] = 3

    # Apertures
    options['acquisitionC2'] = 3
    options['acquisitionO1'] = 4
    options['acquisitionPhP'] = 5

    renderer_template = template.render(**options)

    #if not os.path.exists(build_d):  # create the build directory if not existing
    #    os.makedirs(build_d)

    with open(out_file+".tex", "w") as f:  # saves tex_code to outpout file
        f.write(renderer_template)

    os.system('pdflatex -output-directory {} {}'.format(".", os.path.realpath(out_file + '.tex')))

    #shutil.copy2(out_file+".pdf", os.path.dirname(os.path.realpath(in_file)))