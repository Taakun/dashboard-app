from google.cloud import bigquery
import json

class DataLoader:
    def __init__(self, json_path):
        with open(json_path, encoding="utf-8") as f:
            self.dataset = json.load(f)
        self.client = bigquery.Client()
        self.dataset_dict = {}

    def load_data(self):
        for k, v in self.dataset['dataset_name'].items():
            query_template = f"""
            SELECT *
            FROM `dashboard-app-001.dash_data.{v}`
            """
            query_job = self.client.query(query_template)
            df = query_job.to_dataframe()
            self.dataset_dict.update([(k, df)])
            
        return self.dataset, self.dataset_dict

# 使用例
# data_loader = DataLoader('app/dataset.json')
# data_loader.load_data()
# dataset_dict = data_loader.dataset_dict
