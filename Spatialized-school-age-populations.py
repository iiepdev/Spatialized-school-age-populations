"""
Model exported as python.
Name : Sprague multipliers
Group : 
With QGIS : 31802


This publication is available in Open Access under the Attribution-ShareAlike 3.0 IGO (CC-BY-SA 3.0 IGO) licence (http://creativecommons.org/licenses/by-sa/3.0/igo/). By using the content of this publication, the users accept to be bound by the terms of use of the UNESCO Open Access Repository (http://www.unesco.org/open-access/terms-use-ccbysa-en). The present licence applies exclusively to the original contents of the IIEP Education Policy Toolbox.

This tool was helpful? Let us know how you used it, and suggest improvements by contacting us development@iiep.unesco.org
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterFile
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterString
from qgis.core import QgsProcessingParameterNumber
from qgis.core import QgsProcessingParameterBoolean
from qgis.core import QgsProcessingParameterFeatureSink
from qgis.core import QgsProcessingParameterDefinition
from qgis.core import QgsExpression
import processing


class SpragueMultipliers(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFile('Foldercontainingtherasterfiles', 'Folder containing the raster files', behavior=QgsProcessingParameterFile.Folder, fileFilter='All files (*.*)', defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('Administrativeboundaries', 'Administrative boundaries', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        # 3-letter code required
        self.addParameter(QgsProcessingParameterString('ISOcountrycode', 'ISO country code', multiLine=False, defaultValue='COL'))
        self.addParameter(QgsProcessingParameterNumber('Year', 'Year', type=QgsProcessingParameterNumber.Integer, minValue=1900, maxValue=2100, defaultValue=2020))
        self.addParameter(QgsProcessingParameterBoolean('Useunconstrainedpopulationestimates', 'Use constrained population estimates', defaultValue=False))
        self.addParameter(QgsProcessingParameterBoolean('UseUNadjustedconstrainedestimates', 'Use UN adjusted constrained estimates', optional=True, defaultValue=False))
        self.addParameter(QgsProcessingParameterBoolean('Createcustomschoolagegroups', 'Create custom school age groups', defaultValue=False))
        param = QgsProcessingParameterNumber('Preprimarystartingage', 'Pre-primary starting age', optional=True, type=QgsProcessingParameterNumber.Integer, minValue=2, maxValue=6, defaultValue=None)
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        param = QgsProcessingParameterNumber('Preprimaryduration', 'Pre-primary duration', optional=True, type=QgsProcessingParameterNumber.Integer, minValue=1, maxValue=4, defaultValue=None)
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        param = QgsProcessingParameterNumber('Primarystartingage', 'Primary starting age', optional=True, type=QgsProcessingParameterNumber.Integer, minValue=5, maxValue=7, defaultValue=None)
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        param = QgsProcessingParameterNumber('Primaryduration', 'Primary duration', optional=True, type=QgsProcessingParameterNumber.Integer, minValue=4, maxValue=8, defaultValue=None)
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        param = QgsProcessingParameterBoolean('SystemdividedinLowerandUppersecondary', 'System divided in Lower and Upper secondary', optional=True, defaultValue=True)
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        param = QgsProcessingParameterNumber('Lowersecondarystartingage', 'Lower secondary starting age', optional=True, type=QgsProcessingParameterNumber.Integer, minValue=10, maxValue=14, defaultValue=None)
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        param = QgsProcessingParameterNumber('Lowersecondaryduration', 'Lower secondary duration', optional=True, type=QgsProcessingParameterNumber.Integer, minValue=1, maxValue=8, defaultValue=None)
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        param = QgsProcessingParameterNumber('Uppersecondarystartingage', 'Upper secondary starting age', optional=True, type=QgsProcessingParameterNumber.Integer, minValue=13, maxValue=18, defaultValue=None)
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        param = QgsProcessingParameterNumber('Uppersecondaryduration', 'Upper secondary duration', optional=True, type=QgsProcessingParameterNumber.Integer, minValue=1, maxValue=8, defaultValue=None)
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        param = QgsProcessingParameterNumber('Secondarystartingage', 'Secondary starting age', optional=True, type=QgsProcessingParameterNumber.Integer, minValue=10, maxValue=14, defaultValue=None)
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        param = QgsProcessingParameterNumber('Secondaryduration', 'Secondary duration', optional=True, type=QgsProcessingParameterNumber.Integer, minValue=1, maxValue=8, defaultValue=None)
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        self.addParameter(QgsProcessingParameterFeatureSink('Results', 'Results', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('ResultsWithLowerAndUpperSecondary', 'Results with Lower and Upper secondary', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('ResultsWithSecondary', 'Results with Secondary', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterBoolean('VERBOSE_LOG', 'Verbose logging', optional=True, defaultValue=False))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(45, model_feedback)
        results = {}
        outputs = {}

        # Distinguish between Lower and Upper secondary
        alg_params = {
        }
        outputs['DistinguishBetweenLowerAndUpperSecondary'] = processing.run('native:condition', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Female 0 to 1
        alg_params = {
            'COLUMN_PREFIX': 'F_0_',
            'INPUT_RASTER': QgsExpression('CASE\r\nWHEN NOT @Useunconstrainedpopulationestimates THEN @Foldercontainingtherasterfiles || \'/\' ||  lower(to_string( @ISOcountrycode ))|| \'_f_0_\' ||to_string( @Year ) ||\'.tif\'\r\nWHEN  @Useunconstrainedpopulationestimates AND NOT  @UseUNadjustedconstrainedestimates  THEN @Foldercontainingtherasterfiles || \'/\' ||  lower(to_string( @ISOcountrycode ))|| \'_f_0_\' ||to_string( @Year ) ||\'_constrained.tif\'\r\nELSE \r\n@Foldercontainingtherasterfiles || \'/\' ||  lower(to_string( @ISOcountrycode ))|| \'_f_0_\' ||to_string( @Year ) ||\'_constrained_UNadj.tif\'\r\nEND').evaluate(),
            'INPUT_VECTOR': parameters['Administrativeboundaries'],
            'RASTER_BAND': 1,
            'STATISTICS': [1]
        }
        outputs['Female0To1'] = processing.run('native:zonalstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Female 1 to 4
        alg_params = {
            'COLUMN_PREFIX': 'F_1_',
            'INPUT_RASTER': QgsExpression('CASE\r\nWHEN NOT @Useunconstrainedpopulationestimates THEN @Foldercontainingtherasterfiles || \'/\' ||  lower(to_string( @ISOcountrycode ))|| \'_f_1_\' ||to_string( @Year ) ||\'.tif\'\r\nWHEN  @Useunconstrainedpopulationestimates AND NOT  @UseUNadjustedconstrainedestimates  THEN @Foldercontainingtherasterfiles || \'/\' ||  lower(to_string( @ISOcountrycode ))|| \'_f_1_\' ||to_string( @Year ) ||\'_constrained.tif\'\r\nELSE \r\n@Foldercontainingtherasterfiles || \'/\' ||  lower(to_string( @ISOcountrycode ))|| \'_f_1_\' ||to_string( @Year ) ||\'_constrained_UNadj.tif\'\r\nEND').evaluate(),
            'INPUT_VECTOR': parameters['Administrativeboundaries'],
            'RASTER_BAND': 1,
            'STATISTICS': [1]
        }
        outputs['Female1To4'] = processing.run('native:zonalstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Female 5 to 9
        alg_params = {
            'COLUMN_PREFIX': 'F_5_',
            'INPUT_RASTER': QgsExpression('CASE\r\nWHEN NOT @Useunconstrainedpopulationestimates THEN @Foldercontainingtherasterfiles || \'/\' ||  lower(to_string( @ISOcountrycode ))|| \'_f_5_\' ||to_string( @Year ) ||\'.tif\'\r\nWHEN  @Useunconstrainedpopulationestimates AND NOT  @UseUNadjustedconstrainedestimates  THEN @Foldercontainingtherasterfiles || \'/\' ||  lower(to_string( @ISOcountrycode ))|| \'_f_5_\' ||to_string( @Year ) ||\'_constrained.tif\'\r\nELSE \r\n@Foldercontainingtherasterfiles || \'/\' ||  lower(to_string( @ISOcountrycode ))|| \'_f_5_\' ||to_string( @Year ) ||\'_constrained_UNadj.tif\'\r\nEND').evaluate(),
            'INPUT_VECTOR': parameters['Administrativeboundaries'],
            'RASTER_BAND': 1,
            'STATISTICS': [1]
        }
        outputs['Female5To9'] = processing.run('native:zonalstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # Create custom age groups
        alg_params = {
        }
        outputs['CreateCustomAgeGroups'] = processing.run('native:condition', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # Female 10 to 14
        alg_params = {
            'COLUMN_PREFIX': 'F_10_',
            'INPUT_RASTER': QgsExpression('CASE\r\nWHEN NOT @Useunconstrainedpopulationestimates THEN @Foldercontainingtherasterfiles || \'/\' ||  lower(to_string( @ISOcountrycode ))|| \'_f_10_\' ||to_string( @Year ) ||\'.tif\'\r\nWHEN  @Useunconstrainedpopulationestimates AND NOT  @UseUNadjustedconstrainedestimates  THEN @Foldercontainingtherasterfiles || \'/\' ||  lower(to_string( @ISOcountrycode ))|| \'_f_10_\' ||to_string( @Year ) ||\'_constrained.tif\'\r\nELSE \r\n@Foldercontainingtherasterfiles || \'/\' ||  lower(to_string( @ISOcountrycode ))|| \'_f_10_\' ||to_string( @Year ) ||\'_constrained_UNadj.tif\'\r\nEND').evaluate(),
            'INPUT_VECTOR': parameters['Administrativeboundaries'],
            'RASTER_BAND': 1,
            'STATISTICS': [1]
        }
        outputs['Female10To14'] = processing.run('native:zonalstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        # Female 15 to 19
        alg_params = {
            'COLUMN_PREFIX': 'F_15_',
            'INPUT_RASTER': QgsExpression('CASE\r\nWHEN NOT @Useunconstrainedpopulationestimates THEN @Foldercontainingtherasterfiles || \'/\' ||  lower(to_string( @ISOcountrycode ))|| \'_f_15_\' ||to_string( @Year ) ||\'.tif\'\r\nWHEN  @Useunconstrainedpopulationestimates AND NOT  @UseUNadjustedconstrainedestimates  THEN @Foldercontainingtherasterfiles || \'/\' ||  lower(to_string( @ISOcountrycode ))|| \'_f_15_\' ||to_string( @Year ) ||\'_constrained.tif\'\r\nELSE \r\n@Foldercontainingtherasterfiles || \'/\' ||  lower(to_string( @ISOcountrycode ))|| \'_f_15_\' ||to_string( @Year ) ||\'_constrained_UNadj.tif\'\r\nEND').evaluate(),
            'INPUT_VECTOR': parameters['Administrativeboundaries'],
            'RASTER_BAND': 1,
            'STATISTICS': [1]
        }
        outputs['Female15To19'] = processing.run('native:zonalstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(7)
        if feedback.isCanceled():
            return {}

        # Female 20 to 24
        alg_params = {
            'COLUMN_PREFIX': 'F_20_',
            'INPUT_RASTER': QgsExpression('CASE\r\nWHEN NOT @Useunconstrainedpopulationestimates THEN @Foldercontainingtherasterfiles || \'/\' ||  lower(to_string( @ISOcountrycode ))|| \'_f_20_\' ||to_string( @Year ) ||\'.tif\'\r\nWHEN  @Useunconstrainedpopulationestimates AND NOT  @UseUNadjustedconstrainedestimates  THEN @Foldercontainingtherasterfiles || \'/\' ||  lower(to_string( @ISOcountrycode ))|| \'_f_20_\' ||to_string( @Year ) ||\'_constrained.tif\'\r\nELSE \r\n@Foldercontainingtherasterfiles || \'/\' ||  lower(to_string( @ISOcountrycode ))|| \'_f_20_\' ||to_string( @Year ) ||\'_constrained_UNadj.tif\'\r\nEND').evaluate(),
            'INPUT_VECTOR': parameters['Administrativeboundaries'],
            'RASTER_BAND': 1,
            'STATISTICS': [1]
        }
        outputs['Female20To24'] = processing.run('native:zonalstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(8)
        if feedback.isCanceled():
            return {}

        # Female 25 to 29
        alg_params = {
            'COLUMN_PREFIX': 'F_25_',
            'INPUT_RASTER': QgsExpression('CASE\r\nWHEN NOT @Useunconstrainedpopulationestimates THEN @Foldercontainingtherasterfiles || \'/\' ||  lower(to_string( @ISOcountrycode ))|| \'_f_25_\' ||to_string( @Year ) ||\'.tif\'\r\nWHEN  @Useunconstrainedpopulationestimates AND NOT  @UseUNadjustedconstrainedestimates  THEN @Foldercontainingtherasterfiles || \'/\' ||  lower(to_string( @ISOcountrycode ))|| \'_f_25_\' ||to_string( @Year ) ||\'_constrained.tif\'\r\nELSE \r\n@Foldercontainingtherasterfiles || \'/\' ||  lower(to_string( @ISOcountrycode ))|| \'_f_25_\' ||to_string( @Year ) ||\'_constrained_UNadj.tif\'\r\nEND').evaluate(),
            'INPUT_VECTOR': parameters['Administrativeboundaries'],
            'RASTER_BAND': 1,
            'STATISTICS': [1]
        }
        outputs['Female25To29'] = processing.run('native:zonalstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(9)
        if feedback.isCanceled():
            return {}

        # Female 30 to 34
        alg_params = {
            'COLUMN_PREFIX': 'F_30_',
            'INPUT_RASTER': QgsExpression('CASE\r\nWHEN NOT @Useunconstrainedpopulationestimates THEN @Foldercontainingtherasterfiles || \'/\' ||  lower(to_string( @ISOcountrycode ))|| \'_f_30_\' ||to_string( @Year ) ||\'.tif\'\r\nWHEN  @Useunconstrainedpopulationestimates AND NOT  @UseUNadjustedconstrainedestimates  THEN @Foldercontainingtherasterfiles || \'/\' ||  lower(to_string( @ISOcountrycode ))|| \'_f_30_\' ||to_string( @Year ) ||\'_constrained.tif\'\r\nELSE \r\n@Foldercontainingtherasterfiles || \'/\' ||  lower(to_string( @ISOcountrycode ))|| \'_f_30_\' ||to_string( @Year ) ||\'_constrained_UNadj.tif\'\r\nEND').evaluate(),
            'INPUT_VECTOR': parameters['Administrativeboundaries'],
            'RASTER_BAND': 1,
            'STATISTICS': [1]
        }
        outputs['Female30To34'] = processing.run('native:zonalstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(10)
        if feedback.isCanceled():
            return {}

        # Female 35 to 39
        alg_params = {
            'COLUMN_PREFIX': 'F_35_',
            'INPUT_RASTER': QgsExpression('CASE\r\nWHEN NOT @Useunconstrainedpopulationestimates THEN @Foldercontainingtherasterfiles || \'/\' ||  lower(to_string( @ISOcountrycode ))|| \'_f_35_\' ||to_string( @Year ) ||\'.tif\'\r\nWHEN  @Useunconstrainedpopulationestimates AND NOT  @UseUNadjustedconstrainedestimates  THEN @Foldercontainingtherasterfiles || \'/\' ||  lower(to_string( @ISOcountrycode ))|| \'_f_35_\' ||to_string( @Year ) ||\'_constrained.tif\'\r\nELSE \r\n@Foldercontainingtherasterfiles || \'/\' ||  lower(to_string( @ISOcountrycode ))|| \'_f_35_\' ||to_string( @Year ) ||\'_constrained_UNadj.tif\'\r\nEND').evaluate(),
            'INPUT_VECTOR': parameters['Administrativeboundaries'],
            'RASTER_BAND': 1,
            'STATISTICS': [1]
        }
        outputs['Female35To39'] = processing.run('native:zonalstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(11)
        if feedback.isCanceled():
            return {}

        # Male 0 to 1
        alg_params = {
            'COLUMN_PREFIX': 'M_0_',
            'INPUT_RASTER': QgsExpression('CASE\r\nWHEN NOT @Useunconstrainedpopulationestimates THEN @Foldercontainingtherasterfiles || \'/\' ||  lower(to_string( @ISOcountrycode ))|| \'_m_0_\' ||to_string( @Year ) ||\'.tif\'\r\nWHEN  @Useunconstrainedpopulationestimates AND NOT  @UseUNadjustedconstrainedestimates  THEN @Foldercontainingtherasterfiles || \'/\' ||  lower(to_string( @ISOcountrycode ))|| \'_m_0_\' ||to_string( @Year ) ||\'_constrained.tif\'\r\nELSE \r\n@Foldercontainingtherasterfiles || \'/\' ||  lower(to_string( @ISOcountrycode ))|| \'_m_0_\' ||to_string( @Year ) ||\'_constrained_UNadj.tif\'\r\nEND').evaluate(),
            'INPUT_VECTOR': parameters['Administrativeboundaries'],
            'RASTER_BAND': 1,
            'STATISTICS': [1]
        }
        outputs['Male0To1'] = processing.run('native:zonalstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(12)
        if feedback.isCanceled():
            return {}

        # Male 1 to 4
        alg_params = {
            'COLUMN_PREFIX': 'M_1_',
            'INPUT_RASTER': QgsExpression('CASE\r\nWHEN NOT @Useunconstrainedpopulationestimates THEN @Foldercontainingtherasterfiles || \'/\' ||  lower(to_string( @ISOcountrycode ))|| \'_m_1_\' ||to_string( @Year ) ||\'.tif\'\r\nWHEN  @Useunconstrainedpopulationestimates AND NOT  @UseUNadjustedconstrainedestimates  THEN @Foldercontainingtherasterfiles || \'/\' ||  lower(to_string( @ISOcountrycode ))|| \'_m_1_\' ||to_string( @Year ) ||\'_constrained.tif\'\r\nELSE \r\n@Foldercontainingtherasterfiles || \'/\' ||  lower(to_string( @ISOcountrycode ))|| \'_m_1_\' ||to_string( @Year ) ||\'_constrained_UNadj.tif\'\r\nEND').evaluate(),
            'INPUT_VECTOR': parameters['Administrativeboundaries'],
            'RASTER_BAND': 1,
            'STATISTICS': [1]
        }
        outputs['Male1To4'] = processing.run('native:zonalstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(13)
        if feedback.isCanceled():
            return {}

        # Male 5 to 9
        alg_params = {
            'COLUMN_PREFIX': 'M_5_',
            'INPUT_RASTER': QgsExpression('CASE\r\nWHEN NOT @Useunconstrainedpopulationestimates THEN @Foldercontainingtherasterfiles || \'/\' ||  lower(to_string( @ISOcountrycode ))|| \'_m_5_\' ||to_string( @Year ) ||\'.tif\'\r\nWHEN  @Useunconstrainedpopulationestimates AND NOT  @UseUNadjustedconstrainedestimates  THEN @Foldercontainingtherasterfiles || \'/\' ||  lower(to_string( @ISOcountrycode ))|| \'_m_5_\' ||to_string( @Year ) ||\'_constrained.tif\'\r\nELSE \r\n@Foldercontainingtherasterfiles || \'/\' ||  lower(to_string( @ISOcountrycode ))|| \'_m_5_\' ||to_string( @Year ) ||\'_constrained_UNadj.tif\'\r\nEND').evaluate(),
            'INPUT_VECTOR': parameters['Administrativeboundaries'],
            'RASTER_BAND': 1,
            'STATISTICS': [1]
        }
        outputs['Male5To9'] = processing.run('native:zonalstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(14)
        if feedback.isCanceled():
            return {}

        # Male 10 to 14
        alg_params = {
            'COLUMN_PREFIX': 'M_10_',
            'INPUT_RASTER': QgsExpression('CASE\r\nWHEN NOT @Useunconstrainedpopulationestimates THEN @Foldercontainingtherasterfiles || \'/\' ||  lower(to_string( @ISOcountrycode ))|| \'_m_10_\' ||to_string( @Year ) ||\'.tif\'\r\nWHEN  @Useunconstrainedpopulationestimates AND NOT  @UseUNadjustedconstrainedestimates  THEN @Foldercontainingtherasterfiles || \'/\' ||  lower(to_string( @ISOcountrycode ))|| \'_m_10_\' ||to_string( @Year ) ||\'_constrained.tif\'\r\nELSE \r\n@Foldercontainingtherasterfiles || \'/\' ||  lower(to_string( @ISOcountrycode ))|| \'_m_10_\' ||to_string( @Year ) ||\'_constrained_UNadj.tif\'\r\nEND').evaluate(),
            'INPUT_VECTOR': parameters['Administrativeboundaries'],
            'RASTER_BAND': 1,
            'STATISTICS': [1]
        }
        outputs['Male10To14'] = processing.run('native:zonalstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(15)
        if feedback.isCanceled():
            return {}

        # Male 15 to 19
        alg_params = {
            'COLUMN_PREFIX': 'M_15_',
            'INPUT_RASTER': QgsExpression('CASE\r\nWHEN NOT @Useunconstrainedpopulationestimates THEN @Foldercontainingtherasterfiles || \'/\' ||  lower(to_string( @ISOcountrycode ))|| \'_m_15_\' ||to_string( @Year ) ||\'.tif\'\r\nWHEN  @Useunconstrainedpopulationestimates AND NOT  @UseUNadjustedconstrainedestimates  THEN @Foldercontainingtherasterfiles || \'/\' ||  lower(to_string( @ISOcountrycode ))|| \'_m_15_\' ||to_string( @Year ) ||\'_constrained.tif\'\r\nELSE \r\n@Foldercontainingtherasterfiles || \'/\' ||  lower(to_string( @ISOcountrycode ))|| \'_m_15_\' ||to_string( @Year ) ||\'_constrained_UNadj.tif\'\r\nEND').evaluate(),
            'INPUT_VECTOR': parameters['Administrativeboundaries'],
            'RASTER_BAND': 1,
            'STATISTICS': [1]
        }
        outputs['Male15To19'] = processing.run('native:zonalstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(16)
        if feedback.isCanceled():
            return {}

        # Male 20 to 24
        alg_params = {
            'COLUMN_PREFIX': 'M_20_',
            'INPUT_RASTER': QgsExpression('CASE\r\nWHEN NOT @Useunconstrainedpopulationestimates THEN @Foldercontainingtherasterfiles || \'/\' ||  lower(to_string( @ISOcountrycode ))|| \'_m_20_\' ||to_string( @Year ) ||\'.tif\'\r\nWHEN  @Useunconstrainedpopulationestimates AND NOT  @UseUNadjustedconstrainedestimates  THEN @Foldercontainingtherasterfiles || \'/\' ||  lower(to_string( @ISOcountrycode ))|| \'_m_20_\' ||to_string( @Year ) ||\'_constrained.tif\'\r\nELSE \r\n@Foldercontainingtherasterfiles || \'/\' ||  lower(to_string( @ISOcountrycode ))|| \'_m_20_\' ||to_string( @Year ) ||\'_constrained_UNadj.tif\'\r\nEND').evaluate(),
            'INPUT_VECTOR': parameters['Administrativeboundaries'],
            'RASTER_BAND': 1,
            'STATISTICS': [1]
        }
        outputs['Male20To24'] = processing.run('native:zonalstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(17)
        if feedback.isCanceled():
            return {}

        # Male 25 to 29
        alg_params = {
            'COLUMN_PREFIX': 'M_25_',
            'INPUT_RASTER': QgsExpression('CASE\r\nWHEN NOT @Useunconstrainedpopulationestimates THEN @Foldercontainingtherasterfiles || \'/\' ||  lower(to_string( @ISOcountrycode ))|| \'_m_25_\' ||to_string( @Year ) ||\'.tif\'\r\nWHEN  @Useunconstrainedpopulationestimates AND NOT  @UseUNadjustedconstrainedestimates  THEN @Foldercontainingtherasterfiles || \'/\' ||  lower(to_string( @ISOcountrycode ))|| \'_m_25_\' ||to_string( @Year ) ||\'_constrained.tif\'\r\nELSE \r\n@Foldercontainingtherasterfiles || \'/\' ||  lower(to_string( @ISOcountrycode ))|| \'_m_25_\' ||to_string( @Year ) ||\'_constrained_UNadj.tif\'\r\nEND').evaluate(),
            'INPUT_VECTOR': parameters['Administrativeboundaries'],
            'RASTER_BAND': 1,
            'STATISTICS': [1]
        }
        outputs['Male25To29'] = processing.run('native:zonalstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(18)
        if feedback.isCanceled():
            return {}

        # Male 30 to 34
        alg_params = {
            'COLUMN_PREFIX': 'M_30_',
            'INPUT_RASTER': QgsExpression('CASE\r\nWHEN NOT @Useunconstrainedpopulationestimates THEN @Foldercontainingtherasterfiles || \'/\' ||  lower(to_string( @ISOcountrycode ))|| \'_m_30_\' ||to_string( @Year ) ||\'.tif\'\r\nWHEN  @Useunconstrainedpopulationestimates AND NOT  @UseUNadjustedconstrainedestimates  THEN @Foldercontainingtherasterfiles || \'/\' ||  lower(to_string( @ISOcountrycode ))|| \'_m_30_\' ||to_string( @Year ) ||\'_constrained.tif\'\r\nELSE \r\n@Foldercontainingtherasterfiles || \'/\' ||  lower(to_string( @ISOcountrycode ))|| \'_m_30_\' ||to_string( @Year ) ||\'_constrained_UNadj.tif\'\r\nEND').evaluate(),
            'INPUT_VECTOR': parameters['Administrativeboundaries'],
            'RASTER_BAND': 1,
            'STATISTICS': [1]
        }
        outputs['Male30To34'] = processing.run('native:zonalstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(19)
        if feedback.isCanceled():
            return {}

        # Male 35 to 39
        alg_params = {
            'COLUMN_PREFIX': 'M_35_',
            'INPUT_RASTER': QgsExpression('CASE\r\nWHEN NOT @Useunconstrainedpopulationestimates THEN @Foldercontainingtherasterfiles || \'/\' ||  lower(to_string( @ISOcountrycode ))|| \'_m_35_\' ||to_string( @Year ) ||\'.tif\'\r\nWHEN  @Useunconstrainedpopulationestimates AND NOT  @UseUNadjustedconstrainedestimates  THEN @Foldercontainingtherasterfiles || \'/\' ||  lower(to_string( @ISOcountrycode ))|| \'_m_35_\' ||to_string( @Year ) ||\'_constrained.tif\'\r\nELSE \r\n@Foldercontainingtherasterfiles || \'/\' ||  lower(to_string( @ISOcountrycode ))|| \'_m_35_\' ||to_string( @Year ) ||\'_constrained_UNadj.tif\'\r\nEND').evaluate(),
            'INPUT_VECTOR': parameters['Administrativeboundaries'],
            'RASTER_BAND': 1,
            'STATISTICS': [1]
        }
        outputs['Male35To39'] = processing.run('native:zonalstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(20)
        if feedback.isCanceled():
            return {}

        # Creating the 0 to 4 age groups
        alg_params = {
            'FIELDS_MAPPING': [{'expression': '\"F_5_sum\"','length': 0,'name': 'F_5_sum','precision': 0,'type': 6},{'expression': '\"F_10_sum\"','length': 0,'name': 'F_10_sum','precision': 0,'type': 6},{'expression': '\"F_15_sum\"','length': 0,'name': 'F_15_sum','precision': 0,'type': 6},{'expression': '\"F_20_sum\"','length': 0,'name': 'F_20_sum','precision': 0,'type': 6},{'expression': '\"F_25_sum\"','length': 0,'name': 'F_25_sum','precision': 0,'type': 6},{'expression': '\"F_30_sum\"','length': 0,'name': 'F_30_sum','precision': 0,'type': 6},{'expression': '\"F_35_sum\"','length': 0,'name': 'F_35_sum','precision': 0,'type': 6},{'expression': 'M_5_sum','length': 0,'name': 'M_5_sum','precision': 0,'type': 6},{'expression': 'M_10_sum','length': 0,'name': 'M_10_sum','precision': 0,'type': 6},{'expression': 'M_15_sum','length': 0,'name': 'M_15_sum','precision': 0,'type': 6},{'expression': 'M_20_sum','length': 0,'name': 'M_20_sum','precision': 0,'type': 6},{'expression': 'M_25_sum','length': 0,'name': 'M_25_sum','precision': 0,'type': 6},{'expression': 'M_30_sum','length': 0,'name': 'M_30_sum','precision': 0,'type': 6},{'expression': 'M_35_sum','length': 0,'name': 'M_35_sum','precision': 0,'type': 6},{'expression': '\"F_0_sum\" + \"F_1_sum\"','length': 0,'name': 'F_0_sum','precision': 0,'type': 6},{'expression': '\"M_0_sum\" + \"M_1_sum\"','length': 0,'name': 'M_0_sum','precision': 0,'type': 6}],
            'INPUT': parameters['Administrativeboundaries'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CreatingThe0To4AgeGroups'] = processing.run('native:refactorfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(21)
        if feedback.isCanceled():
            return {}

        # Calculating single years of age - Section 1
        alg_params = {
            'FIELDS_MAPPING': [{'expression': '$area','length': 0,'name': 'Area','precision': 0,'type': 6},{'expression': ' 0.3616*\"M_0_sum\" - 0.2768*\"M_5_sum\" + 0.1488*\"M_10_sum\" - 0.0336*\"M_15_sum\"  ','length': 0,'name': 'Y_M_0','precision': 0,'type': 6},{'expression': ' 0.2640*\"M_0_sum\" - 0.0960*\"M_5_sum\" + 0.0400*\"M_10_sum\" - 0.0080*\"M_15_sum\"  ','length': 0,'name': 'Y_M_1','precision': 0,'type': 6},{'expression': ' 0.1840*\"M_0_sum\" + 0.0400*\"M_5_sum\" - 0.0320*\"M_10_sum\" + 0.0080*\"M_15_sum\" ','length': 0,'name': 'Y_M_2','precision': 0,'type': 6},{'expression': ' 0.1200*\"M_0_sum\" + 0.1360*\"M_5_sum\" - 0.0720*\"M_10_sum\" + 0.0160*\"M_15_sum\"  ','length': 0,'name': 'Y_M_3','precision': 0,'type': 6},{'expression': ' 0.0336*\"M_0_sum\" + 0.2272*\"M_5_sum\" - 0.0752*\"M_10_sum\" + 0.0144*\"M_15_sum\" ','length': 0,'name': 'Y_M_5','precision': 0,'type': 6},{'expression': ' 0.0080*\"M_0_sum\" + 0.2320*\"M_5_sum\" - 0.0480*\"M_10_sum\" + 0.0080*\"M_15_sum\" ','length': 0,'name': 'Y_M_6','precision': 0,'type': 6},{'expression': ' -0.0080*\"M_0_sum\" + 0.2160*\"M_5_sum\" - 0.0080*\"M_10_sum\" + 0.0000*\"M_15_sum\"','length': 0,'name': 'Y_M_7','precision': 0,'type': 6},{'expression': ' -0.0160*\"M_0_sum\" + 0.1840*\"M_5_sum\" + 0.0400*\"M_10_sum\" - 0.0080*\"M_15_sum\"','length': 0,'name': 'Y_M_8','precision': 0,'type': 6},{'expression': ' -0.0128*\"M_0_sum\" + 0.0848*\"M_5_sum\" + 0.1504*\"M_10_sum\" - 0.0240*\"M_15_sum\" + 0.0016*\"M_20_sum\"','length': 0,'name': 'Y_M_10','precision': 0,'type': 6},{'expression': ' -0.0016*\"M_0_sum\" + 0.0144*\"M_5_sum\" + 0.2224*\"M_10_sum\" - 0.0416*\"M_15_sum\" + 0.0064*\"M_20_sum\"','length': 0,'name': 'Y_M_11','precision': 0,'type': 6},{'expression': ' 0.0064*\"M_0_sum\" - 0.0336*\"M_5_sum\" + 0.2544*\"M_10_sum\" - 0.0336*\"M_15_sum\" + 0.0064*\"M_20_sum\"','length': 0,'name': 'Y_M_12','precision': 0,'type': 6},{'expression': ' 0.0064*\"M_0_sum\" - 0.0416*\"M_5_sum\" + 0.2224*\"M_10_sum\" + 0.0144*\"M_15_sum\" - 0.0016*\"M_20_sum\"','length': 0,'name': 'Y_M_13','precision': 0,'type': 6},{'expression': ' -0.0128*\"M_5_sum\" + 0.0848*\"M_10_sum\" + 0.1504*\"M_15_sum\" - 0.0240*\"M_20_sum\" + 0.0016*\"M_25_sum\"','length': 0,'name': 'Y_M_15','precision': 0,'type': 6},{'expression': ' -0.0016*\"M_5_sum\" + 0.0144*\"M_10_sum\" + 0.2224*\"M_15_sum\" - 0.0416*\"M_20_sum\" + 0.0064*\"M_25_sum\"','length': 0,'name': 'Y_M_16','precision': 0,'type': 6},{'expression': ' 0.0064*\"M_5_sum\" - 0.0336*\"M_10_sum\" + 0.2544*\"M_15_sum\" - 0.0336*\"M_20_sum\" + 0.0064*\"M_25_sum\"','length': 0,'name': 'Y_M_17','precision': 0,'type': 6},{'expression': ' 0.0064*\"M_5_sum\" - 0.0416*\"M_10_sum\" + 0.2224*\"M_15_sum\" + 0.0144*\"M_20_sum\" - 0.0016*\"M_25_sum\"','length': 0,'name': 'Y_M_18','precision': 0,'type': 6},{'expression': ' -0.0128*\"M_10_sum\" + 0.0848*\"M_15_sum\" + 0.1504*\"M_20_sum\" - 0.0240*\"M_25_sum\" + 0.0016*\"M_30_sum\"','length': 0,'name': 'Y_M_20','precision': 0,'type': 6},{'expression': ' -0.0016*\"M_10_sum\" + 0.0144*\"M_15_sum\" + 0.2224*\"M_20_sum\" - 0.0416*\"M_25_sum\" + 0.0064*\"M_30_sum\"','length': 0,'name': 'Y_M_21','precision': 0,'type': 6},{'expression': ' 0.0064*\"M_10_sum\" - 0.0336*\"M_15_sum\" + 0.2544*\"M_20_sum\" - 0.0336*\"M_25_sum\" + 0.0064*\"M_30_sum\"','length': 0,'name': 'Y_M_22','precision': 0,'type': 6},{'expression': ' 0.0064*\"M_10_sum\" - 0.0416*\"M_15_sum\" + 0.2224*\"M_20_sum\" + 0.0144*\"M_25_sum\" - 0.0016*\"M_30_sum\"','length': 0,'name': 'Y_M_23','precision': 0,'type': 6},{'expression': ' -0.0128*\"M_15_sum\" + 0.0848*\"M_20_sum\" + 0.1504*\"M_25_sum\" - 0.0240*\"M_30_sum\" + 0.0016*\"M_35_sum\"','length': 0,'name': 'Y_M_25','precision': 0,'type': 6},{'expression': ' -0.0016*\"M_15_sum\" + 0.0144*\"M_20_sum\" + 0.2224*\"M_25_sum\" - 0.0416*\"M_30_sum\" + 0.0064*\"M_35_sum\"','length': 0,'name': 'Y_M_26','precision': 0,'type': 6},{'expression': ' 0.0064*\"M_15_sum\" - 0.0336*\"M_20_sum\" + 0.2544*\"M_25_sum\" - 0.0336*\"M_30_sum\" + 0.0064*\"M_35_sum\"','length': 0,'name': 'Y_M_27','precision': 0,'type': 6},{'expression': ' 0.0064*\"M_15_sum\" - 0.0416*\"M_20_sum\" + 0.2224*\"M_25_sum\" + 0.0144*\"M_30_sum\" - 0.0016*\"M_35_sum\"','length': 0,'name': 'Y_M_28','precision': 0,'type': 6},{'expression': ' 0.3616*\"F_0_sum\" - 0.2768*\"F_5_sum\" + 0.1488*\"F_10_sum\" - 0.0336*\"F_15_sum\" ','length': 0,'name': 'Y_F_0','precision': 0,'type': 6},{'expression': ' 0.2640*\"F_0_sum\" - 0.0960*\"F_5_sum\" + 0.0400*\"F_10_sum\" - 0.0080*\"F_15_sum\" ','length': 0,'name': 'Y_F_1','precision': 0,'type': 6},{'expression': ' 0.1840*\"F_0_sum\" + 0.0400*\"F_5_sum\" - 0.0320*\"F_10_sum\" + 0.0080*\"F_15_sum\" ','length': 0,'name': 'Y_F_2','precision': 0,'type': 6},{'expression': ' 0.1200*\"F_0_sum\" + 0.1360*\"F_5_sum\" - 0.0720*\"F_10_sum\" + 0.0160*\"F_15_sum\" ','length': 0,'name': 'Y_F_3','precision': 0,'type': 6},{'expression': ' 0.0336*\"F_0_sum\" + 0.2272*\"F_5_sum\" - 0.0752*\"F_10_sum\" + 0.0144*\"F_15_sum\"','length': 0,'name': 'Y_F_5','precision': 0,'type': 6},{'expression': ' 0.0080*\"F_0_sum\" + 0.2320*\"F_5_sum\" - 0.0480*\"F_10_sum\" + 0.0080*\"F_15_sum\" ','length': 0,'name': 'Y_F_6','precision': 0,'type': 6},{'expression': ' -0.0080*\"F_0_sum\" + 0.2160*\"F_5_sum\" - 0.0080*\"F_10_sum\" + 0.0000*\"F_15_sum\"','length': 0,'name': 'Y_F_7','precision': 0,'type': 6},{'expression': ' -0.0160*\"F_0_sum\" + 0.1840*\"F_5_sum\" + 0.0400*\"F_10_sum\" - 0.0080*\"F_15_sum\"','length': 0,'name': 'Y_F_8','precision': 0,'type': 6},{'expression': ' -0.0128*\"F_0_sum\" + 0.0848*\"F_5_sum\" + 0.1504*\"F_10_sum\" - 0.0240*\"F_15_sum\" + 0.0016*\"F_20_sum\"','length': 0,'name': 'Y_F_10','precision': 0,'type': 6},{'expression': ' -0.0016*\"F_0_sum\" + 0.0144*\"F_5_sum\" + 0.2224*\"F_10_sum\" - 0.0416*\"F_15_sum\" + 0.0064*\"F_20_sum\"','length': 0,'name': 'Y_F_11','precision': 0,'type': 6},{'expression': ' 0.0064*\"F_0_sum\" - 0.0336*\"F_5_sum\" + 0.2544*\"F_10_sum\" - 0.0336*\"F_15_sum\" + 0.0064*\"F_20_sum\"','length': 0,'name': 'Y_F_12','precision': 0,'type': 6},{'expression': ' 0.0064*\"F_0_sum\" - 0.0416*\"F_5_sum\" + 0.2224*\"F_10_sum\" + 0.0144*\"F_15_sum\" - 0.0016*\"F_20_sum\"','length': 0,'name': 'Y_F_13','precision': 0,'type': 6},{'expression': ' -0.0128*\"F_5_sum\" + 0.0848*\"F_10_sum\" + 0.1504*\"F_15_sum\" - 0.0240*\"F_20_sum\" + 0.0016*\"F_25_sum\"','length': 0,'name': 'Y_F_15','precision': 0,'type': 6},{'expression': ' -0.0016*\"F_5_sum\" + 0.0144*\"F_10_sum\" + 0.2224*\"F_15_sum\" - 0.0416*\"F_20_sum\" + 0.0064*\"F_25_sum\"','length': 0,'name': 'Y_F_16','precision': 0,'type': 6},{'expression': ' 0.0064*\"F_5_sum\" - 0.0336*\"F_10_sum\" + 0.2544*\"F_15_sum\" - 0.0336*\"F_20_sum\" + 0.0064*\"F_25_sum\"','length': 0,'name': 'Y_F_17','precision': 0,'type': 6},{'expression': ' 0.0064*\"F_5_sum\" - 0.0416*\"F_10_sum\" + 0.2224*\"F_15_sum\" + 0.0144*\"F_20_sum\" - 0.0016*\"F_25_sum\"','length': 0,'name': 'Y_F_18','precision': 0,'type': 6},{'expression': ' -0.0128*\"F_10_sum\" + 0.0848*\"F_15_sum\" + 0.1504*\"F_20_sum\" - 0.0240*\"F_25_sum\" + 0.0016*\"F_30_sum\"','length': 0,'name': 'Y_F_20','precision': 0,'type': 6},{'expression': ' -0.0016*\"F_10_sum\" + 0.0144*\"F_15_sum\" + 0.2224*\"F_20_sum\" - 0.0416*\"F_25_sum\" + 0.0064*\"F_30_sum\"','length': 0,'name': 'Y_F_21','precision': 0,'type': 6},{'expression': ' 0.0064*\"F_10_sum\" - 0.0336*\"F_15_sum\" + 0.2544*\"F_20_sum\" - 0.0336*\"F_25_sum\" + 0.0064*\"F_30_sum\"','length': 0,'name': 'Y_F_22','precision': 0,'type': 6},{'expression': ' 0.0064*\"F_10_sum\" - 0.0416*\"F_15_sum\" + 0.2224*\"F_20_sum\" + 0.0144*\"F_25_sum\" - 0.0016*\"F_30_sum\"','length': 0,'name': 'Y_F_23','precision': 0,'type': 6},{'expression': ' -0.0128*\"F_15_sum\" + 0.0848*\"F_20_sum\" + 0.1504*\"F_25_sum\" - 0.0240*\"F_30_sum\" + 0.0016*\"F_35_sum\"','length': 0,'name': 'Y_F_25','precision': 0,'type': 6},{'expression': ' -0.0016*\"F_15_sum\" + 0.0144*\"F_20_sum\" + 0.2224*\"F_25_sum\" - 0.0416*\"F_30_sum\" + 0.0064*\"F_35_sum\"','length': 0,'name': 'Y_F_26','precision': 0,'type': 6},{'expression': ' 0.0064*\"F_15_sum\" - 0.0336*\"F_20_sum\" + 0.2544*\"F_25_sum\" - 0.0336*\"F_30_sum\" + 0.0064*\"F_35_sum\"','length': 0,'name': 'Y_F_27','precision': 0,'type': 6},{'expression': ' 0.0064*\"F_15_sum\" - 0.0416*\"F_20_sum\" + 0.2224*\"F_25_sum\" + 0.0144*\"F_30_sum\" - 0.0016*\"F_35_sum\"','length': 0,'name': 'Y_F_28','precision': 0,'type': 6},{'expression': '\"M_0_sum\"','length': 0,'name': 'M_0_sum','precision': 0,'type': 6},{'expression': '\"M_5_sum\"','length': 0,'name': 'M_5_sum','precision': 0,'type': 6},{'expression': '\"M_10_sum\"','length': 0,'name': 'M_10_sum','precision': 0,'type': 6},{'expression': '\"M_15_sum\"','length': 0,'name': 'M_15_sum','precision': 0,'type': 6},{'expression': '\"M_20_sum\"','length': 0,'name': 'M_20_sum','precision': 0,'type': 6},{'expression': '\"M_25_sum\"','length': 0,'name': 'M_25_sum','precision': 0,'type': 6},{'expression': '\"F_0_sum\"','length': 0,'name': 'F_0_sum','precision': 0,'type': 6},{'expression': '\"F_5_sum\"','length': 0,'name': 'F_5_sum','precision': 0,'type': 6},{'expression': '\"F_10_sum\"','length': 0,'name': 'F_10_sum','precision': 0,'type': 6},{'expression': '\"F_15_sum\"','length': 0,'name': 'F_15_sum','precision': 0,'type': 6},{'expression': '\"F_20_sum\"','length': 0,'name': 'F_20_sum','precision': 0,'type': 6},{'expression': '\"F_25_sum\"','length': 0,'name': 'F_25_sum','precision': 0,'type': 6}],
            'INPUT': outputs['CreatingThe0To4AgeGroups']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatingSingleYearsOfAgeSection1'] = processing.run('native:refactorfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(22)
        if feedback.isCanceled():
            return {}

        # Create spatial index - Section 1
        alg_params = {
            'INPUT': outputs['CalculatingSingleYearsOfAgeSection1']['OUTPUT']
        }
        outputs['CreateSpatialIndexSection1'] = processing.run('native:createspatialindex', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(23)
        if feedback.isCanceled():
            return {}

        # Calculating single years of age - Section 2
        alg_params = {
            'FIELDS_MAPPING': [{'expression': '\"M_0_sum\" - \"Y_M_0\" - \"Y_M_1\" - \"Y_M_2\" - \"Y_M_3\"','length': 0,'name': 'Y_M_4','precision': 0,'type': 6},{'expression': '\"M_5_sum\" - \"Y_M_5\" - \"Y_M_6\" - \"Y_M_7\" - \"Y_M_8\"','length': 0,'name': 'Y_M_9','precision': 0,'type': 6},{'expression': '\"M_10_sum\" - \"Y_M_10\" - \"Y_M_11\" - \"Y_M_12\" - \"Y_M_13\"','length': 0,'name': 'Y_M_14','precision': 0,'type': 6},{'expression': '\"M_15_sum\" - \"Y_M_15\" - \"Y_M_16\" - \"Y_M_17\" - \"Y_M_18\"','length': 0,'name': 'Y_M_19','precision': 0,'type': 6},{'expression': '\"M_20_sum\" - \"Y_M_20\" - \"Y_M_21\" - \"Y_M_22\" - \"Y_M_23\"','length': 0,'name': 'Y_M_24','precision': 0,'type': 6},{'expression': '\"M_25_sum\" - \"Y_M_25\" - \"Y_M_26\" - \"Y_M_27\" - \"Y_M_28\"','length': 0,'name': 'Y_M_29','precision': 0,'type': 6},{'expression': '\"F_0_sum\" - \"Y_F_0\" - \"Y_F_1\" - \"Y_F_2\" - \"Y_F_3\"','length': 0,'name': 'Y_F_4','precision': 0,'type': 6},{'expression': '\"F_5_sum\" - \"Y_F_5\" - \"Y_F_6\" - \"Y_F_7\" - \"Y_F_8\"','length': 0,'name': 'Y_F_9','precision': 0,'type': 6},{'expression': '\"F_10_sum\" - \"Y_F_10\" - \"Y_F_11\" - \"Y_F_12\" - \"Y_F_13\"','length': 0,'name': 'Y_F_14','precision': 0,'type': 6},{'expression': '\"F_15_sum\" - \"Y_F_15\" - \"Y_F_16\" - \"Y_F_17\" - \"Y_F_18\"','length': 0,'name': 'Y_F_19','precision': 0,'type': 6},{'expression': '\"F_20_sum\" - \"Y_F_20\" - \"Y_F_21\" - \"Y_F_22\" - \"Y_F_23\"','length': 0,'name': 'Y_F_24','precision': 0,'type': 6},{'expression': '\"F_25_sum\" - \"Y_F_25\" - \"Y_F_26\" - \"Y_F_27\" - \"Y_F_28\"','length': 0,'name': 'Y_F_29','precision': 0,'type': 6},{'expression': '\"Y_M_0\" + \"Y_F_0\"','length': 0,'name': 'Y_T_0','precision': 0,'type': 6},{'expression': '\"Y_M_1\" + \"Y_F_1\"','length': 0,'name': 'Y_T_1','precision': 0,'type': 6},{'expression': ' \"Y_M_2\" + \"Y_F_2\"','length': 0,'name': 'Y_T_2','precision': 0,'type': 6},{'expression': '\"Y_M_3\" + \"Y_F_3\"','length': 0,'name': 'Y_T_3','precision': 0,'type': 6},{'expression': '\"Y_M_5\" + \"Y_F_5\"','length': 0,'name': 'Y_T_5','precision': 0,'type': 6},{'expression': '\"Y_M_6\" + \"Y_F_6\"','length': 0,'name': 'Y_T_6','precision': 0,'type': 6},{'expression': '\"Y_M_7\" + \"Y_F_7\"','length': 0,'name': 'Y_T_7','precision': 0,'type': 6},{'expression': '\"Y_M_8\" + \"Y_F_8\"','length': 0,'name': 'Y_T_8','precision': 0,'type': 6},{'expression': '\"Y_M_10\" + \"Y_F_10\"','length': 0,'name': 'Y_T_10','precision': 0,'type': 6},{'expression': '\"Y_M_11\" + \"Y_F_11\"','length': 0,'name': 'Y_T_11','precision': 0,'type': 6},{'expression': '\"Y_M_12\" + \"Y_F_12\"','length': 0,'name': 'Y_T_12','precision': 0,'type': 6},{'expression': '\"Y_M_13\" + \"Y_F_13\"','length': 0,'name': 'Y_T_13','precision': 0,'type': 6},{'expression': ' \"Y_M_15\" + \"Y_F_15\"','length': 0,'name': 'Y_T_15','precision': 0,'type': 6},{'expression': '\"Y_M_16\" + \"Y_F_16\"','length': 0,'name': 'Y_T_16','precision': 0,'type': 6},{'expression': '\"Y_M_17\" + \"Y_F_17\"','length': 0,'name': 'Y_T_17','precision': 0,'type': 6},{'expression': '\"Y_M_18\" + \"Y_F_18\"','length': 0,'name': 'Y_T_18','precision': 0,'type': 6},{'expression': '\"Y_M_20\" + \"Y_F_20\"','length': 0,'name': 'Y_T_20','precision': 0,'type': 6},{'expression': '\"Y_M_21\" + \"Y_F_21\"','length': 0,'name': 'Y_T_21','precision': 0,'type': 6},{'expression': '\"Y_M_22\" + \"Y_F_22\"','length': 0,'name': 'Y_T_22','precision': 0,'type': 6},{'expression': ' \"Y_M_23\" + \"Y_F_23\"','length': 0,'name': 'Y_T_23','precision': 0,'type': 6},{'expression': '\"Y_M_25\" + \"Y_F_25\"','length': 0,'name': 'Y_T_25','precision': 0,'type': 6},{'expression': '\"Y_M_26\" + \"Y_F_26\"','length': 0,'name': 'Y_T_26','precision': 0,'type': 6},{'expression': '\"Y_M_27\" + \"Y_F_27\"','length': 0,'name': 'Y_T_27','precision': 0,'type': 6},{'expression': '\"Y_M_28\" + \"Y_F_28\"','length': 0,'name': 'Y_T_28','precision': 0,'type': 6}],
            'INPUT': outputs['CreateSpatialIndexSection1']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatingSingleYearsOfAgeSection2'] = processing.run('native:refactorfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(24)
        if feedback.isCanceled():
            return {}

        # Create spatial index - Section 2
        alg_params = {
            'INPUT': outputs['CalculatingSingleYearsOfAgeSection2']['OUTPUT']
        }
        outputs['CreateSpatialIndexSection2'] = processing.run('native:createspatialindex', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(25)
        if feedback.isCanceled():
            return {}

        # Calculating single years of age - Section 3
        alg_params = {
            'FIELDS_MAPPING': [{'expression': '\"Y_M_4\" + \"Y_F_4\"','length': 0,'name': 'Y_T_4','precision': 0,'type': 6},{'expression': '\"Y_M_9\" + \"Y_F_9\"','length': 0,'name': 'Y_T_9','precision': 0,'type': 6},{'expression': '\"Y_M_14\" + \"Y_F_14\"','length': 0,'name': 'Y_T_14','precision': 0,'type': 6},{'expression': '\"Y_M_19\" + \"Y_F_19\"','length': 0,'name': 'Y_T_19','precision': 0,'type': 6},{'expression': '\"Y_M_24\" + \"Y_F_24\"','length': 0,'name': 'Y_T_24','precision': 0,'type': 6},{'expression': '\"Y_M_29\" + \"Y_F_29\"','length': 0,'name': 'Y_T_29','precision': 0,'type': 6}],
            'INPUT': outputs['CreateSpatialIndexSection2']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatingSingleYearsOfAgeSection3'] = processing.run('native:refactorfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(26)
        if feedback.isCanceled():
            return {}

        # Create spatial index - Section 3
        alg_params = {
            'INPUT': outputs['CalculatingSingleYearsOfAgeSection3']['OUTPUT']
        }
        outputs['CreateSpatialIndexSection3'] = processing.run('native:createspatialindex', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(27)
        if feedback.isCanceled():
            return {}

        # Join attributes by location - Section 1 and 2
        alg_params = {
            'DISCARD_NONMATCHING': True,
            'INPUT': outputs['CreateSpatialIndexSection1']['OUTPUT'],
            'JOIN': outputs['CreateSpatialIndexSection2']['OUTPUT'],
            'JOIN_FIELDS': [''],
            'METHOD': 1,
            'PREDICATE': [2],
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinAttributesByLocationSection1And2'] = processing.run('native:joinattributesbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(28)
        if feedback.isCanceled():
            return {}

        # Create spatial index for Section 1 and 2
        alg_params = {
            'INPUT': outputs['JoinAttributesByLocationSection1And2']['OUTPUT']
        }
        outputs['CreateSpatialIndexForSection1And2'] = processing.run('native:createspatialindex', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(29)
        if feedback.isCanceled():
            return {}

        # Join attributes by location - Sections 1 through 3
        alg_params = {
            'DISCARD_NONMATCHING': True,
            'INPUT': outputs['CreateSpatialIndexForSection1And2']['OUTPUT'],
            'JOIN': outputs['CreateSpatialIndexSection3']['OUTPUT'],
            'JOIN_FIELDS': [''],
            'METHOD': 1,
            'PREDICATE': [2],
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinAttributesByLocationSections1Through3'] = processing.run('native:joinattributesbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(30)
        if feedback.isCanceled():
            return {}

        # Reorganizing the results
        alg_params = {
            'FIELDS_MAPPING': [{'expression': '\"Y_M_0\"','length': 0,'name': 'Y_M_0','precision': 0,'type': 6},{'expression': '\"Y_M_1\"','length': 0,'name': 'Y_M_1','precision': 0,'type': 6},{'expression': '\"Y_M_2\"','length': 0,'name': 'Y_M_2','precision': 0,'type': 6},{'expression': '\"Y_M_3\"','length': 0,'name': 'Y_M_3','precision': 0,'type': 6},{'expression': '\"Y_M_4\"','length': 0,'name': 'Y_M_4','precision': 0,'type': 6},{'expression': '\"Y_M_5\"','length': 0,'name': 'Y_M_5','precision': 0,'type': 6},{'expression': '\"Y_M_6\"','length': 0,'name': 'Y_M_6','precision': 0,'type': 6},{'expression': '\"Y_M_7\"','length': 0,'name': 'Y_M_7','precision': 0,'type': 6},{'expression': '\"Y_M_8\"','length': 0,'name': 'Y_M_8','precision': 0,'type': 6},{'expression': '\"Y_M_9\"','length': 0,'name': 'Y_M_9','precision': 0,'type': 6},{'expression': '\"Y_M_10\"','length': 0,'name': 'Y_M_10','precision': 0,'type': 6},{'expression': '\"Y_M_11\"','length': 0,'name': 'Y_M_11','precision': 0,'type': 6},{'expression': '\"Y_M_12\"','length': 0,'name': 'Y_M_12','precision': 0,'type': 6},{'expression': '\"Y_M_13\"','length': 0,'name': 'Y_M_13','precision': 0,'type': 6},{'expression': '\"Y_M_14\"','length': 0,'name': 'Y_M_14','precision': 0,'type': 6},{'expression': '\"Y_M_15\"','length': 0,'name': 'Y_M_15','precision': 0,'type': 6},{'expression': '\"Y_M_16\"','length': 0,'name': 'Y_M_16','precision': 0,'type': 6},{'expression': '\"Y_M_17\"','length': 0,'name': 'Y_M_17','precision': 0,'type': 6},{'expression': '\"Y_M_18\"','length': 0,'name': 'Y_M_18','precision': 0,'type': 6},{'expression': '\"Y_M_19\"','length': 0,'name': 'Y_M_19','precision': 0,'type': 6},{'expression': '\"Y_M_20\"','length': 0,'name': 'Y_M_20','precision': 0,'type': 6},{'expression': '\"Y_M_21\"','length': 0,'name': 'Y_M_21','precision': 0,'type': 6},{'expression': '\"Y_M_22\"','length': 0,'name': 'Y_M_22','precision': 0,'type': 6},{'expression': '\"Y_M_23\"','length': 0,'name': 'Y_M_23','precision': 0,'type': 6},{'expression': '\"Y_M_24\"','length': 0,'name': 'Y_M_24','precision': 0,'type': 6},{'expression': '\"Y_M_25\"','length': 0,'name': 'Y_M_25','precision': 0,'type': 6},{'expression': '\"Y_M_26\"','length': 0,'name': 'Y_M_26','precision': 0,'type': 6},{'expression': '\"Y_M_27\"','length': 0,'name': 'Y_M_27','precision': 0,'type': 6},{'expression': '\"Y_M_28\"','length': 0,'name': 'Y_M_28','precision': 0,'type': 6},{'expression': '\"Y_M_29\"','length': 0,'name': 'Y_M_29','precision': 0,'type': 6},{'expression': '\"Y_F_0\"','length': 0,'name': 'Y_F_0','precision': 0,'type': 6},{'expression': '\"Y_F_1\"','length': 0,'name': 'Y_F_1','precision': 0,'type': 6},{'expression': '\"Y_F_2\"','length': 0,'name': 'Y_F_2','precision': 0,'type': 6},{'expression': '\"Y_F_3\"','length': 0,'name': 'Y_F_3','precision': 0,'type': 6},{'expression': '\"Y_F_4\"','length': 0,'name': 'Y_F_4','precision': 0,'type': 6},{'expression': '\"Y_F_5\"','length': 0,'name': 'Y_F_5','precision': 0,'type': 6},{'expression': '\"Y_F_6\"','length': 0,'name': 'Y_F_6','precision': 0,'type': 6},{'expression': '\"Y_F_7\"','length': 0,'name': 'Y_F_7','precision': 0,'type': 6},{'expression': '\"Y_F_8\"','length': 0,'name': 'Y_F_8','precision': 0,'type': 6},{'expression': '\"Y_F_9\"','length': 0,'name': 'Y_F_9','precision': 0,'type': 6},{'expression': '\"Y_F_10\"','length': 0,'name': 'Y_F_10','precision': 0,'type': 6},{'expression': '\"Y_F_11\"','length': 0,'name': 'Y_F_11','precision': 0,'type': 6},{'expression': '\"Y_F_12\"','length': 0,'name': 'Y_F_12','precision': 0,'type': 6},{'expression': '\"Y_F_13\"','length': 0,'name': 'Y_F_13','precision': 0,'type': 6},{'expression': '\"Y_F_14\"','length': 0,'name': 'Y_F_14','precision': 0,'type': 6},{'expression': '\"Y_F_15\"','length': 0,'name': 'Y_F_15','precision': 0,'type': 6},{'expression': '\"Y_F_16\"','length': 0,'name': 'Y_F_16','precision': 0,'type': 6},{'expression': '\"Y_F_17\"','length': 0,'name': 'Y_F_17','precision': 0,'type': 6},{'expression': '\"Y_F_18\"','length': 0,'name': 'Y_F_18','precision': 0,'type': 6},{'expression': '\"Y_F_19\"','length': 0,'name': 'Y_F_19','precision': 0,'type': 6},{'expression': '\"Y_F_20\"','length': 0,'name': 'Y_F_20','precision': 0,'type': 6},{'expression': '\"Y_F_21\"','length': 0,'name': 'Y_F_21','precision': 0,'type': 6},{'expression': '\"Y_F_22\"','length': 0,'name': 'Y_F_22','precision': 0,'type': 6},{'expression': '\"Y_F_23\"','length': 0,'name': 'Y_F_23','precision': 0,'type': 6},{'expression': '\"Y_F_24\"','length': 0,'name': 'Y_F_24','precision': 0,'type': 6},{'expression': '\"Y_F_25\"','length': 0,'name': 'Y_F_25','precision': 0,'type': 6},{'expression': '\"Y_F_26\"','length': 0,'name': 'Y_F_26','precision': 0,'type': 6},{'expression': '\"Y_F_27\"','length': 0,'name': 'Y_F_27','precision': 0,'type': 6},{'expression': '\"Y_F_28\"','length': 0,'name': 'Y_F_28','precision': 0,'type': 6},{'expression': '\"Y_F_29\"','length': 0,'name': 'Y_F_29','precision': 0,'type': 6},{'expression': '\"Y_T_0\"','length': 0,'name': 'Y_T_0','precision': 0,'type': 6},{'expression': '\"Y_T_1\"','length': 0,'name': 'Y_T_1','precision': 0,'type': 6},{'expression': '\"Y_T_2\"','length': 0,'name': 'Y_T_2','precision': 0,'type': 6},{'expression': '\"Y_T_3\"','length': 0,'name': 'Y_T_3','precision': 0,'type': 6},{'expression': '\"Y_T_4\"','length': 0,'name': 'Y_T_4','precision': 0,'type': 6},{'expression': '\"Y_T_5\"','length': 0,'name': 'Y_T_5','precision': 0,'type': 6},{'expression': '\"Y_T_6\"','length': 0,'name': 'Y_T_6','precision': 0,'type': 6},{'expression': '\"Y_T_7\"','length': 0,'name': 'Y_T_7','precision': 0,'type': 6},{'expression': '\"Y_T_8\"','length': 0,'name': 'Y_T_8','precision': 0,'type': 6},{'expression': '\"Y_T_9\"','length': 0,'name': 'Y_T_9','precision': 0,'type': 6},{'expression': '\"Y_T_10\"','length': 0,'name': 'Y_T_10','precision': 0,'type': 6},{'expression': '\"Y_T_11\"','length': 0,'name': 'Y_T_11','precision': 0,'type': 6},{'expression': '\"Y_T_12\"','length': 0,'name': 'Y_T_12','precision': 0,'type': 6},{'expression': '\"Y_T_13\"','length': 0,'name': 'Y_T_13','precision': 0,'type': 6},{'expression': '\"Y_T_14\"','length': 0,'name': 'Y_T_14','precision': 0,'type': 6},{'expression': '\"Y_T_15\"','length': 0,'name': 'Y_T_15','precision': 0,'type': 6},{'expression': '\"Y_T_16\"','length': 0,'name': 'Y_T_16','precision': 0,'type': 6},{'expression': '\"Y_T_17\"','length': 0,'name': 'Y_T_17','precision': 0,'type': 6},{'expression': '\"Y_T_18\"','length': 0,'name': 'Y_T_18','precision': 0,'type': 6},{'expression': '\"Y_T_19\"','length': 0,'name': 'Y_T_19','precision': 0,'type': 6},{'expression': '\"Y_T_20\"','length': 0,'name': 'Y_T_20','precision': 0,'type': 6},{'expression': '\"Y_T_21\"','length': 0,'name': 'Y_T_21','precision': 0,'type': 6},{'expression': '\"Y_T_22\"','length': 0,'name': 'Y_T_22','precision': 0,'type': 6},{'expression': '\"Y_T_23\"','length': 0,'name': 'Y_T_23','precision': 0,'type': 6},{'expression': '\"Y_T_24\"','length': 0,'name': 'Y_T_24','precision': 0,'type': 6},{'expression': '\"Y_T_25\"','length': 0,'name': 'Y_T_25','precision': 0,'type': 6},{'expression': '\"Y_T_26\"','length': 0,'name': 'Y_T_26','precision': 0,'type': 6},{'expression': '\"Y_T_27\"','length': 0,'name': 'Y_T_27','precision': 0,'type': 6},{'expression': '\"Y_T_28\"','length': 0,'name': 'Y_T_28','precision': 0,'type': 6},{'expression': '\"Y_T_29\"','length': 0,'name': 'Y_T_29','precision': 0,'type': 6}],
            'INPUT': outputs['JoinAttributesByLocationSections1Through3']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ReorganizingTheResults'] = processing.run('native:refactorfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(31)
        if feedback.isCanceled():
            return {}

        # Calculating school ages with Secondary
        alg_params = {
            'FIELDS_MAPPING': [{'expression': '\"Y_M_0\"','length': 0,'name': 'Y_M_0','precision': 0,'type': 6},{'expression': '\"Y_M_1\"','length': 0,'name': 'Y_M_1','precision': 0,'type': 6},{'expression': '\"Y_M_2\"','length': 0,'name': 'Y_M_2','precision': 0,'type': 6},{'expression': '\"Y_M_3\"','length': 0,'name': 'Y_M_3','precision': 0,'type': 6},{'expression': '\"Y_M_4\"','length': 0,'name': 'Y_M_4','precision': 0,'type': 6},{'expression': '\"Y_M_5\"','length': 0,'name': 'Y_M_5','precision': 0,'type': 6},{'expression': '\"Y_M_6\"','length': 0,'name': 'Y_M_6','precision': 0,'type': 6},{'expression': '\"Y_M_7\"','length': 0,'name': 'Y_M_7','precision': 0,'type': 6},{'expression': '\"Y_M_8\"','length': 0,'name': 'Y_M_8','precision': 0,'type': 6},{'expression': '\"Y_M_9\"','length': 0,'name': 'Y_M_9','precision': 0,'type': 6},{'expression': '\"Y_M_10\"','length': 0,'name': 'Y_M_10','precision': 0,'type': 6},{'expression': '\"Y_M_11\"','length': 0,'name': 'Y_M_11','precision': 0,'type': 6},{'expression': '\"Y_M_12\"','length': 0,'name': 'Y_M_12','precision': 0,'type': 6},{'expression': '\"Y_M_13\"','length': 0,'name': 'Y_M_13','precision': 0,'type': 6},{'expression': '\"Y_M_14\"','length': 0,'name': 'Y_M_14','precision': 0,'type': 6},{'expression': '\"Y_M_15\"','length': 0,'name': 'Y_M_15','precision': 0,'type': 6},{'expression': '\"Y_M_16\"','length': 0,'name': 'Y_M_16','precision': 0,'type': 6},{'expression': '\"Y_M_17\"','length': 0,'name': 'Y_M_17','precision': 0,'type': 6},{'expression': '\"Y_M_18\"','length': 0,'name': 'Y_M_18','precision': 0,'type': 6},{'expression': '\"Y_M_19\"','length': 0,'name': 'Y_M_19','precision': 0,'type': 6},{'expression': '\"Y_M_20\"','length': 0,'name': 'Y_M_20','precision': 0,'type': 6},{'expression': '\"Y_M_21\"','length': 0,'name': 'Y_M_21','precision': 0,'type': 6},{'expression': '\"Y_M_22\"','length': 0,'name': 'Y_M_22','precision': 0,'type': 6},{'expression': '\"Y_M_23\"','length': 0,'name': 'Y_M_23','precision': 0,'type': 6},{'expression': '\"Y_M_24\"','length': 0,'name': 'Y_M_24','precision': 0,'type': 6},{'expression': '\"Y_M_25\"','length': 0,'name': 'Y_M_25','precision': 0,'type': 6},{'expression': '\"Y_M_26\"','length': 0,'name': 'Y_M_26','precision': 0,'type': 6},{'expression': '\"Y_M_27\"','length': 0,'name': 'Y_M_27','precision': 0,'type': 6},{'expression': '\"Y_M_28\"','length': 0,'name': 'Y_M_28','precision': 0,'type': 6},{'expression': '\"Y_M_29\"','length': 0,'name': 'Y_M_29','precision': 0,'type': 6},{'expression': '\"Y_F_0\"','length': 0,'name': 'Y_F_0','precision': 0,'type': 6},{'expression': '\"Y_F_1\"','length': 0,'name': 'Y_F_1','precision': 0,'type': 6},{'expression': '\"Y_F_2\"','length': 0,'name': 'Y_F_2','precision': 0,'type': 6},{'expression': '\"Y_F_3\"','length': 0,'name': 'Y_F_3','precision': 0,'type': 6},{'expression': '\"Y_F_4\"','length': 0,'name': 'Y_F_4','precision': 0,'type': 6},{'expression': '\"Y_F_5\"','length': 0,'name': 'Y_F_5','precision': 0,'type': 6},{'expression': '\"Y_F_6\"','length': 0,'name': 'Y_F_6','precision': 0,'type': 6},{'expression': '\"Y_F_7\"','length': 0,'name': 'Y_F_7','precision': 0,'type': 6},{'expression': '\"Y_F_8\"','length': 0,'name': 'Y_F_8','precision': 0,'type': 6},{'expression': '\"Y_F_9\"','length': 0,'name': 'Y_F_9','precision': 0,'type': 6},{'expression': '\"Y_F_10\"','length': 0,'name': 'Y_F_10','precision': 0,'type': 6},{'expression': '\"Y_F_11\"','length': 0,'name': 'Y_F_11','precision': 0,'type': 6},{'expression': '\"Y_F_12\"','length': 0,'name': 'Y_F_12','precision': 0,'type': 6},{'expression': '\"Y_F_13\"','length': 0,'name': 'Y_F_13','precision': 0,'type': 6},{'expression': '\"Y_F_14\"','length': 0,'name': 'Y_F_14','precision': 0,'type': 6},{'expression': '\"Y_F_15\"','length': 0,'name': 'Y_F_15','precision': 0,'type': 6},{'expression': '\"Y_F_16\"','length': 0,'name': 'Y_F_16','precision': 0,'type': 6},{'expression': '\"Y_F_17\"','length': 0,'name': 'Y_F_17','precision': 0,'type': 6},{'expression': '\"Y_F_18\"','length': 0,'name': 'Y_F_18','precision': 0,'type': 6},{'expression': '\"Y_F_19\"','length': 0,'name': 'Y_F_19','precision': 0,'type': 6},{'expression': '\"Y_F_20\"','length': 0,'name': 'Y_F_20','precision': 0,'type': 6},{'expression': '\"Y_F_21\"','length': 0,'name': 'Y_F_21','precision': 0,'type': 6},{'expression': '\"Y_F_22\"','length': 0,'name': 'Y_F_22','precision': 0,'type': 6},{'expression': '\"Y_F_23\"','length': 0,'name': 'Y_F_23','precision': 0,'type': 6},{'expression': '\"Y_F_24\"','length': 0,'name': 'Y_F_24','precision': 0,'type': 6},{'expression': '\"Y_F_25\"','length': 0,'name': 'Y_F_25','precision': 0,'type': 6},{'expression': '\"Y_F_26\"','length': 0,'name': 'Y_F_26','precision': 0,'type': 6},{'expression': '\"Y_F_27\"','length': 0,'name': 'Y_F_27','precision': 0,'type': 6},{'expression': '\"Y_F_28\"','length': 0,'name': 'Y_F_28','precision': 0,'type': 6},{'expression': '\"Y_F_29\"','length': 0,'name': 'Y_F_29','precision': 0,'type': 6},{'expression': '\"Y_T_0\"','length': 0,'name': 'Y_T_0','precision': 0,'type': 6},{'expression': '\"Y_T_1\"','length': 0,'name': 'Y_T_1','precision': 0,'type': 6},{'expression': '\"Y_T_2\"','length': 0,'name': 'Y_T_2','precision': 0,'type': 6},{'expression': '\"Y_T_3\"','length': 0,'name': 'Y_T_3','precision': 0,'type': 6},{'expression': '\"Y_T_4\"','length': 0,'name': 'Y_T_4','precision': 0,'type': 6},{'expression': '\"Y_T_5\"','length': 0,'name': 'Y_T_5','precision': 0,'type': 6},{'expression': '\"Y_T_6\"','length': 0,'name': 'Y_T_6','precision': 0,'type': 6},{'expression': '\"Y_T_7\"','length': 0,'name': 'Y_T_7','precision': 0,'type': 6},{'expression': '\"Y_T_8\"','length': 0,'name': 'Y_T_8','precision': 0,'type': 6},{'expression': '\"Y_T_9\"','length': 0,'name': 'Y_T_9','precision': 0,'type': 6},{'expression': '\"Y_T_10\"','length': 0,'name': 'Y_T_10','precision': 0,'type': 6},{'expression': '\"Y_T_11\"','length': 0,'name': 'Y_T_11','precision': 0,'type': 6},{'expression': '\"Y_T_12\"','length': 0,'name': 'Y_T_12','precision': 0,'type': 6},{'expression': '\"Y_T_13\"','length': 0,'name': 'Y_T_13','precision': 0,'type': 6},{'expression': '\"Y_T_14\"','length': 0,'name': 'Y_T_14','precision': 0,'type': 6},{'expression': '\"Y_T_15\"','length': 0,'name': 'Y_T_15','precision': 0,'type': 6},{'expression': '\"Y_T_16\"','length': 0,'name': 'Y_T_16','precision': 0,'type': 6},{'expression': '\"Y_T_17\"','length': 0,'name': 'Y_T_17','precision': 0,'type': 6},{'expression': '\"Y_T_18\"','length': 0,'name': 'Y_T_18','precision': 0,'type': 6},{'expression': '\"Y_T_19\"','length': 0,'name': 'Y_T_19','precision': 0,'type': 6},{'expression': '\"Y_T_20\"','length': 0,'name': 'Y_T_20','precision': 0,'type': 6},{'expression': '\"Y_T_21\"','length': 0,'name': 'Y_T_21','precision': 0,'type': 6},{'expression': '\"Y_T_22\"','length': 0,'name': 'Y_T_22','precision': 0,'type': 6},{'expression': '\"Y_T_23\"','length': 0,'name': 'Y_T_23','precision': 0,'type': 6},{'expression': '\"Y_T_24\"','length': 0,'name': 'Y_T_24','precision': 0,'type': 6},{'expression': '\"Y_T_25\"','length': 0,'name': 'Y_T_25','precision': 0,'type': 6},{'expression': '\"Y_T_26\"','length': 0,'name': 'Y_T_26','precision': 0,'type': 6},{'expression': '\"Y_T_27\"','length': 0,'name': 'Y_T_27','precision': 0,'type': 6},{'expression': '\"Y_T_28\"','length': 0,'name': 'Y_T_28','precision': 0,'type': 6},{'expression': '\"Y_T_29\"','length': 0,'name': 'Y_T_29','precision': 0,'type': 6},{'expression': 'eval(array_to_string(array_foreach(generate_series( @Preprimarystartingage ,  @Preprimarystartingage + @Preprimaryduration - 1),concat(\'\"Y_F_\',@element,\'\"\')),\'+\'))','length': 0,'name': 'Pre_primary_F','precision': 0,'type': 6},{'expression': 'eval(array_to_string(array_foreach(generate_series( @Preprimarystartingage ,  @Preprimarystartingage + @Preprimaryduration - 1),concat(\'\"Y_M_\',@element,\'\"\')),\'+\'))','length': 0,'name': 'Pre_primary_M','precision': 0,'type': 6},{'expression': 'eval(array_to_string(array_foreach(generate_series( @Preprimarystartingage ,  @Preprimarystartingage + @Preprimaryduration - 1),concat(\'\"Y_T_\',@element,\'\"\')),\'+\'))','length': 0,'name': 'Pre_primary_T','precision': 0,'type': 6},{'expression': 'eval(array_to_string(array_foreach(generate_series(  @Primarystartingage  ,   @Primarystartingage  +  @Primaryduration  - 1),concat(\'\"Y_F_\',@element,\'\"\')),\'+\'))','length': 0,'name': 'Primary_F','precision': 0,'type': 6},{'expression': 'eval(array_to_string(array_foreach(generate_series( @Primarystartingage ,  @Primarystartingage + @Primaryduration - 1),concat(\'\"Y_M_\',@element,\'\"\')),\'+\'))','length': 0,'name': 'Primary_M','precision': 0,'type': 6},{'expression': 'eval(array_to_string(array_foreach(generate_series( @Primarystartingage ,  @Primarystartingage + @Primaryduration - 1),concat(\'\"Y_T_\',@element,\'\"\')),\'+\'))','length': 0,'name': 'Primary_T','precision': 0,'type': 6},{'expression': 'eval(array_to_string(array_foreach(generate_series(    @Secondarystartingage    ,     @Secondarystartingage + @Secondaryduration    - 1),concat(\'\"Y_F_\',@element,\'\"\')),\'+\'))','length': 0,'name': 'Sec_F','precision': 0,'type': 6},{'expression': 'eval(array_to_string(array_foreach(generate_series(    @Secondarystartingage    ,     @Secondarystartingage + @Secondaryduration    - 1),concat(\'\"Y_M_\',@element,\'\"\')),\'+\'))','length': 0,'name': 'Sec_M','precision': 0,'type': 6},{'expression': 'eval(array_to_string(array_foreach(generate_series(    @Secondarystartingage    ,     @Secondarystartingage + @Secondaryduration    - 1),concat(\'\"Y_T_\',@element,\'\"\')),\'+\'))','length': 0,'name': 'Sec_T','precision': 0,'type': 6}],
            'INPUT': outputs['ReorganizingTheResults']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatingSchoolAgesWithSecondary'] = processing.run('native:refactorfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(32)
        if feedback.isCanceled():
            return {}

        # Create spatial index for Secondary
        alg_params = {
            'INPUT': outputs['CalculatingSchoolAgesWithSecondary']['OUTPUT']
        }
        outputs['CreateSpatialIndexForSecondary'] = processing.run('native:createspatialindex', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(33)
        if feedback.isCanceled():
            return {}

        # Calculating school ages with Lower and Upper secondary
        alg_params = {
            'FIELDS_MAPPING': [{'expression': '\"Y_M_0\"','length': 0,'name': 'Y_M_0','precision': 0,'type': 6},{'expression': '\"Y_M_1\"','length': 0,'name': 'Y_M_1','precision': 0,'type': 6},{'expression': '\"Y_M_2\"','length': 0,'name': 'Y_M_2','precision': 0,'type': 6},{'expression': '\"Y_M_3\"','length': 0,'name': 'Y_M_3','precision': 0,'type': 6},{'expression': '\"Y_M_4\"','length': 0,'name': 'Y_M_4','precision': 0,'type': 6},{'expression': '\"Y_M_5\"','length': 0,'name': 'Y_M_5','precision': 0,'type': 6},{'expression': '\"Y_M_6\"','length': 0,'name': 'Y_M_6','precision': 0,'type': 6},{'expression': '\"Y_M_7\"','length': 0,'name': 'Y_M_7','precision': 0,'type': 6},{'expression': '\"Y_M_8\"','length': 0,'name': 'Y_M_8','precision': 0,'type': 6},{'expression': '\"Y_M_9\"','length': 0,'name': 'Y_M_9','precision': 0,'type': 6},{'expression': '\"Y_M_10\"','length': 0,'name': 'Y_M_10','precision': 0,'type': 6},{'expression': '\"Y_M_11\"','length': 0,'name': 'Y_M_11','precision': 0,'type': 6},{'expression': '\"Y_M_12\"','length': 0,'name': 'Y_M_12','precision': 0,'type': 6},{'expression': '\"Y_M_13\"','length': 0,'name': 'Y_M_13','precision': 0,'type': 6},{'expression': '\"Y_M_14\"','length': 0,'name': 'Y_M_14','precision': 0,'type': 6},{'expression': '\"Y_M_15\"','length': 0,'name': 'Y_M_15','precision': 0,'type': 6},{'expression': '\"Y_M_16\"','length': 0,'name': 'Y_M_16','precision': 0,'type': 6},{'expression': '\"Y_M_17\"','length': 0,'name': 'Y_M_17','precision': 0,'type': 6},{'expression': '\"Y_M_18\"','length': 0,'name': 'Y_M_18','precision': 0,'type': 6},{'expression': '\"Y_M_19\"','length': 0,'name': 'Y_M_19','precision': 0,'type': 6},{'expression': '\"Y_M_20\"','length': 0,'name': 'Y_M_20','precision': 0,'type': 6},{'expression': '\"Y_M_21\"','length': 0,'name': 'Y_M_21','precision': 0,'type': 6},{'expression': '\"Y_M_22\"','length': 0,'name': 'Y_M_22','precision': 0,'type': 6},{'expression': '\"Y_M_23\"','length': 0,'name': 'Y_M_23','precision': 0,'type': 6},{'expression': '\"Y_M_24\"','length': 0,'name': 'Y_M_24','precision': 0,'type': 6},{'expression': '\"Y_M_25\"','length': 0,'name': 'Y_M_25','precision': 0,'type': 6},{'expression': '\"Y_M_26\"','length': 0,'name': 'Y_M_26','precision': 0,'type': 6},{'expression': '\"Y_M_27\"','length': 0,'name': 'Y_M_27','precision': 0,'type': 6},{'expression': '\"Y_M_28\"','length': 0,'name': 'Y_M_28','precision': 0,'type': 6},{'expression': '\"Y_M_29\"','length': 0,'name': 'Y_M_29','precision': 0,'type': 6},{'expression': '\"Y_F_0\"','length': 0,'name': 'Y_F_0','precision': 0,'type': 6},{'expression': '\"Y_F_1\"','length': 0,'name': 'Y_F_1','precision': 0,'type': 6},{'expression': '\"Y_F_2\"','length': 0,'name': 'Y_F_2','precision': 0,'type': 6},{'expression': '\"Y_F_3\"','length': 0,'name': 'Y_F_3','precision': 0,'type': 6},{'expression': '\"Y_F_4\"','length': 0,'name': 'Y_F_4','precision': 0,'type': 6},{'expression': '\"Y_F_5\"','length': 0,'name': 'Y_F_5','precision': 0,'type': 6},{'expression': '\"Y_F_6\"','length': 0,'name': 'Y_F_6','precision': 0,'type': 6},{'expression': '\"Y_F_7\"','length': 0,'name': 'Y_F_7','precision': 0,'type': 6},{'expression': '\"Y_F_8\"','length': 0,'name': 'Y_F_8','precision': 0,'type': 6},{'expression': '\"Y_F_9\"','length': 0,'name': 'Y_F_9','precision': 0,'type': 6},{'expression': '\"Y_F_10\"','length': 0,'name': 'Y_F_10','precision': 0,'type': 6},{'expression': '\"Y_F_11\"','length': 0,'name': 'Y_F_11','precision': 0,'type': 6},{'expression': '\"Y_F_12\"','length': 0,'name': 'Y_F_12','precision': 0,'type': 6},{'expression': '\"Y_F_13\"','length': 0,'name': 'Y_F_13','precision': 0,'type': 6},{'expression': '\"Y_F_14\"','length': 0,'name': 'Y_F_14','precision': 0,'type': 6},{'expression': '\"Y_F_15\"','length': 0,'name': 'Y_F_15','precision': 0,'type': 6},{'expression': '\"Y_F_16\"','length': 0,'name': 'Y_F_16','precision': 0,'type': 6},{'expression': '\"Y_F_17\"','length': 0,'name': 'Y_F_17','precision': 0,'type': 6},{'expression': '\"Y_F_18\"','length': 0,'name': 'Y_F_18','precision': 0,'type': 6},{'expression': '\"Y_F_19\"','length': 0,'name': 'Y_F_19','precision': 0,'type': 6},{'expression': '\"Y_F_20\"','length': 0,'name': 'Y_F_20','precision': 0,'type': 6},{'expression': '\"Y_F_21\"','length': 0,'name': 'Y_F_21','precision': 0,'type': 6},{'expression': '\"Y_F_22\"','length': 0,'name': 'Y_F_22','precision': 0,'type': 6},{'expression': '\"Y_F_23\"','length': 0,'name': 'Y_F_23','precision': 0,'type': 6},{'expression': '\"Y_F_24\"','length': 0,'name': 'Y_F_24','precision': 0,'type': 6},{'expression': '\"Y_F_25\"','length': 0,'name': 'Y_F_25','precision': 0,'type': 6},{'expression': '\"Y_F_26\"','length': 0,'name': 'Y_F_26','precision': 0,'type': 6},{'expression': '\"Y_F_27\"','length': 0,'name': 'Y_F_27','precision': 0,'type': 6},{'expression': '\"Y_F_28\"','length': 0,'name': 'Y_F_28','precision': 0,'type': 6},{'expression': '\"Y_F_29\"','length': 0,'name': 'Y_F_29','precision': 0,'type': 6},{'expression': '\"Y_T_0\"','length': 0,'name': 'Y_T_0','precision': 0,'type': 6},{'expression': '\"Y_T_1\"','length': 0,'name': 'Y_T_1','precision': 0,'type': 6},{'expression': '\"Y_T_2\"','length': 0,'name': 'Y_T_2','precision': 0,'type': 6},{'expression': '\"Y_T_3\"','length': 0,'name': 'Y_T_3','precision': 0,'type': 6},{'expression': '\"Y_T_4\"','length': 0,'name': 'Y_T_4','precision': 0,'type': 6},{'expression': '\"Y_T_5\"','length': 0,'name': 'Y_T_5','precision': 0,'type': 6},{'expression': '\"Y_T_6\"','length': 0,'name': 'Y_T_6','precision': 0,'type': 6},{'expression': '\"Y_T_7\"','length': 0,'name': 'Y_T_7','precision': 0,'type': 6},{'expression': '\"Y_T_8\"','length': 0,'name': 'Y_T_8','precision': 0,'type': 6},{'expression': '\"Y_T_9\"','length': 0,'name': 'Y_T_9','precision': 0,'type': 6},{'expression': '\"Y_T_10\"','length': 0,'name': 'Y_T_10','precision': 0,'type': 6},{'expression': '\"Y_T_11\"','length': 0,'name': 'Y_T_11','precision': 0,'type': 6},{'expression': '\"Y_T_12\"','length': 0,'name': 'Y_T_12','precision': 0,'type': 6},{'expression': '\"Y_T_13\"','length': 0,'name': 'Y_T_13','precision': 0,'type': 6},{'expression': '\"Y_T_14\"','length': 0,'name': 'Y_T_14','precision': 0,'type': 6},{'expression': '\"Y_T_15\"','length': 0,'name': 'Y_T_15','precision': 0,'type': 6},{'expression': '\"Y_T_16\"','length': 0,'name': 'Y_T_16','precision': 0,'type': 6},{'expression': '\"Y_T_17\"','length': 0,'name': 'Y_T_17','precision': 0,'type': 6},{'expression': '\"Y_T_18\"','length': 0,'name': 'Y_T_18','precision': 0,'type': 6},{'expression': '\"Y_T_19\"','length': 0,'name': 'Y_T_19','precision': 0,'type': 6},{'expression': '\"Y_T_20\"','length': 0,'name': 'Y_T_20','precision': 0,'type': 6},{'expression': '\"Y_T_21\"','length': 0,'name': 'Y_T_21','precision': 0,'type': 6},{'expression': '\"Y_T_22\"','length': 0,'name': 'Y_T_22','precision': 0,'type': 6},{'expression': '\"Y_T_23\"','length': 0,'name': 'Y_T_23','precision': 0,'type': 6},{'expression': '\"Y_T_24\"','length': 0,'name': 'Y_T_24','precision': 0,'type': 6},{'expression': '\"Y_T_25\"','length': 0,'name': 'Y_T_25','precision': 0,'type': 6},{'expression': '\"Y_T_26\"','length': 0,'name': 'Y_T_26','precision': 0,'type': 6},{'expression': '\"Y_T_27\"','length': 0,'name': 'Y_T_27','precision': 0,'type': 6},{'expression': '\"Y_T_28\"','length': 0,'name': 'Y_T_28','precision': 0,'type': 6},{'expression': '\"Y_T_29\"','length': 0,'name': 'Y_T_29','precision': 0,'type': 6},{'expression': 'eval(array_to_string(array_foreach(generate_series( @Preprimarystartingage ,  @Preprimarystartingage + @Preprimaryduration - 1),concat(\'\"Y_F_\',@element,\'\"\')),\'+\'))','length': 0,'name': 'Pre_primary_F','precision': 0,'type': 6},{'expression': 'eval(array_to_string(array_foreach(generate_series( @Preprimarystartingage ,  @Preprimarystartingage + @Preprimaryduration - 1),concat(\'\"Y_M_\',@element,\'\"\')),\'+\'))','length': 0,'name': 'Pre_primary_M','precision': 0,'type': 6},{'expression': 'eval(array_to_string(array_foreach(generate_series( @Preprimarystartingage ,  @Preprimarystartingage + @Preprimaryduration - 1),concat(\'\"Y_T_\',@element,\'\"\')),\'+\'))','length': 0,'name': 'Pre_primary_T','precision': 0,'type': 6},{'expression': 'eval(array_to_string(array_foreach(generate_series(  @Primarystartingage  ,   @Primarystartingage  +  @Primaryduration  - 1),concat(\'\"Y_F_\',@element,\'\"\')),\'+\'))','length': 0,'name': 'Primary_F','precision': 0,'type': 6},{'expression': 'eval(array_to_string(array_foreach(generate_series( @Primarystartingage ,  @Primarystartingage + @Primaryduration - 1),concat(\'\"Y_M_\',@element,\'\"\')),\'+\'))','length': 0,'name': 'Primary_M','precision': 0,'type': 6},{'expression': 'eval(array_to_string(array_foreach(generate_series( @Primarystartingage ,  @Primarystartingage + @Primaryduration - 1),concat(\'\"Y_T_\',@element,\'\"\')),\'+\'))','length': 0,'name': 'Primary_T','precision': 0,'type': 6},{'expression': 'eval(array_to_string(array_foreach(generate_series(  @Lowersecondarystartingage  ,   @Lowersecondarystartingage + @Lowersecondaryduration  - 1),concat(\'\"Y_F_\',@element,\'\"\')),\'+\'))','length': 0,'name': 'LowSec_F','precision': 0,'type': 6},{'expression': 'eval(array_to_string(array_foreach(generate_series(  @Lowersecondarystartingage  ,   @Lowersecondarystartingage + @Lowersecondaryduration  - 1),concat(\'\"Y_M_\',@element,\'\"\')),\'+\'))','length': 0,'name': 'LowSec_M','precision': 0,'type': 6},{'expression': 'eval(array_to_string(array_foreach(generate_series(  @Lowersecondarystartingage  ,   @Lowersecondarystartingage + @Lowersecondaryduration  - 1),concat(\'\"Y_T_\',@element,\'\"\')),\'+\'))','length': 0,'name': 'LowSec_T','precision': 0,'type': 6},{'expression': 'eval(array_to_string(array_foreach(generate_series(   @Uppersecondarystartingage   ,    @Uppersecondarystartingage + @Uppersecondaryduration   - 1),concat(\'\"Y_F_\',@element,\'\"\')),\'+\'))','length': 0,'name': 'UppSec_F','precision': 0,'type': 6},{'expression': 'eval(array_to_string(array_foreach(generate_series(   @Uppersecondarystartingage   ,    @Uppersecondarystartingage + @Uppersecondaryduration   - 1),concat(\'\"Y_M_\',@element,\'\"\')),\'+\'))','length': 0,'name': 'UppSec_M','precision': 0,'type': 6},{'expression': 'eval(array_to_string(array_foreach(generate_series(   @Uppersecondarystartingage   ,    @Uppersecondarystartingage + @Uppersecondaryduration   - 1),concat(\'\"Y_T_\',@element,\'\"\')),\'+\'))','length': 0,'name': 'UppSec_T','precision': 0,'type': 6}],
            'INPUT': outputs['ReorganizingTheResults']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculatingSchoolAgesWithLowerAndUpperSecondary'] = processing.run('native:refactorfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(34)
        if feedback.isCanceled():
            return {}

        # Creating the file shapefile (Secondary)
        alg_params = {
            'DISCARD_NONMATCHING': True,
            'INPUT': parameters['Administrativeboundaries'],
            'JOIN': outputs['CreateSpatialIndexForSecondary']['OUTPUT'],
            'JOIN_FIELDS': [''],
            'METHOD': 1,
            'PREDICATE': [2],
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CreatingTheFileShapefileSecondary'] = processing.run('native:joinattributesbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(35)
        if feedback.isCanceled():
            return {}

        # Create spatial index for administrative boundaries
        alg_params = {
            'INPUT': parameters['Administrativeboundaries']
        }
        outputs['CreateSpatialIndexForAdministrativeBoundaries'] = processing.run('native:createspatialindex', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(36)
        if feedback.isCanceled():
            return {}

        # Creating the file shapefile
        alg_params = {
            'DISCARD_NONMATCHING': True,
            'INPUT': outputs['CreateSpatialIndexForAdministrativeBoundaries']['OUTPUT'],
            'JOIN': outputs['ReorganizingTheResults']['OUTPUT'],
            'JOIN_FIELDS': [''],
            'METHOD': 1,
            'PREDICATE': [2],
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CreatingTheFileShapefile'] = processing.run('native:joinattributesbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(37)
        if feedback.isCanceled():
            return {}

        # Drop field(s)
        alg_params = {
            'COLUMN': ['fid'],
            'INPUT': outputs['CreatingTheFileShapefileSecondary']['OUTPUT'],
            'OUTPUT': parameters['ResultsWithSecondary']
        }
        outputs['DropFields'] = processing.run('qgis:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['ResultsWithSecondary'] = outputs['DropFields']['OUTPUT']

        feedback.setCurrentStep(38)
        if feedback.isCanceled():
            return {}

        # Create spatial index for Lower and Upper secondary
        alg_params = {
            'INPUT': outputs['CalculatingSchoolAgesWithLowerAndUpperSecondary']['OUTPUT']
        }
        outputs['CreateSpatialIndexForLowerAndUpperSecondary'] = processing.run('native:createspatialindex', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(39)
        if feedback.isCanceled():
            return {}

        # Creating the file shapefile (Lower and Upper secondary)
        alg_params = {
            'DISCARD_NONMATCHING': True,
            'INPUT': parameters['Administrativeboundaries'],
            'JOIN': outputs['CreateSpatialIndexForLowerAndUpperSecondary']['OUTPUT'],
            'JOIN_FIELDS': [''],
            'METHOD': 1,
            'PREDICATE': [2],
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CreatingTheFileShapefileLowerAndUpperSecondary'] = processing.run('native:joinattributesbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(40)
        if feedback.isCanceled():
            return {}

        # Exporting the results to Excel
        alg_params = {
            'DATASOURCE_OPTIONS': '',
            'INPUT': outputs['CreatingTheFileShapefileSecondary']['OUTPUT'],
            'LAYER_NAME': '',
            'LAYER_OPTIONS': '',
            'OUTPUT': QgsExpression('@Foldercontainingtherasterfiles || \'/\' || \'Population_estimates_\' ||  lower(@ISOcountrycode)  || to_string( @Year ) || \'SchoolAge\' || \'.xlsx\'').evaluate(),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExportingTheResultsToExcel'] = processing.run('native:savefeatures', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(41)
        if feedback.isCanceled():
            return {}

        # Drop field(s)
        alg_params = {
            'COLUMN': ['fid'],
            'INPUT': outputs['CreatingTheFileShapefile']['OUTPUT'],
            'OUTPUT': parameters['Results']
        }
        outputs['DropFields'] = processing.run('qgis:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Results'] = outputs['DropFields']['OUTPUT']

        feedback.setCurrentStep(42)
        if feedback.isCanceled():
            return {}

        # Drop field(s)
        alg_params = {
            'COLUMN': ['fid'],
            'INPUT': outputs['CreatingTheFileShapefileLowerAndUpperSecondary']['OUTPUT'],
            'OUTPUT': parameters['ResultsWithLowerAndUpperSecondary']
        }
        outputs['DropFields'] = processing.run('qgis:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['ResultsWithLowerAndUpperSecondary'] = outputs['DropFields']['OUTPUT']

        feedback.setCurrentStep(43)
        if feedback.isCanceled():
            return {}

        # Exporting the results to Excel
        alg_params = {
            'DATASOURCE_OPTIONS': '',
            'INPUT': outputs['CreatingTheFileShapefileLowerAndUpperSecondary']['OUTPUT'],
            'LAYER_NAME': '',
            'LAYER_OPTIONS': '',
            'OUTPUT': QgsExpression('@Foldercontainingtherasterfiles || \'/\' || \'Population_estimates_\' ||  lower(@ISOcountrycode)  || to_string( @Year ) || \'SchoolAge\' || \'.xlsx\'').evaluate(),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExportingTheResultsToExcel'] = processing.run('native:savefeatures', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(44)
        if feedback.isCanceled():
            return {}

        # Exporting the results to Excel
        alg_params = {
            'DATASOURCE_OPTIONS': '',
            'INPUT': outputs['CreatingTheFileShapefile']['OUTPUT'],
            'LAYER_NAME': '',
            'LAYER_OPTIONS': '',
            'OUTPUT': QgsExpression('@Foldercontainingtherasterfiles || \'/\' || \'Population_estimates_\' ||  upper(@ISOcountrycode) || \'_\'  || to_string( @Year ) || \'.xlsx\'').evaluate(),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExportingTheResultsToExcel'] = processing.run('native:savefeatures', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        return results

    def name(self):
        return 'Sprague multipliers'

    def displayName(self):
        return 'Sprague multipliers'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def shortHelpString(self):
        return """<html><body><h2>Algorithm description</h2>
