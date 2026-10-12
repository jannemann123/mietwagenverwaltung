"""Integrationstest der Portfolio-Kopie mit ausschließlich synthetischen Daten."""
import contextlib
import io
from pathlib import Path
import tempfile
import unittest

import run  # Bindet die drei lokalen Pakete ohne Registry ein.
from rentalcarstorage import RentalStorage
from rentalcarmanager import RentalCarManager
from rentalcarmanager.rental_car_manager import RentalException
from rentalcarui.rental_car_ui import RentalCarUI


class RentalWorkflowTest(unittest.TestCase):
    def test_rental_return_and_persistence(self):
        with tempfile.TemporaryDirectory() as directory:
            path = str(Path(directory) / 'rental')
            storage = RentalStorage.new(path)
            try:
                manager = RentalCarManager(storage)
                manager.add_customer('Demo Person')
                manager.add_car('DEMO-001', 'Example', 'Compact')
                customer = list(manager.get_customers())[0]
                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    RentalCarUI(manager)._RentalCarUI__view_available_car_models()
                self.assertIn('Compact', output.getvalue())
                manager.rent_car(customer.identifier, 'Compact')
                self.assertEqual(list(manager.get_cars())[0].rented_by_customer, customer.identifier)
                with self.assertRaises(RentalException):
                    manager.remove_car('DEMO-001')
                with self.assertRaises(RentalException):
                    manager.remove_customer(customer.identifier)
                manager.return_car('DEMO-001')
            finally:
                storage.close()
            storage = RentalStorage.open(path)
            try:
                manager = RentalCarManager(storage)
                self.assertEqual(len(list(manager.get_customers())), 1)
                self.assertEqual(list(manager.get_cars())[0].rented_by_customer, 0)
                manager.remove_car('DEMO-001')
                manager.remove_customer(customer.identifier)
                self.assertEqual(list(manager.get_cars()), [])
                self.assertEqual(list(manager.get_customers()), [])
            finally:
                storage.close()


if __name__ == '__main__':
    unittest.main()
