from PyQt5.QtCore import QCoreApplication
from qgis.core import (QgsProcessing,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterFileDestination)


# Пример скрипта в тулбоксе
# можно программно положить в
# {profile foler}/processing/scripts/

class SaveAttributesAlgorithm(QgsProcessingAlgorithm):
    """Сохраняем аттрибуты объекты в CSV"""
    OUTPUT = 'OUTPUT'
    INPUT = 'INPUT'

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT,
                self.tr('Input layer'),
                [QgsProcessing.TypeVectorAnyGeometry]
            )
        )

        # Выходной файл в формате CSV
        self.addParameter(
            QgsProcessingParameterFileDestination(
                self.OUTPUT,
                self.tr('Output File'),
                'CSV files (*.csv)',
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        source = self.parameterAsSource(parameters, self.INPUT, context)
        csv = self.parameterAsFileOutput(parameters, self.OUTPUT, context)

        fieldnames = [field.name() for field in source.fields()]

        # Получаем фичи и рассчитываем информацию для прогресс бара
        total = 100.0 / source.featureCount() if source.featureCount() else 0
        features = source.getFeatures()

        with open(csv, 'w') as output_file:
            # Имена полей
            line = ','.join(name for name in fieldnames) + '\n'
            output_file.write(line)
            for current, f in enumerate(features):
                # Выходим из алгоритма если нажали кнопку выход
                if feedback.isCanceled():
                    break

                # Записывает аттрибуты в csv файлик
                line = ','.join(str(f[name]) for name in fieldnames) + '\n'
                output_file.write(line)

                # Обновляем статус прогресс бара
                feedback.setProgress(int(current * total))

        return {self.OUTPUT: csv}

    def name(self):
        return 'save_attributes'

    def displayName(self):
        return self.tr('Сохраняем аттрибуты объекты в CSV')

    def group(self):
        return self.tr(self.groupId())

    def groupId(self):
        return ''

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return SaveAttributesAlgorithm()