<p>This algorithm aims at creating single years of age for any level of administrative boundaries or any other polygon layer, based on clustered 5-year age group raster files, by applying Sprague multipliers. It also allows the user to reconstruct the different school age groups for a particular country, regardless of whether the system divides lower and upper secondary or not. </p>
<h2>Input parameters</h2>
<h3>Folder containing the raster files</h3>
<p>Select the folder containing the raster files with the 5-year age groups.</p>
<h3>Administrative boundaries</h3>
<p>Polygon layer containing the administrative boundaries on which the single years of age' variables will be calculated. It can also be any other arrangement (e.g. Voronoi polygons).</p>
<h3>ISO country code</h3>
<p>3-letter ISO country code</p>
<h3>Year</h3>
<p>Year of analysis (e.g. 2014)</p>
<h3>Use constrained population estimates</h3>
<p></p>
<h3>Use UN adjusted constrained estimates</h3>
<p></p>
<h3>Create custom school age groups</h3>
<p>Select to create custom school age groups for the country or region.</p>
<h3>Pre-primary starting age</h3>
<p>This must be a number.</p>
<h3>Pre-primary duration</h3>
<p>This must be a number.</p>
<h3>Primary starting age</h3>
<p>This must be a number.</p>
<h3>Primary duration</h3>
<p>This must be a number.</p>
<h3>System divided in Lower and Upper secondary</h3>
<p>Select if the education system is divided in Lower and Upper Secondary.</p>
<h3>Lower secondary starting age</h3>
<p>This must be a number.</p>
<h3>Lower secondary duration</h3>
<p>This must be a number.</p>
<h3>Upper secondary starting age</h3>
<p>This must be a number.</p>
<h3>Upper secondary duration</h3>
<p>This must be a number.</p>
<h3>Secondary starting age</h3>
<p>This must be a number.</p>
<h3>Secondary duration</h3>
<p>This must be a number.</p>
<h3>Results</h3>
<p>This will only be calculated if the option to create custom school age groups is not selected. It will contain the same information as the Administrative boundaries' polygon layer, plus additional columns for the single years of age by sex.</p>
<h3>Results with Lower and Upper secondary</h3>
<p>This will only be created if the option to create custom school age groups and to make a distinction between Lower and Upper secondary is selected. It will create, in addition to the single year of age columns, additional columns by sex for each educational level. </p>
<h3>Results with Secondary</h3>
<p>This will only be created if the option to create custom school age groups is selected and the option to make a distinction between Lower and Upper secondary is unselected. It will create, in addition to the single year of age columns, additional columns by sex for each educational level. </p>
<h3>Verbose logging</h3>
<p></p>
<h2>Outputs</h2>
<h3>Results</h3>
<p>This will only be calculated if the option to create custom school age groups is not selected. It will contain the same information as the Administrative boundaries' polygon layer, plus additional columns for the single years of age by sex.</p>
<h3>Results with Lower and Upper secondary</h3>
<p>This will only be created if the option to create custom school age groups and to make a distinction between Lower and Upper secondary is selected. It will create, in addition to the single year of age columns, additional columns by sex for each educational level. </p>
<h3>Results with Secondary</h3>
<p>This will only be created if the option to create custom school age groups is selected and the option to make a distinction between Lower and Upper secondary is unselected. It will create, in addition to the single year of age columns, additional columns by sex for each educational level. </p>
<br><p align="right">Algorithm author: Development unit, IIEP-UNESCO (development@iiep.unesco.org)
The designations employed and the presentation of the material in this publication do not imply the expression of any opinion whatsoever on the part of UNESCO or IIEP concerning the legal status of any country, territory, city or area, or of its authorities, or concerning the delimitation of its frontiers or boundaries. 
This material has been partly funded by UK aid from the UK government; however the views expressed do not necessarily reflect the UK government’s official policies.</p><p align="right">Help author: Development unit, IIEP-UNESCO (development@iiep.unesco.org)</p><p align="right">Algorithm version: 1.0</p></body></html>"""

    def createInstance(self):
        return SpragueMultipliers()
