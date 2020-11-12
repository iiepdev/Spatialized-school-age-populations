"""
Model exported as python.
Name : Sprague multipliers - Model
Group : 
With QGIS : 31400
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterRasterLayer
from qgis.core import QgsProcessingParameterVectorLayer
import processing


class SpragueMultipliersModel(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterRasterLayer('Female0to1yearsold', 'Female - 0 to 1 years old', defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterLayer('Female1to4yearsold', 'Female - 1 to 4 years old', defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterLayer('Female5to9yearsold', 'Female - 5 to 9 years old', defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterLayer('Female10to14yearsold', 'Female - 10 to 14 years old', defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterLayer('Female15to19yearsold', 'Female - 15 to 19 years old', defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterLayer('Female20to24yearsold', 'Female - 20 to 24 years old', defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterLayer('Female25to29yearsold', 'Female - 25 to 29 years old', defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterLayer('Female30to34yearsold', 'Female - 30 to 34 years old', defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterLayer('Female35to39yearsold', 'Female - 35 to 39 years old', defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterLayer('Male0to1yearsold', 'Male - 0 to 1 years old', defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterLayer('Male1to4yearsold', 'Male - 1 to 4 years old', defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterLayer('Male5to9yearsold', 'Male - 5 to 9 years old', defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterLayer('Male10to14yearsold', 'Male - 10 to 14 years old', defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterLayer('Male15to19yearsold', 'Male - 15 to 19 years old', defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterLayer('Male20to24yearsold', 'Male - 20 to 24 years old', defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterLayer('Male25to29yearsold', 'Male - 25 to 29 years old', defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterLayer('Male30to34yearsold', 'Male - 30 to 34 years old', defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterLayer('Male35to39yearsold', 'Male - 35 to 39 years old', defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('Smallestadministrativeboundary', 'Smallest administrative boundary', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(18, model_feedback)
        results = {}
        outputs = {}

        # Female - 0 to 1 years old - Zonal statistics
        alg_params = {
            'COLUMN_PREFIX': 'F_0_to_1',
            'INPUT_RASTER': parameters['Female0to1yearsold'],
            'INPUT_VECTOR': parameters['Smallestadministrativeboundary'],
            'RASTER_BAND': 1,
            'STATISTICS': [1]
        }
        outputs['Female0To1YearsOldZonalStatistics'] = processing.run('native:zonalstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Female - 1 to 4 years old - Zonal statistics
        alg_params = {
            'COLUMN_PREFIX': 'F_1_to_4',
            'INPUT_RASTER': parameters['Female1to4yearsold'],
            'INPUT_VECTOR': parameters['Smallestadministrativeboundary'],
            'RASTER_BAND': 1,
            'STATISTICS': [1]
        }
        outputs['Female1To4YearsOldZonalStatistics'] = processing.run('native:zonalstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Female - 5 to 9 years old - Zonal statistics
        alg_params = {
            'COLUMN_PREFIX': 'F_5_to_9',
            'INPUT_RASTER': parameters['Female5to9yearsold'],
            'INPUT_VECTOR': parameters['Smallestadministrativeboundary'],
            'RASTER_BAND': 1,
            'STATISTICS': [1]
        }
        outputs['Female5To9YearsOldZonalStatistics'] = processing.run('native:zonalstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Female - 10 to 14 years old - Zonal statistics
        alg_params = {
            'COLUMN_PREFIX': 'F_10_to_14',
            'INPUT_RASTER': parameters['Female10to14yearsold'],
            'INPUT_VECTOR': parameters['Smallestadministrativeboundary'],
            'RASTER_BAND': 1,
            'STATISTICS': [1]
        }
        outputs['Female10To14YearsOldZonalStatistics'] = processing.run('native:zonalstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # Female - 15 to 19 years old - Zonal statistics
        alg_params = {
            'COLUMN_PREFIX': 'F_15_to_19',
            'INPUT_RASTER': parameters['Female15to19yearsold'],
            'INPUT_VECTOR': parameters['Smallestadministrativeboundary'],
            'RASTER_BAND': 1,
            'STATISTICS': [1]
        }
        outputs['Female15To19YearsOldZonalStatistics'] = processing.run('native:zonalstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # Female - 20 to 24 years old - Zonal statistics
        alg_params = {
            'COLUMN_PREFIX': 'F_20_to_24',
            'INPUT_RASTER': parameters['Female20to24yearsold'],
            'INPUT_VECTOR': parameters['Smallestadministrativeboundary'],
            'RASTER_BAND': 1,
            'STATISTICS': [1]
        }
        outputs['Female20To24YearsOldZonalStatistics'] = processing.run('native:zonalstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        # Female - 25 to 29 years old - Zonal statistics
        alg_params = {
            'COLUMN_PREFIX': 'F_25_to_29',
            'INPUT_RASTER': parameters['Female25to29yearsold'],
            'INPUT_VECTOR': parameters['Smallestadministrativeboundary'],
            'RASTER_BAND': 1,
            'STATISTICS': [1]
        }
        outputs['Female25To29YearsOldZonalStatistics'] = processing.run('native:zonalstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(7)
        if feedback.isCanceled():
            return {}

        # Female - 30 to 34 years old - Zonal statistics
        alg_params = {
            'COLUMN_PREFIX': 'F_30_to_34',
            'INPUT_RASTER': parameters['Female30to34yearsold'],
            'INPUT_VECTOR': parameters['Smallestadministrativeboundary'],
            'RASTER_BAND': 1,
            'STATISTICS': [1]
        }
        outputs['Female30To34YearsOldZonalStatistics'] = processing.run('native:zonalstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(8)
        if feedback.isCanceled():
            return {}

        # Female - 35 to 39 years old - Zonal statistics
        alg_params = {
            'COLUMN_PREFIX': 'F_35_to_39',
            'INPUT_RASTER': parameters['Female35to39yearsold'],
            'INPUT_VECTOR': parameters['Smallestadministrativeboundary'],
            'RASTER_BAND': 1,
            'STATISTICS': [1]
        }
        outputs['Female35To39YearsOldZonalStatistics'] = processing.run('native:zonalstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(9)
        if feedback.isCanceled():
            return {}

        # Male - 0 to 1 years old - Zonal statistics
        alg_params = {
            'COLUMN_PREFIX': 'M_0_to_1',
            'INPUT_RASTER': parameters['Male0to1yearsold'],
            'INPUT_VECTOR': parameters['Smallestadministrativeboundary'],
            'RASTER_BAND': 1,
            'STATISTICS': [1]
        }
        outputs['Male0To1YearsOldZonalStatistics'] = processing.run('native:zonalstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(10)
        if feedback.isCanceled():
            return {}

        # Male - 1 to 4 years old - Zonal statistics
        alg_params = {
            'COLUMN_PREFIX': 'M_1_to_4',
            'INPUT_RASTER': parameters['Male1to4yearsold'],
            'INPUT_VECTOR': parameters['Smallestadministrativeboundary'],
            'RASTER_BAND': 1,
            'STATISTICS': [1]
        }
        outputs['Male1To4YearsOldZonalStatistics'] = processing.run('native:zonalstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(11)
        if feedback.isCanceled():
            return {}

        # Male - 5 to 9 years old - Zonal statistics
        alg_params = {
            'COLUMN_PREFIX': 'M_5_to_9',
            'INPUT_RASTER': parameters['Male5to9yearsold'],
            'INPUT_VECTOR': parameters['Smallestadministrativeboundary'],
            'RASTER_BAND': 1,
            'STATISTICS': [1]
        }
        outputs['Male5To9YearsOldZonalStatistics'] = processing.run('native:zonalstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(12)
        if feedback.isCanceled():
            return {}

        # Male - 10 to 14 years old - Zonal statistics
        alg_params = {
            'COLUMN_PREFIX': 'M_10_to_14',
            'INPUT_RASTER': parameters['Male10to14yearsold'],
            'INPUT_VECTOR': parameters['Smallestadministrativeboundary'],
            'RASTER_BAND': 1,
            'STATISTICS': [1]
        }
        outputs['Male10To14YearsOldZonalStatistics'] = processing.run('native:zonalstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(13)
        if feedback.isCanceled():
            return {}

        # Male - 15 to 19 years old - Zonal statistics
        alg_params = {
            'COLUMN_PREFIX': 'M_15_to_19',
            'INPUT_RASTER': parameters['Male15to19yearsold'],
            'INPUT_VECTOR': parameters['Smallestadministrativeboundary'],
            'RASTER_BAND': 1,
            'STATISTICS': [1]
        }
        outputs['Male15To19YearsOldZonalStatistics'] = processing.run('native:zonalstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(14)
        if feedback.isCanceled():
            return {}

        # Male - 20 to 24 years old - Zonal statistics
        alg_params = {
            'COLUMN_PREFIX': 'M_20_to_24',
            'INPUT_RASTER': parameters['Male20to24yearsold'],
            'INPUT_VECTOR': parameters['Smallestadministrativeboundary'],
            'RASTER_BAND': 1,
            'STATISTICS': [1]
        }
        outputs['Male20To24YearsOldZonalStatistics'] = processing.run('native:zonalstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(15)
        if feedback.isCanceled():
            return {}

        # Male - 25 to 29 years old - Zonal statistics
        alg_params = {
            'COLUMN_PREFIX': 'M_25_to_29',
            'INPUT_RASTER': parameters['Male25to29yearsold'],
            'INPUT_VECTOR': parameters['Smallestadministrativeboundary'],
            'RASTER_BAND': 1,
            'STATISTICS': [1]
        }
        outputs['Male25To29YearsOldZonalStatistics'] = processing.run('native:zonalstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(16)
        if feedback.isCanceled():
            return {}

        # Male - 30 to 34 years old
        alg_params = {
            'COLUMN_PREFIX': 'M_30_to_34',
            'INPUT_RASTER': parameters['Male30to34yearsold'],
            'INPUT_VECTOR': parameters['Smallestadministrativeboundary'],
            'RASTER_BAND': 1,
            'STATISTICS': [1]
        }
        outputs['Male30To34YearsOld'] = processing.run('native:zonalstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        feedback.setCurrentStep(17)
        if feedback.isCanceled():
            return {}

        # Male - 35 to 39 years old
        alg_params = {
            'COLUMN_PREFIX': 'M_35_to_39',
            'INPUT_RASTER': parameters['Male35to39yearsold'],
            'INPUT_VECTOR': parameters['Smallestadministrativeboundary'],
            'RASTER_BAND': 1,
            'STATISTICS': [1]
        }
        outputs['Male35To39YearsOld'] = processing.run('native:zonalstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)        
        return results

    def name(self):
        return 'Sprague multipliers - Model'

    def displayName(self):
        return 'Sprague multipliers - Model'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return SpragueMultipliersModel()

