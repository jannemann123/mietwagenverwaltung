from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parent
for component in ("ui", "manager", "storage"):
    sys.path.insert(0, str(ROOT / "packages" / component / "src"))
from rentalcarstorage import RentalStorage
from rentalcarmanager import RentalCarManager
from rentalcarui.rental_car_ui import RentalCarUI

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Lokale Mietwagenverwaltung")
    parser.add_argument("--data-dir", type=Path, default=ROOT / "data")
    args = parser.parse_args()
    args.data_dir.mkdir(parents=True, exist_ok=True)
    db = args.data_dir / "rental"
    import dbm
    storage = RentalStorage.open(str(db)) if dbm.whichdb(str(db)) else RentalStorage.new(str(db))
    try:
        RentalCarUI(RentalCarManager(storage)).open()
    finally:
        storage.close()

if __name__ == "__main__":
    main()
