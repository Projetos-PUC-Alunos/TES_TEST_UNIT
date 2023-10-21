import json
import random
from faker import Faker

def generate_data(num_lines):
    fake = Faker()
    countries = ["US", "UK", "CA", "AU", "FR", "DE", "JP", "BR"]
    data = []

    for i in range(1, num_lines + 1):
        person = {
            "name": fake.name(),
            "age": random.randint(18, 60),
            "country": random.choice(countries)
        }
        data.append(person)

    return data

def save_to_json(data, file_path):
    with open(file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)

if __name__ == "__main__":
    num_lines = 1000  # Defina o número de linhas desejado aqui
    data = generate_data(num_lines)
    save_to_json(data, "data/users.json")
    print(f"{num_lines} linhas de dados foram geradas e escritas em 'data/users.json'.")