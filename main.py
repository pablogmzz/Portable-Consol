from machine import Pin, I2C
import ssd1306 
import random
from time import sleep, ticks_ms, ticks_diff, sleep_ms

#Configuracion de pantalla
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

#Configuracion de botones
boton_arriba = Pin(0, Pin.IN, Pin.PULL_UP)
boton_abajo = Pin(2, Pin.IN, Pin.PULL_UP)
boton_izq = Pin(5, Pin.IN, Pin.PULL_UP)
boton_der = Pin(33, Pin.IN, Pin.PULL_UP)
boton_sel = Pin(4, Pin.IN, Pin.PULL_UP)
boton_ex = Pin(15, Pin.IN, Pin.PULL_UP)

PAGE_SIZE = 5
opciones = ['reflejos', 'snake', 'simon', 'pong', 'breakout', 'flappy bird']
seleccion = 0

def mostrar_menu():
    oled.fill(0)
    oled.text("Selecciona juego:", 0, 0)

    total = len(opciones)
    total_pages = (total + PAGE_SIZE - 1) // PAGE_SIZE
    page = seleccion // PAGE_SIZE
    start = page * PAGE_SIZE
    end   = min(start + PAGE_SIZE, total)

    # Dibujar sólo las opciones de la página actual
    for idx in range(start, end):
        line = idx - start
        pref = ">" if idx == seleccion else " "
        oled.text(pref + opciones[idx], 0, 10 + line*10)

    # Indicador de página en pequeño (abajo-dcha)
    oled.text(f"{page+1}/{total_pages}", 90, 56)

    oled.show()

def seleccionar_opcion():
    global seleccion

    mostrar_menu()
    while True:
        if boton_arriba.value() == 0:
            # subir selección y saltar de página si hay que
            seleccion = (seleccion - 1) % len(opciones)
            mostrar_menu()
            espera_soltado(boton_arriba)

        if boton_abajo.value() == 0:
            # bajar selección y saltar de página si hay que
            seleccion = (seleccion + 1) % len(opciones)
            mostrar_menu()
            espera_soltado(boton_abajo)

        if boton_sel.value() == 0:
            juego = opciones[seleccion]
            oled.fill(0)
            oled.text("Cargando...", 0, 20)
            oled.text(juego, 0, 30)
            oled.show()
            sleep_ms(500)
            return juego

def espera_soltado(pin):
    """Espera a que pin vuelva a 1 (suéltalo)."""
    while pin.value() == 0:
        sleep(0.01)

def leer_boton():
    estado_ant = {
        "arriba": 1,
        "abajo": 1,
        "izquierda": 1,
        "derecha": 1
    }

    while True:
        lectura = {
            "arriba": boton_arriba.value(),
            "abajo": boton_abajo.value(),
            "izquierda": boton_izq.value(),
            "derecha": boton_der.value()
        }

        for nombre in lectura:
            if estado_ant[nombre] == 1 and lectura[nombre] == 0: 
                return nombre
            estado_ant[nombre] = lectura[nombre]

        sleep_ms(10)

def jugar_reflejos():
    while True:
        # Pantalla de instrucciones
        oled.fill(0)
        oled.text('Pulsa sel', 30, 0)
        oled.text('para jugar', 30, 10)
        oled.text('-----------------', 0, 20)
        oled.text('Pulsa ex', 30, 30)
        oled.text('para salir', 30, 40)
        oled.show()

        # Espera a que se pulse botón_jugar
        while boton_sel.value() == 1 and boton_ex.value() == 1:
            sleep(0.1)

        if boton_ex.value() == 0:
            # Salir del juego
            return

        # Comienza el juego
        oled.fill(0)
        oled.text("Espera...", 0, 0)
        oled.show()
        sleep(random.uniform(2, 5))  # Tiempo aleatorio

        # Muestra "Pulsa ahora"
        oled.fill(0)
        oled.text("Pulsa ahora!", 0, 0)
        oled.show()

        inicio = ticks_ms()
        reaccion = False

        # Espera respuesta durante 500 ms
        while ticks_diff(ticks_ms(), inicio) < 500:
            if boton_sel.value() == 0:
                reaccion = True
                break

        oled.fill(0)
        if reaccion:
            oled.text("Bien hecho!", 0, 0)
        else:
            oled.text("Muy lento...", 0, 0)
        oled.show()
        sleep(2)

