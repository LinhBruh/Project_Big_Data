import pandas as pd
import numpy as np
from faker import Faker

fake = Faker()
num_records = 10 # 10 triệu bản ghi

# Tạo dữ liệu bằng NumPy để tăng tốc
data = {
    "customer_id": np.arange(1, num_records + 1),
    "name": [fake.name() for _ in range(num_records)],
    "email": [fake.email() for _ in range(num_records)],
    "phone": [fake.phone_number() for _ in range(num_records)],
    "address": [fake.address() for _ in range(num_records)],
    "created_at": pd.date_range("2020-01-01", periods=num_records, freq="S").strftime("%Y-%m-%d %H:%M:%S")
}

df = pd.DataFrame(data)
print(df.head())
