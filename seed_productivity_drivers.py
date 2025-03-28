from app import create_app, db
from app.models import ProductivityDriver
import pandas as pd

app = create_app()

# Load the drivers from the CSV file
df = pd.read_csv("data/productivity_drivers.csv")

with app.app_context():
    for _, row in df.iterrows():
        driver = ProductivityDriver(
            domain=row["Domain"],
            theme=row["Theme"],
            name=row["Driver Name"],
            unit=row.get("Unit (Suggested)", ""),
            description=row.get("Description", "")
        )
        db.session.add(driver)

    db.session.commit()
    print("✅ Seeded productivity drivers successfully.")