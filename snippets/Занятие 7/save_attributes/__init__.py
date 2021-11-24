from .save_attributes import SaveAttributesPlugin

# Обязателен для загрузки плагина
def classFactory(iface):
    return SaveAttributesPlugin(iface)