def jugar_snake():

    direcciones = {
        "derecha": (1, 0),
        "abajo": (0, 1),
        "izquierda": (-1, 0),
        "arriba": (0, -1)
    }
    direccion_actual = direcciones["derecha"]

    estado_ant = {
        "arriba": 1,
        "abajo": 1,
        "izquierda": 1,
        "derecha": 1
    }

    serpiente = [(5, 4), (4, 4), (3, 4)]
    score = 0

    def generar_comida():
        while True:
            x = random.randint(0, 15)
            y = random.randint(0, 7)
            if (x, y) not in serpiente:
                return (x, y)

    comida = generar_comida()
    t_anterior = ticks_ms()
    intervalo = 250 

    while True:
        lectura = {
            "arriba": boton_arriba.value(),
            "abajo": boton_abajo.value(),
            "izquierda": boton_izq.value(),
            "derecha": boton_der.value()
        }

        opuesta = (-direccion_actual[0], -direccion_actual[1])

        for nombre, valor in lectura.items():
            if estado_ant[nombre] == 1 and valor == 0:
                nueva_dir = direcciones[nombre]
                if nueva_dir != opuesta:
                    direccion_actual = nueva_dir
            estado_ant[nombre] = valor

        if boton_ex.value() == 0:
            return

        if ticks_diff(ticks_ms(), t_anterior) >= intervalo:
            t_anterior = ticks_ms()

            dx, dy = direccion_actual
            cabeza_x, cabeza_y = serpiente[0]
            nueva_cabeza = (cabeza_x + dx, cabeza_y + dy)

            if not (0 <= nueva_cabeza[0] < 16 and 0 <= nueva_cabeza[1] < 8):
                break

            if nueva_cabeza in serpiente:
                break

            serpiente.insert(0, nueva_cabeza)

            if nueva_cabeza == comida:
                score += 1
                comida = generar_comida()
            else:
                serpiente.pop()

            oled.fill(0)

            for i in range(1, 7):
                for j in range(1, 7):
                    oled.pixel(comida[0] * 8 + i, comida[1] * 8 + j, 1)

            for x, y in serpiente:
                for i in range(8):
                    for j in range(8):
                        oled.pixel(x * 8 + i, y * 8 + j, 1)

            oled.show()

        sleep_ms(10)

    # GAME OVER
    oled.fill(0)
    oled.text("GAME OVER", 20, 10)
    oled.text("Score: "+str(score), 20, 30)
    oled.text("Pulsa ex", 30, 45)
    oled.text("para salir",20,55)
    oled.show()
    while True:
        if boton_ex.value() == 0:
            return
        sleep_ms(10)

def mostrar_paso(paso):
    oled.fill(0)
    oled.text("Simon dice:", 0, 0)
    oled.text(paso.upper(), 0, 20)
    oled.show()
    sleep_ms(600)
    oled.fill(0)
    oled.show()
    sleep_ms(200)

def mostrar_confirmacion(nombre):
    oled.fill(0)
    oled.text("Tu: " + nombre.upper(), 0, 20)
    oled.show()
    sleep_ms(400)

def jugar_simon():
    opciones = ['arriba', 'abajo', 'izquierda', 'derecha']
    lista_simon = []
    jugando = True
    score = 0
    while jugando:
        nuevo = random.choice(opciones)
        lista_simon.append(nuevo)

        for paso in lista_simon:
            mostrar_paso(paso)

        for paso_esperado in lista_simon:
            entrada = leer_boton()
            mostrar_confirmacion(entrada)  
            if entrada != paso_esperado:
                oled.fill(0)
                oled.text("Fallaste!", 0, 20)
                oled.text("Score: " + str(score) ,0,0)
                oled.show()
                sleep_ms(1000)
                return  

        oled.fill(0)
        score += 1
        oled.text("Bien hecho!", 0, 20)
        oled.show()
        sleep_ms(500)

