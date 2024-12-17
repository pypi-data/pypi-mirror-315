import asyncio
from .hotel_management.reservations import Reservation, ReservationSystem
from .hotel_management.customers import Customer, CustomerManagement
from .hotel_management.rooms import Room, RoomManagement
from .hotel_management.payments import process_payment
from datetime import datetime

async def main():
    # Inicializar sistemas
    reservation_system = ReservationSystem()
    customer_mgmt = CustomerManagement()
    room_mgmt = RoomManagement()

    # Crear habitaciones
    room1 = Room(101,'Single', 100)
    room2 = Room(102,'Double', 200)
    room_mgmt.add_room(room1)
    room_mgmt.add_room(room2)
    # Agregar clientes
    customer1 = Customer(1, "Alice", "alice@example.com")
    customer2 = Customer(2, "Juan", "juan@example.com")
    customer_mgmt.add_customer(customer1)
    customer_mgmt.add_customer(customer2)

    # Verificar disponibilidad de habitaciones
    if room_mgmt.check_availability(101):
        reservation1 = Reservation(1,'Alice', 101, datetime.now(), datetime.now())
        reservation_system.add_reservation(reservation1)
        # Procesar pago asincrónicamente
        await process_payment('Alice', 100)
        room_mgmt.update_availability(101)

    # Verificar disponibilidad de habitaciones
    if room_mgmt.check_availability(102):
        reservation2 = Reservation(2,'Juan', 102, datetime.now(), datetime.now())
        reservation_system.add_reservation(reservation2)
        # Procesar pago asincrónicamente
        await process_payment('Juan', 200)
        room_mgmt.update_availability(102)
    # cancelar una reserva
    reservation_system.cancel_reservation(2)
    room_mgmt.update_availability(102)
    # cancelar una reserva inexistente
    reservation_system.cancel_reservation(4)

if __name__ == "__main__":
    asyncio.run(main())

