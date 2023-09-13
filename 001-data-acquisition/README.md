# 001 - Adquisición de datos

Un osciloscopio GW Instek GDS-3354 (Firmware V1.10) es utilizado para obtener grandes cantidades de muestras en cada canal con el fin de obtener datos como los máximos picos.

La librería [gds_3354](/001-data-acquisition/gds_3354.py) está diseñada para correr en Python 3.6.8, ya que es la utilizada en la computadora dedicada al laboratorio y a la que se conectó el osciloscopio por USB.

Los datos son adquiridos por serial en formato LSF. Existe una diferencia en los 50.000 bytes de datos binarios al adquirirlos por serial y al guardarlos en un archivo en la memoria interna o un USB. Esta diferencia es compensada con el método de clase `convert_hex`. La operación a realizar sobre los datos en binario recibidos por serial para obtener los datos reales es:

1. Tomar de a 2 bytes, con el bit más significativo a la izquierda.
2. Desplazar a la izquierda 8 bits (o multiplicar por 256 y tomar los 16 bits menos significativos).
3. Sumar un offset, que para una posición vertical de 0V en el osciloscopio corresponde a `32768` o `0x8000`. Para vpos = -840mV corresponde a `22016` o `0x5600`

El programa [test_connection](/001-data-acquisition/test_connection.py) está pensado para ejecutarse línea por línea en la terminal interactiva.

El programa [save_waveforms](/001-data-acquisition/save_waveforms.py) al ejecutarse almacena las tandas de tomas de datos en carpetas separadas, y guarda un log del proceso en un archivo.
