import os
import pandas as pd


class ResultService:

    def __init__(self):

        self.results_directory = "results"

        os.makedirs(
            self.results_directory,
            exist_ok=True
        )

    def save_dynamic_results(self, results):

        file_path = os.path.join(
            self.results_directory,
            "dynamic_experiment_results.csv"
        )

        df = pd.DataFrame(results)

        df.to_csv(
            file_path,
            index=False
        )

        return file_path