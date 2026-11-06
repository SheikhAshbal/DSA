raw_temperatures = [22.5, 25.0, 'missing', 21.2, 28.4, 'error', 23.1]

cleaned = [t + 1.0 for t in raw_temperatures if isinstance(t, float)]

print(cleaned)