def jugar_pong():
    # Tamaño pantalla
    ancho = 128
    alto = 64

    # Tamaño paletas y pelota
    paleta_ancho = 3
    paleta_alto = 15
    pelota_size = 2

    # Posiciones iniciales
    jugador_y = alto // 2 - paleta_alto // 2
    ia_y     = alto // 2 - paleta_alto // 2
    pelota_x = ancho // 2
    pelota_y = alto // 2
    dx = -2
    dy = 2

    # Velocidades
    velocidad_jugador = 2
    velocidad_ia      = 1

    # Puntuaciones
    jugador_puntos = 0
    ia_puntos      = 0

    # Temporizador
    t_anterior = ticks_ms()
    intervalo  = 20

    # Rellena un rectángulo pixel a pixel
    def rect_relleno(oled, x, y, w, h, color=1):
        for i in range(w):
            for j in range(h):
                oled.pixel(x + i, y + j, color)

    # Dibuja todo el frame
    def dibujar():
        oled.fill(0)
        rect_relleno(oled, 2,             jugador_y, paleta_ancho, paleta_alto)
        rect_relleno(oled, ancho - 5,    ia_y,      paleta_ancho, paleta_alto)
        rect_relleno(oled, pelota_x,      pelota_y,  pelota_size,  pelota_size)
        oled.text(str(jugador_puntos), 40, 0)
        oled.text(str(ia_puntos),      80, 0)
        oled.show()

    # Pantalla de pausa
    def pausa():
        oled.fill(0)
        oled.text("=== PAUSE ===", 20, 10)
        oled.text("SEL: Resume",    10, 30)
        oled.text("EX:  Menu",      10, 45)
        oled.show()
        # Espera a que se pulse SEL o EX
        while True:
            if boton_sel.value() == 0:
                # debounce
                sleep_ms(200)
                return  # reanudar
            if boton_ex.value() == 0:
                # debounce
                sleep_ms(200)
                raise StopIteration  # señal para volver al menú

    try:
        while True:
            # Detecta petición de pausa
            if boton_sel.value() == 0:
                sleep_ms(200)  # debounce
                pausa()

            # Controla el ritmo de frames
            if ticks_diff(ticks_ms(), t_anterior) < intervalo:
                continue
            t_anterior = ticks_ms()

            # Movimiento jugador
            if boton_arriba.value() == 0 and jugador_y > 0:
                jugador_y -= velocidad_jugador
            elif boton_abajo.value() == 0 and jugador_y + paleta_alto < alto:
                jugador_y += velocidad_jugador

            # IA sigue la pelota
            if pelota_y < ia_y + paleta_alto // 2 and ia_y > 0:
                ia_y -= velocidad_ia
            elif pelota_y > ia_y + paleta_alto // 2 and ia_y + paleta_alto < alto:
                ia_y += velocidad_ia

            # Mueve la pelota
            pelota_x += dx
            pelota_y += dy

            # Rebote con bordes superior e inferior
            if pelota_y <= 0 or pelota_y + pelota_size >= alto:
                dy *= -1

            # Rebote con paleta jugador
            if (pelota_x <= 2 + paleta_ancho and
                jugador_y <= pelota_y <= jugador_y + paleta_alto):
                dx *= -1

            # Rebote con paleta IA
            if (pelota_x + pelota_size >= ancho - 5 and
                ia_y <= pelota_y <= ia_y + paleta_alto):
                dx *= -1

            # Punto IA
            if pelota_x <= 0:
                ia_puntos += 1
                pelota_x = ancho // 2
                pelota_y = alto  // 2
                dx = 2; dy = 2
                sleep_ms(1000)

            # Punto jugador
            if pelota_x >= ancho:
                jugador_puntos += 1
                pelota_x = ancho // 2
                pelota_y = alto  // 2
                dx = -2; dy = 2
                sleep_ms(1000)

            dibujar()

    except StopIteration:
        # Se lanzó para volver al menú
        return

