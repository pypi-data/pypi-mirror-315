# Paquete Platzi Final curso: Fundamentos de Programación y Python

Este paquete implementa un ejemplo de un sistema básico de gestión de reservas en Python.

## Cómo instalar la librería?
Para instalar la librería, usa el siguiente comando:

pip install pkg-platzi-final==0.4.0

## Cómo usarlo?

Para usarlo, crea un archivo `.py` y copia el siguiente script:

```python
import asyncio
from pkg_platzi_final.main import main
asyncio.run(main())
```

## Resultado esperado:
Luego de instalar la librería y ejecutar el código de ejemplo, el resultado esperado debería ser:
```
La habitación número 101 ha sido agregada!
La habitación número 102 ha sido agregada!
El cliente Alice ha sido adicionado!
El cliente Juan ha sido adicionado!
La habitación 101 está disponible!
Reserva creada para Alice en la habitación 101
Procesando el pago del cliente Alice por valor de $100
Pago completado para el cliente Alice por valor de $100
La habitación 101 ahora NO está disponible!
La habitación 102 está disponible!
Reserva creada para Juan en la habitación 102
Procesando el pago del cliente Juan por valor de $200
Pago completado para el cliente Juan por valor de $200
La habitación 102 ahora NO está disponible!
Reserva 2 cancelada
La habitación 102 ahora está disponible!
Reserva no encontrada!!!
```