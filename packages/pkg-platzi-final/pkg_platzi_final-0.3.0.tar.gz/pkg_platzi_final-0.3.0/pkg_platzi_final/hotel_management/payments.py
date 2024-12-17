import asyncio
import random

async def process_payment(customer_name, amount):
    """Simula el procesamiento de un pago."""
    print(f'Procesando el pago del cliente {customer_name} por valor de ${amount}')
    await asyncio.sleep(random.randint(1,3)) # simular tiempo de procesar pago
    print(f'Pago completado para el cliente {customer_name} por valor de ${amount}')
    return True
