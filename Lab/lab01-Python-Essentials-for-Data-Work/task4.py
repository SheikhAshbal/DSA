def safe_convert(value):
    try:
        return int(value)
    except ValueError:
        return 'Invalid'

test_values = ['10', 'abc', '42', 'hello', '7']

results = [safe_convert(v) for v in test_values]
print(results)
