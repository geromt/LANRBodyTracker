# LANRHandTracker

Programa que utiliza una webcam para seguir los movimientos de la 
mano, para después mandar los datos a distintos juegos de neuro-rehabilitación
desarrollados en el [LANR](https://lanr.ifc.unam.mx/index.html).
---
## Dependencias

- python 3.11
- opencv-python=4.8.1.78
- mediapipe=0.10.8
- cvzone=1.6.1
- pyYAML=6.0.1

Se utilizó pyinstaller=6.2.0 para distribuir el programa.

## Ejecutar

```commandline
python3 main.py <path-to-config-file>
```

## Distribución con Pyinstaller

```commandline
 pyinstaller .\LANRHandTracker.spec
```
Si tiene necesidad de generar de nuevo el archivo 
`LANRHandTracker.spec`, es probable que haya
problemas con las dependencias de `mediapipe`. 

Este link resultó util para resolver el problema: 
[Issues compiling mediapipe with pyinstaller on macos](https://stackoverflow.com/questions/67887088/issues-compiling-mediapipe-with-pyinstaller-on-macos).

## Configuración

Para configurar el tracker y su salida se utiliza un archivo de configuracion YAML, se puede encontrar un
ejemplo del mismo en este repositorio.

### Opciones de configuración

Cada una de las siguientes opciones puede aparecer de manera opcional como una llave dentro del diccionario `config`.
Si alguna opción no aparece en el diccionario, se usará su valor por default.

- **camera_index**: *Entero, Default: 0*. Índice de la cámara que utilizará el tracker. Por ahora, no hay manera de 
                    saber qué índice le corresponde a cuál cámara.

- **port**: *Entero, Default: 5052*. Puerto por el que se enviarán los datos de tracker.

- **config_frame**: *Booleano, Default: false*. Indica si se debe modificar el tamaño del frame capturado por la cámara.

- **frame_height**: *Entero, Default: 720*. En caso de que `config_frame` sea `true`, indica la altura del frame.

- **frame_width**: *Entero, Default: 1280*. En caso de que `config_frame` sea `true`, indica el ancho del frame.

- **display_video**: *Booleano, Default: false*. Indica si se debe mostrar la imagen capturada por la cámara. Es
                     recomendable, sólo usar esta opción para hacer pruebas.

- **display_video_size**: *Flotante, Default: 1*. En caso de que `display_video` sea `true`, indica la razón entre la
                           la imagen capturada y la mostrada. Por ejemplo, si `display_video_size` es `0.5`, el alto y ancho
                           de la imagen se reducirá a la mitad.

- **draw_hand**: *Booleano, Default: true*. En caso de que `display_video` sea `true`, indica si se debe dibujar la mano
                 sobre la imagen. Por ahora sólo está disponible si `coordinates` es `"pixel"`.

- **static_mode**: *Booleano, Default: false*. Indica si la detección debe hacerse en cada frame, lo cual es más lento,
                   y sólo se recomienda para detecciones en imágenes o videos.

- **max_hands**: *Entero, Default: 1*. Indica el número máximo de manos que pueden ser detectadas a la vez.

- **model_complexity**: *Entero, Default: 1*. Indica la complejidad del modelo de landmarks. Los valores pueden ser 0 ó 1.
                        En el valor 0, el tracker es más rápido, pero tiene dificultades para encontrar los landmarks en
                        ciertas posiciones de la mano. En el valor 1, la posición de los landmarks es más confiable, pero 
                        el tracker es más lento.

- **min_detection_confidence**: *Float, Default: 0.5*. Traduciendo de la documentación de Mediapipe, este valor indica 
                                "La mínima puntuación de confidencia para que la detección de la mano sea considerada
                                como exitosa en el modelo de deteccion de palma".

- **min_tracking_confidence**: *Float, Default: 0.5*. Traduciendo de la documentación de Mediapipe, este valor indica 
                                "La mínima puntuación de confidencia para que el trackeo de la mano sea considerada
                                como exitoso. ...".

### Opciones de output

Cada una de las siguientes opciones puede aparecer de manera opcional como una llave dentro del diccionario `output`.
Si alguna opción no aparece en el diccionario, se usará su valor por default. El orden en el que aparecen en la cadena
es la misma en la que aparecen en este documento.

- **include_fps**: *Booleano, Default: false*. Indica si se deben incluir los fps.

- **type**: *Boolean, Default: false*. Indica si debe incluirse el tipo de mano. Los posibles valores son `'Right'` y,
            `'Left'`.

- **include_height**: *Boolean, Default: false*. Indica si se debe incluir la altura en pixeles de la imagen. Esta puede
                      ser distinta al valor de `frame_height`.

- **include_width**: *Boolean, Default: false*. Indica si se debe incluir el ancho en pixeles de la imagen. Esta puede
                      ser distinta al valor de `frame_width`.

- **include_box**: *Boolean, Default: false*. Indica si se debe incluir el rectángulo que contiene la mano.

- **include_center**: *Boolean, Default: false*. Indica si se debe incluir el centro del rectángulo que contiene la mano. 

- **lm_list**: *Lista de enteros, Default: []*. Indica los índices de los landmarks que serán enviados. Si la lista está
               vacía, se enviarán todos los landmarks. Si no se incluye esta opción, no se enviará ninguno. Para saber
               cuál índice le corresponde a cada landmark revise 
               [Hand Landmarker](https://developers.google.com/mediapipe/solutions/vision/hand_landmarker).

- **flip_x**: *Boolean, Default: false*. Indica si deben de reflejarse las coordenadas en el eje x.

- **flip_y**: *Boolean, Default: false*. Indica si deben de reflejarse las coordenadas en el eje y.

- **coordinates**: *String, Default: "pixel"*. Indica el tipo de coordenadas que se mandarán.
    - "pixel": Las coordenadas `x` y `y` son el valor en pixeles con respecto al alto y ancho de la imagen, 
               respectivamente. La coordenada `z` representa la profundidad con respecto a la muñeca.
    - "norm": Las coordenadas `x` y `y` son el valor un valor normalizado entre 0 y 1, con respecto al alto y ancho de 
              la imagen, respectivamente. La coordenada `z` representa la profundidad con respecto a la muñeca.
    - "real": Cada landmark representa coordenadas en 3D del mundo real in metros con origen en el centro geométrico de
              la mano.

- **round**: *Entero, Default: -1*. Indica el número de decimales en las coordenadas de los landmarks si `coodinates` es
             igual a `norm` o `real`. Si se indica -1, entonces no se redondean las coordenadas.

- **print_data**: *Boolean, Default: false*. Indica si se debe imprimir la cadena que se enviará. Es recomendable usarlo
                  sólo para pruebas.