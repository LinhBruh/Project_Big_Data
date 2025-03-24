import data_generation.generate_data as gd

customers = [gd.customers_gen() for _ in range(100_000)]