def jugar_breakout():
     # Pantalla
    ancho, alto = 128, 64

    # Pala
    pala_w, pala_h = 20, 4
    pala_x = (ancho - pala_w)//2
    pala_y = alto - pala_h - 2
    vel_pala = 3

    # Bola
    bola_size = 2
    bola_x = ancho//2
    bola_y = pala_y - bola_size
    bola_dx = random.choice([-2, 2])
    bola_dy = -2

    # Ladrillos (8×4)
    cols, filas = 8, 4
    ladr_w, ladr_h = ancho//cols, 8
    ladrillos = [[1]*cols for _ in range(filas)]

    # Puntuación
    puntuacion = 0

    # Temporizador
    t_ant = ticks_ms()
    intervalo = 20

    # Dibuja o borra un rectángulo pixel a pixel
    def rect_relleno(x, y, w, h, c=1):
        for i in range(w):
            for j in range(h):
                oled.pixel(x + i, y + j, c)

    # Dibuja sólo los ladrillos (al inicio)
    def init_ladrillos():
        oled.fill(0)
        for f in range(filas):
            for c in range(cols):
                if ladrillos[f][c]:
                    x0 = c * ladr_w
                    y0 = f * ladr_h
                    rect_relleno(x0+1, y0+1, ladr_w-2, ladr_h-2, 1)
        oled.show()

    # Pantalla de pausa
    def pausa():
        oled.fill(0)
        oled.text("=== PAUSE ===", 20, 15)
        oled.text("SEL: Resume", 20, 30)
        oled.text("EX:  Menu",  20, 45)
        oled.show()
        while True:
            if boton_sel.value() == 0:
                sleep_ms(200)  # debounce
                # Al reanudar, limpiamos y redibujamos todo:
                oled.fill(0)
                init_ladrillos()
                # Dibuja pala, bola y marcador en sus posiciones actuales
                rect_relleno(pala_x, pala_y, pala_w, pala_h, 1)
                rect_relleno(bola_x, bola_y, bola_size, bola_size, 1)
                oled.text(str(puntuacion), ancho-20, 0)
                oled.show()
                return
            if boton_ex.value() == 0:
                sleep_ms(200)
                raise StopIteration

    # Inicializa ladrillos y guarda posiciones previas
    init_ladrillos()
    prev_pala_x, prev_bola_x, prev_bola_y = pala_x, bola_x, bola_y

    try:
        while True:
            # Check pausa
            if boton_sel.value() == 0:
                sleep_ms(200)
                pausa()

            # Control de ritmo
            if ticks_diff(ticks_ms(), t_ant) < intervalo:
                continue
            t_ant = ticks_ms()

            # Borra pala y bola viejas
            rect_relleno(prev_pala_x, pala_y, pala_w, pala_h, 0)
            rect_relleno(prev_bola_x, prev_bola_y, bola_size, bola_size, 0)

            # Movimiento pala
            if boton_izq.value() == 0 and pala_x > 0:
                pala_x -= vel_pala
            if boton_der.value() == 0 and pala_x + pala_w < ancho:
                pala_x += vel_pala

            # Movimiento bola
            bola_x += bola_dx
            bola_y += bola_dy

            # Rebotes con paredes
            if bola_x <= 0 or bola_x + bola_size >= ancho:
                bola_dx *= -1
            if bola_y <= 0:
                bola_dy *= -1

            # Rebote con pala
            if (pala_y <= bola_y + bola_size <= pala_y + pala_h and
                pala_x <= bola_x <= pala_x + pala_w):
                bola_dy *= -1

            # Colisión con ladrillos
            fcol = bola_y // ladr_h
            ccol = bola_x // ladr_w
            if 0 <= fcol < filas and 0 <= ccol < cols and ladrillos[fcol][ccol]:
                ladrillos[fcol][ccol] = 0
                puntuacion += 1
                x0 = ccol * ladr_w
                y0 = fcol * ladr_h
                rect_relleno(x0+1, y0+1, ladr_w-2, ladr_h-2, 0)
                bola_dy *= -1

            # Game over
            if bola_y > alto:
                oled.fill(0)
                oled.text("GAME OVER", 30, 20)
                oled.text("Score: " + str(puntuacion), 20, 40)
                oled.show()
                sleep_ms(2000)
                return

            # Dibuja pala, bola y marcador
            rect_relleno(pala_x, pala_y, pala_w, pala_h, 1)
            rect_relleno(bola_x, bola_y, bola_size, bola_size, 1)
            # Borra marcador previo y dibuja nuevo
            rect_relleno(ancho-25, 0, 25, 8, 0)
            oled.text(str(puntuacion), ancho-20, 0)
            oled.show()

            # Actualiza previas
            prev_pala_x, prev_bola_x, prev_bola_y = pala_x, bola_x, bola_y

    except StopIteration:
        # Vuelve al menú
        return

