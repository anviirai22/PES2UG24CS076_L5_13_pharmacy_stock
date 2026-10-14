"""A simple pharmacy stock and prescription management system."""

import json
import sqlite3
from datetime import date, datetime

conn = sqlite3.connect(":memory:")
stock = {}
prescriptions = []


def setup_database():
    """Create the patient database and insert sample records."""
    with conn:
        conn.execute(
            "CREATE TABLE patients "
            "(id TEXT, name TEXT, allergy TEXT)"
        )
        conn.executemany(
            "INSERT INTO patients VALUES (?, ?, ?)",
            [
                ("P1", "Kavya", "penicillin"),
                ("P2", "Arjun", "none"),
                ("P3", "Meena", "ibuprofen"),
            ],
        )


def find_patient(name):
    """Find patients by name using a parameterized SQL query."""
    cursor = conn.cursor()
    query = (
        "SELECT id, allergy FROM patients "
        "WHERE name = ? COLLATE NOCASE"
    )
    return cursor.execute(query, (name,)).fetchall()


def add_stock(drug, units, expiry, batch_log=None):
    """Add positive stock quantities and record the batch."""
    if not isinstance(units, int) or isinstance(units, bool):
        raise ValueError("Stock units must be an integer.")
    if units <= 0:
        raise ValueError("Stock units must be positive.")

    datetime.strptime(expiry, "%Y-%m-%d")

    if batch_log is None:
        batch_log = []

    existing_drug = next(
        (name for name in stock if name.casefold() == drug.casefold()),
        drug,
    )
    current_units = stock.get(
        existing_drug, {}
    ).get("units", 0)

    stock[existing_drug] = {
        "units": current_units + units,
        "expiry": expiry,
    }
    batch_log.append((existing_drug, units))
    return len(batch_log)


def dispense(patient_name, drug, units):
    """Dispense medicine only when patient and stock checks pass."""
    if not isinstance(units, int) or isinstance(units, bool):
        return False
    if units <= 0:
        return False

    patients = find_patient(patient_name)
    if not patients:
        return False

    patient_id, allergy = patients[0]
    if allergy.casefold() != "none":
        if allergy.casefold() == drug.casefold():
            print("Allergy warning for", patient_name)
            return False

    stock_name = next(
        (name for name in stock if name.casefold() == drug.casefold()),
        None,
    )
    if stock_name is None:
        return False

    item = stock[stock_name]
    if item["units"] < units:
        return False

    expiry_date = datetime.strptime(
        item["expiry"], "%Y-%m-%d"
    ).date()
    if expiry_date < date.today():
        print("Expired medicine:", stock_name)
        return False

    item["units"] -= units
    prescriptions.append(
        {
            "patient": patient_id,
            "drug": stock_name,
            "units": units,
            "time": datetime.now().isoformat(timespec="seconds"),
        }
    )
    return True


def expiring_soon(days=30):
    """Return medicines expiring within the next specified days."""
    if days < 0:
        raise ValueError("Days cannot be negative.")

    today = date.today()
    soon = []

    for drug, item in stock.items():
        expiry_date = datetime.strptime(
            item["expiry"], "%Y-%m-%d"
        ).date()
        days_left = (expiry_date - today).days

        if 0 <= days_left <= days:
            soon.append(drug)

    return soon


def export_prescriptions(file="prescriptions.json"):
    """Export prescription records to a JSON file."""
    with open(file, "w", encoding="utf-8") as output_file:
        json.dump(prescriptions, output_file, indent=2)


def load_stock(file="stock.json"):
    """Load valid stock records from a JSON file."""
    try:
        with open(file, "r", encoding="utf-8") as input_file:
            data = json.load(input_file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        print("Stock file contains invalid JSON.")
        return {}

    if not isinstance(data, dict):
        print("Stock file must contain a JSON object.")
        return {}

    for drug, item in data.items():
        if not isinstance(item, dict):
            print("Invalid stock record:", drug)
            return {}
        if not isinstance(item.get("units"), int):
            print("Invalid stock quantity:", drug)
            return {}
        if isinstance(item.get("units"), bool):
            print("Invalid stock quantity:", drug)
            return {}
        if item["units"] < 0 or not isinstance(
            item.get("expiry"), str
        ):
            print("Invalid stock record:", drug)
            return {}
        try:
            datetime.strptime(item["expiry"], "%Y-%m-%d")
        except ValueError:
            print("Invalid expiry date:", drug)
            return {}

    return data


def print_stock():
    """Display the current pharmacy stock."""
    print("Pharmacy Stock")
    for drug, item in stock.items():
        print(
            drug,
            "->",
            item["units"],
            "units, expires",
            item["expiry"],
        )


def main():
    """Run the pharmacy management demonstration."""
    setup_database()
    stock.update(load_stock())

    add_stock("Paracetamol", 100, "2027-03-01")
    add_stock("Amoxicillin", 20, "2025-12-31")
    add_stock("Penicillin", 50, "2027-01-15")
    add_stock("Ibuprofen", 15, "2026-11-30")

    print(
        "Arjun gets Amoxicillin:",
        dispense("Arjun", "Amoxicillin", 30),
    )
    print(
        "Kavya gets Penicillin:",
        dispense("Kavya", "Penicillin", 10),
    )
    print(
        "Meena gets ibuprofen:",
        dispense("Meena", "ibuprofen", 2),
    )
    print(
        "Unknown patient:",
        dispense("Ghost", "Paracetamol", 5),
    )

    name = input(
        "Patient name to look up (Enter for Arjun): "
    ) or "Arjun"
    print("Lookup result:", find_patient(name))
    print("Expiring within 30 days:", expiring_soon())

    export_prescriptions()
    print_stock()


if __name__ == "__main__":
    main()
