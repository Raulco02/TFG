import os
import xml.etree.ElementTree as ET
from xml.dom import minidom

class EscritorXML:
    def verificar_y_crear_xml(self, id, nombre, topic, integracion, ubicacion):
        directorio = "./Dispositivos"
        archivo = "dispositivos.xml"
        ruta_completa = os.path.join(directorio, archivo)

        root = None
        if os.path.exists(ruta_completa):
            # El archivo existe, lo cargamos
            tree = ET.parse(ruta_completa)
            root = tree.getroot()

            # Verificar si el dispositivo ya existe en el archivo
            dispositivos = root.findall(".//dispositivo")
            dispositivo_existente = False
            for dispositivo in dispositivos:
                id_dispositivo = dispositivo.find("id").text
                nombre_dispositivo = dispositivo.find("nombre").text
                if id_dispositivo == id or nombre_dispositivo == nombre:
                    dispositivo_existente = True
                    break

            if not dispositivo_existente:
                # El dispositivo no está en el archivo, así que lo añadimos
                dispositivo = ET.SubElement(root, "dispositivo")
                ET.SubElement(dispositivo, "id").text = id
                ET.SubElement(dispositivo, "nombre").text = nombre
                ET.SubElement(dispositivo, "tipo").text = 'sensor' if integracion["tipo_dispositivo"] == 's' else 'actuador'
                ET.SubElement(dispositivo, "topic").text = topic
                ET.SubElement(dispositivo, "ubicacion").text = ubicacion
                for atributo in integracion["atributos"]:
                    atributo_elem = ET.SubElement(dispositivo, "atributo")
                    ET.SubElement(atributo_elem, "nombre").text = atributo["nombre"]
                    ET.SubElement(atributo_elem, "unidad").text = atributo["unidades"]
                    ET.SubElement(atributo_elem, "actuable").text = str(atributo["actuable"]).lower()
                    if str(atributo["actuable"]).lower() == "true":
                        ET.SubElement(atributo_elem, "topic").text = atributo["topic"]
                        ET.SubElement(atributo_elem, "plantilla").text = atributo["plantilla"]
                ET.SubElement(dispositivo, "script").text = integracion["script"]

                self.write_pretty_xml(tree, ruta_completa)
                print(f"Dispositivo agregado al archivo {archivo}")
            else:
                print("El dispositivo ya existe en el archivo.")
        else:
            # El archivo no existe, así que lo creamos
            root = ET.Element("dispositivos")
            dispositivo = ET.SubElement(root, "dispositivo")
            ET.SubElement(dispositivo, "id").text = id
            ET.SubElement(dispositivo, "nombre").text = nombre
            ET.SubElement(dispositivo, "tipo").text = 'sensor' if integracion["tipo_dispositivo"] == 's' else 'actuador'
            ET.SubElement(dispositivo, "topic").text = topic
            for atributo in integracion["atributos"]:
                atributo_elem = ET.SubElement(dispositivo, "atributo")
                ET.SubElement(atributo_elem, "nombre").text = atributo["nombre"]
                ET.SubElement(atributo_elem, "unidad").text = atributo["unidades"]
                ET.SubElement(atributo_elem, "actuable").text = str(atributo["actuable"]).lower()
            ET.SubElement(dispositivo, "script").text = integracion["script"]

            tree = ET.ElementTree(root)
            self.write_pretty_xml(tree, ruta_completa)
            print(f"Archivo {archivo} creado con éxito en {directorio}")

    def write_pretty_xml(self, tree, file_path):
        # Convertir el ElementTree a una cadena de bytes
        xml_bytes = ET.tostring(tree.getroot(), encoding='utf-8')
        # Parsear la cadena de bytes con minidom
        parsed_xml = minidom.parseString(xml_bytes)
        # Crear una cadena con formato legible
        pretty_xml_lines = parsed_xml.toprettyxml(indent="    ").splitlines()

        # Filtrar líneas vacías o que contienen solo espacios en blanco
        pretty_xml_lines = [line for line in pretty_xml_lines if line.strip()]

        # Escribir las líneas en el archivo
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(pretty_xml_lines))

    def editar_xml(self, prev_id, id, nombre, topic, integracion):
        directorio = "./Dispositivos"
        archivo = "dispositivos.xml"
        ruta_completa = os.path.join(directorio, archivo)

        root = None
        if os.path.exists(ruta_completa):
            # El archivo existe, lo cargamos
            tree = ET.parse(ruta_completa)
            root = tree.getroot()

            # Verificar si el dispositivo ya existe en el archivo
            dispositivos = root.findall(".//dispositivo")
            dispositivo_existente = False
            for dispositivo in dispositivos:
                id_dispositivo = dispositivo.find("id").text
                if id_dispositivo == prev_id:
                    dispositivo_existente = True
                    break

            if not dispositivo_existente:
                raise ValueError("El dispositivo no existe en el archivo 'Dispositivos.xml'.")
            else:
                # El dispositivo está en el archivo, así que lo editamos
                for dispositivo in dispositivos:
                    id_dispositivo = dispositivo.find("id").text
                    if id_dispositivo == prev_id:
                        dispositivo.find("id").text = id
                        dispositivo.find("nombre").text = nombre
                        dispositivo.find("topic").text = topic
                        for atributo in dispositivo.findall("atributo"):
                            dispositivo.remove(atributo)
                        for atributo in integracion["atributos"]:
                            atributo_elem = ET.SubElement(dispositivo, "atributo")
                            ET.SubElement(atributo_elem, "nombre").text = atributo["nombre"]
                            ET.SubElement(atributo_elem, "unidad").text = atributo["unidades"]
                            ET.SubElement(atributo_elem, "actuable").text = str(atributo["actuable"]).lower()
                            if str(atributo["actuable"]).lower() == "true":
                                ET.SubElement(atributo_elem, "topic").text = atributo["topic"]
                                ET.SubElement(atributo_elem, "plantilla").text = atributo["plantilla"]
                        ET.SubElement(dispositivo, "script").text = integracion["script"]

                self.write_pretty_xml(tree, ruta_completa)
                print(f"Dispositivo editado en el archivo {archivo}")
