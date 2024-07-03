from App.model.tarjeta import Tarjeta

class tarjetasHelper:
    def generar_lista_tarjetas(tarjetas, tarjeta_dao):
        print(tarjetas)
        tarjeta={}
        tarjetas_lista=[]
        #tarjetas = seccion[4]
        if tarjetas is None:
            tarjetas = []
        for tarj in tarjetas: #Hacer método para comprobaciones de que las tarjetas estén de forma correcta
            if(tarj[1] == 'Estado' or tarj[1] == 'Termostato'):
                print('TUPLA', tarj)
                tarjeta = Tarjeta(tarj[1], tarj[2], tarj[7], tarj[3], tarj[4], tarj[5], tarj[6], tarj[11], tarj[8], tarj[9], tarj[10], tarj[14], tarj[12], tarj[13])
            elif(tarj[1] == 'Grafico'):
                print('TUPLA', tarj)
                print('TARJETA GRAFICO',tarj)
                tarjeta = Tarjeta(tarj[1], tarj[2], tarj[7], tarj[3], tarj[4], tarj[5], tarj[6], tarj[11], tarj[8], tarj[9], tarj[10], tarj[14], tarj[12], tarj[13])
            elif(tarj[1] == 'Grupo'):
                print('TUPLA', tarj)
                i=0
                for t in tarj:
                    print(t,i)
                    i+=1
                tarjeta = Tarjeta(tarj[1], tarj[2], tarj[7], tarj[3], tarj[4], tarj[5], tarj[6], tarj[11], tarj[14], tarj[15], tarj[16], tarj[17], tarj[12], tarj[13], tarj[8][0], tarj[9][0], tarj[10][0])
            else:
                print('Dentro del else')
                tarjeta = Tarjeta(tarj[1], tarj[2], tarj[7], tarj[3], tarj[4], tarj[5], tarj[6])
                print('Despues de crear tarjeta en else')

            print('Tarjeta:', tarjeta.tipo)
            print('Aqui llega')
            print('Tarjeta', tarjeta.tipo, tarjeta.posicion, tarjeta.contenido, tarjeta.imagen, tarjeta.id_dispositivo, tarjeta.id_atributo, tarjeta.tipo_grafico, tarjeta.tiempo_grafico, tarjeta.id_seccion, tarjeta.valor, tarjeta.nombre_atributo, tarjeta.unidades, tarjeta.icono)
            tarjeta_data = tarjeta_dao.obtener_tarjeta_tipo(tarjeta)#{"id": tarj[0], "tipo": tarj[1], "posicion": tarj[2], "dimensiones": tarj[3], "contenido": tarj[4], "imagen": tarj[5], "id-dispositivo": tarj[6], "id-atributo": tarj[7], "tipo-grafico": tarj[8], "tiempo-grafico": tarj[9], "id-seccion": tarj[10]}
            tarjeta_data['id'] = tarj[0]
            print('Tarjeta data:', tarjeta_data)
            tarjetas_lista.append(tarjeta_data)
        print('Tarjetas lista:', tarjetas_lista)
        return tarjetas_lista