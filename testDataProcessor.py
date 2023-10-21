import os
import unittest
from dataProcessor import read_json_file
from dataProcessor import avgAgeCountry
from dataProcessor import countPeopleByCountry
import numpy as np

class TestDataProcessor(unittest.TestCase):
    def test_read_json_file_success(self):
        current_directory = os.path.dirname(__file__)
        file_path = os.path.join(current_directory, "data/users.json")

        data = read_json_file(file_path)
       
        self.assertEqual(len(data), 1000)  # Ajustar o número esperado de registros
        self.assertTrue(record['name'] == 'Alice' for record in data)
        self.assertTrue(record['age'] == 25 for record in data)

    # Arquivo JSON encontrado
    def test_read_json_file_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            read_json_file("non_existent.json")

    def test_read_json_file_invalid_json(self):
        with open("invalid.json", "w") as file:
            file.write("invalid json data")
        with self.assertRaises(ValueError):
            read_json_file("invalid.json")
        
    # Arquivo JSON vazio.
    def test_avgAgeCountry_empty_data(self):
        # Test when the JSON file is empty.
        empty_data = []
        result = avgAgeCountry(empty_data)
        self.assertEqual(result, {})
            
    # Valores de idade ausentes ou nulos.
    def test_avgAgeCountry_missing_age(self):
        data = [
            {"name": "Alice", "age": 30, "country": "US"},
            {"name": "Bob", "country": "UK"}, # AUSENTE
            {"name": "Charlie", "age": None, "country": "US"}, # NONE
        ]
        result = avgAgeCountry(data)
        self.assertEqual(result, {"US": 30.0})
    
    # Campo country ausente ou nulo.
    def test_avgAgeCountry_missing_country(self):
        data = [
            {"name": "Alice", "age": 30, "country": "US"},
            {"name": "Bob", "age": 18 }, # AUSENTE
            {"name": "Charlie", "age": 41, "country": None}, # NONE
        ]
        result = avgAgeCountry(data)
        self.assertEqual(result, {"US": 30.0, "Unknown": 29.5})
     
     # Modifique a função avgAgeCountry para que ela aceite uma função de transformação como 
     # segundo argumento. Esta função deve ser aplicada à idade antes de calcular a média 
     # (por exemplo, converter idade de anos para meses).   
    def test_avgAgeCountry_with_transform(self):
        data = [
            {"name": "Alice", "age": 30, "country": "US"},
            {"name": "Bob", "age": 24, "country": "US"},
            {"name": "Charlie", "age": 36, "country": "UK"},
            {"name": "David", "age": 48, "country": "UK"},
        ]
        
        def age_in_months(age_in_years):
            return age_in_years * 12
        
        result = avgAgeCountry(data, age_transform=age_in_months)
        
        expected_result = {"US": (30 + 24) * 12 / 2, "UK": (36 + 48) * 12 / 2}
        self.assertEqual(result, expected_result)

    # Teste unitário extra de quantidade de pessoas
    def test_countPeopleByCountry(self):
        
        data = [
            {"name": "Alice", "country": "US"},
            {"name": "Bob", "country": "UK"},
            {"name": "Charlie", "country": "US"},
            {"name": "David", "country": "UK"},
            {"name": "Eve", "country": "US"},
            {"name": "Frank", "country": "FR"},
        ]
        
        result = countPeopleByCountry(data)
        
        expected_result = {"US": 3, "UK": 2, "FR": 1}
        
        self.assertEqual(result, expected_result)

    # Não tem a existência de outlier na idade
    def test_check_age_outliers(self):
        current_directory = os.path.dirname(__file__)
        file_path = os.path.join(current_directory, "data/users.json")

        data = read_json_file(file_path)

        ages = [record.get('age') for record in data if record.get('age') is not None]

        q1 = np.percentile(ages, 25)
        q3 = np.percentile(ages, 75)

        iqr = q3 - q1

        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        outliers = [age for age in ages if age < lower_bound or age > upper_bound]
        self.assertEqual(outliers, [], "Outliers found in age data.")


if __name__ == '__main__':
    unittest.main()