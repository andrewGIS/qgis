from qgis.processing import alg


@alg(name='save_attributes', label='Сохраняем аттрибуты объекты в CSV',
     group='', group_label='')
@alg.input(type=alg.SOURCE, name='INPUT', label='Входной слой')
@alg.input(type=alg.FILE_DEST, name='OUTPUT', label='Выходной слой')
def processAlgorithm(instance, parameters, context, feedback, inputs):
    """Сохраняем аттрибуты объекты в CSV"""
    source = instance.parameterAsSource(parameters, 'INPUT', context)
    csv = instance.parameterAsFileOutput(parameters, 'OUTPUT', context)

    fieldnames = [field.name() for field in source.fields()]

    # Вычисляем данные для прогресс бара
    total = 100.0 / source.featureCount() if source.featureCount() else 0
    features = source.getFeatures()

    with open(csv, 'w') as output_file:
        # Заголовки полей
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

    return {'OUTPUT': csv}
