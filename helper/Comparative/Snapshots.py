import logging
import os
import pathlib
import time
import cv2


class Snapshot:

    def validateSnapshots(context, ruta):
        """
        Si no existe un snapshot previo crea uno.
        Si existe un snapshot previo, obtiene un nuevo registro y lo compara al anterior
        :param ruta: en formato carpeta(s)/imagen (se usa / independiente del S.O.)
        :return:
        """
        try:
            ruta = ruta.replace('/', os.sep)
            snapshot_path = os.path.join(Snapshot.getRutaSnaps(), ruta + ".png")
            temp_snapshot_path = os.path.join(Snapshot.getRutaSnapsTemp(), ruta + ".png")

            if os.path.exists(snapshot_path):
                print("Existe un archivo original")
                Snapshot.save_snapshot(context, temp_snapshot_path)
                validator = Snapshot.compare_snapshots(context, snapshot_path, temp_snapshot_path)
                return validator
            else:
                print("No Existe, se creará un original")
                Snapshot.save_snapshot(context, snapshot_path)
                return True
        except Exception as ex:
            print("Se ha producido una excepción en el método validateSnapshots: %s", ex)

    def save_snapshot(context, rute_snap):
        """
        Guarda un snapshot a pantalla completa
        :param rute_snap: Ruta donde se guardará el snapshot.
        :return:
        """
        try:
            time.sleep(3)
            height, width = Snapshot.scroll_down(context)
            context.browser.set_window_size(width, height)

            # Crear el directorio si no existe
            directorio = Snapshot.retornaSoloRuta(rute_snap)
            if not os.path.exists(str(directorio)):
                print("Se crea el directorio para guardar el screen")
                os.makedirs(str(directorio))

            # Capturar la pantalla y guardar el snapshot
            screenshot_path = rute_snap
            context.browser.save_screenshot(screenshot_path)
            print("Se guarda la imagen en: ", screenshot_path)
        except Exception as ex:
            logging.info("Error al guardar el snapshot:", ex)

    def compare_snapshots(context, original_snap, last_screen_snap):
        """
        Compara dos imagenes, se debe establecer el umbral_maximo de diferencias (desde donde se considera una diferencia critica)
        :param original_snap: Ruta del snapshot original
        :param last_screen_snap: Ruta del snapshot actual
        :return:
        """
        try:
            umbral_maximo = 500  #representa la tolerancia maxima de pixeles diferentes entre los canales RGB
            original = cv2.imread(original_snap)
            last_screen = cv2.imread(last_screen_snap)
            """compara tamaños y capas"""
            if original.shape == last_screen.shape:
                print('Las imagenes tiene el mismo tamaño y canal')
                difference = cv2.subtract(original, last_screen)
                b, g, r = cv2.split(difference)
                # print("Valor de B ",cv2.countNonZero(b))

                if cv2.countNonZero(b) < umbral_maximo or cv2.countNonZero(g) < umbral_maximo or cv2.countNonZero(
                        r) < umbral_maximo:
                    os.remove(last_screen_snap)  #Si las imagenes son iguales elimina la temporal de inmediato
                    return True
                else:
                    return False
            else:
                print('Las imagenes no se pueden comparar')
                return False
        except Exception as ex:
            print("Error al comparar los snapshots:", ex)

    def scroll_down(context):
        """
        Toma el tamaño completo de la pantalla incluyendo un posible scroll
        :return:
        """
        total_width = context.browser.execute_script("return document.body.offsetWidth")
        total_height = context.browser.execute_script("return document.body.parentNode.scrollHeight")
        viewport_width = context.browser.execute_script("return document.body.clientWidth")
        viewport_height = context.browser.execute_script("return window.innerHeight")
        rectangles = []
        i = 0
        while i < total_height:
            ii = 0
            top_height = i + viewport_height

            if top_height > total_height:
                top_height = total_height

            while ii < total_width:
                top_width = ii + viewport_width
                if top_width > total_width:
                    top_width = total_width
                rectangles.append((ii, i, top_width, top_height))
                ii = ii + viewport_width
            i = i + viewport_height
        previous = None

        for rectangle in rectangles:
            if not previous is None:
                context.browser.execute_script("window.scrollTo({0}, {1})".format(rectangle[0], rectangle[1]))
                time.sleep(3)
        return total_height, total_width

    def retornaSoloRuta(ruta):
        """
        Toma una ruta en formato "carpeta/archivo" y retorna solo "carpeta/"
        ej: carpeta/carpeta/archivo  retorna carpeta/carpeta
        La ruta ya debe venir con el os.sep correcto
        :return:
        """
        resultado = ruta.split(os.sep)
        onlyURI = ""
        for i in range(len(resultado) - 1):
            onlyURI = onlyURI + resultado[i] + os.sep
        return onlyURI

    def getRutaSnaps():
        URI = str(pathlib.Path().absolute())
        return URI + os.sep + 'timeMachine' + os.sep + 'snapshot' + os.sep

    def getRutaSnapsTemp():
        URI = str(pathlib.Path().absolute())
        return URI + os.sep + 'timeMachine' + os.sep + 'snapshot_temp' + os.sep
