import json

def read_json_file(file_path):

    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON format in file: {file_path}")

def countPeopleByCountry(data):
    country_counts = {}

    for record in data:
        country = record.get('country', 'Unknown')
        if country in country_counts:
            country_counts[country] += 1
        else:
            country_counts[country] = 1

    return country_counts

def avgAgeCountry(data, age_transform=None):
    country_ages = {}
    
    for record in data:
        age = record.get('age')
        country = record.get('country', 'Unknown')
        
        if age_transform:
            age = age_transform(age)
        
        if country is None:
            country = 'Unknown'
        
        if age is not None:
            if country in country_ages:
                country_ages[country].append(age)
            else:
                country_ages[country] = [age]
    
    avg_ages = {country: sum(ages) / len(ages) for country, ages in country_ages.items()}
    
    return avg_ages