def jugar_flappy():
    # Dimensiones
    ancho, alto = 128, 64

    # Accesos rápidos
    pix  = oled.pixel
    fill = oled.fill
    text = oled.text
    show = oled.show

    # Pájaro (todo en enteros)
    bird_x, bird_y = 30, alto // 2
    vel_y          = 0
    gravedad       = 1     # gravedad entera
    salto          = -5
    bird_size      = 3

    # Tubos
    pipe_w         = 12    # más finos
    gap_h          = 30    # más hueco
    pipe_speed     = 2
    spawn_interval = 3000  # más separación
    last_spawn     = ticks_ms()
    pipes          = []

    # Puntuación
    score = 0

    # Frame timing
    t0        = ticks_ms()
    intervalo = 70     # ≈14 fps

    # Dibujo de bloque (pájaro)
    def rect_o(x, y, w, h, c=1):
        xi, yi = x, y
        for i in range(w):
            for j in range(h):
                pix(xi + i, yi + j, c)

    # Contorno de rectángulo (tuberías)
    def rect_outline(x, y, w, h, c=1):
        xi, yi = x, y
        wi, hi = w, h
        # horizontales
        for i in range(wi):
            pix(xi + i, yi,         c)
            pix(xi + i, yi + hi - 1, c)
        # verticales
        for j in range(hi):
            pix(xi,          yi + j, c)
            pix(xi + wi - 1, yi + j, c)

    # Pantallazo de Game Over
    def game_over():
        fill(0)
        text("GAME OVER", 30, 20)
        text("Score:" + str(score), 30, 35)
        show()
        sleep_ms(2000)

    while True:
        # Control de fps
        if ticks_diff(ticks_ms(), t0) < intervalo:
            continue
        t0 = ticks_ms()

        # Salto
        if boton_sel.value() == 0:
            vel_y = salto
            sleep_ms(100)  # debounce más corto

        # Física entera
        vel_y += gravedad
        bird_y += vel_y

        # Límite arriba/abajo
        if bird_y < 0 or bird_y + bird_size > alto:
            game_over()
            return

        # Generar tubo
        if ticks_diff(ticks_ms(), last_spawn) > spawn_interval:
            last_spawn = ticks_ms()
            gap_y = random.randint(10, alto - gap_h - 10)
            pipes.append([ancho, gap_y])

        # Mover tubos, borrar viejos, colisiones, cuenta
        for idx in range(len(pipes)-1, -1, -1):
            x0, gy = pipes[idx]
            x0 -= pipe_speed
            # fuera de pantalla
            if x0 < -pipe_w:
                pipes.pop(idx)
                score += 1
                continue
            # colisión
            if (bird_x + bird_size > x0 and bird_x < x0 + pipe_w and
               (bird_y < gy or bird_y + bird_size > gy + gap_h)):
                game_over()
                return
            pipes[idx][0] = x0  # actualiza posición

        # Dibujo completo
        fill(0)
        # pájaro
        rect_o(bird_x, bird_y, bird_size, bird_size, 1)
        # tubos
        for x0, gy in pipes:
            rect_outline(x0, 0,        pipe_w, gy,    1)
            rect_outline(x0, gy + gap_h,
                         pipe_w,
                         alto - (gy + gap_h),
                         1)
        # puntuación
        text(str(score), ancho - 20, 0)
        show()


# Bucle principal del programa
while True:
    mostrar_menu()
    juego_elegido = seleccionar_opcion()

    if juego_elegido == 'reflejos':
        jugar_reflejos()
    elif juego_elegido == 'snake':
        jugar_snake()
    elif juego_elegido == 'simon':
        jugar_simon()
    elif juego_elegido == 'pong':
        jugar_pong()
    elif juego_elegido == 'breakout':
        jugar_breakout()
    elif juego_elegido == 'flappy bird':
        jugar_flappy()
    else:
        oled.fill(0)
        oled.text("Juego no valido", 0, 30)
        oled.show()
        sleep(2)

