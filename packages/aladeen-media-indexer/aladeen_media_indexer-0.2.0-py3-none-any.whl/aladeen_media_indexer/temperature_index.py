import pandas as pd
from abc import ABC, abstractmethod
from typing import List, Dict
from aladeen_media_indexer.metrics import Metric
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.decomposition import PCA


class Index(ABC):
    def __init__(self, metrics: List[Metric]) -> None:
        self.metrics = metrics
        # self.weights = weights
        self.index: pd.DataFrame = None

    @abstractmethod
    def calculate_scores(self, df: pd.DataFrame) -> None:
        pass

    @abstractmethod
    def display_top_news(self, top_n: int = 10) -> None:
        pass


class TemperatureIndex(Index):
    def __init__(
        self,
        metrics: List[Metric],
        min_articles_per_day: int = 400,
        dimensionality_reduction=None,
    ) -> None:
        super().__init__(metrics)
        self.min_articles_per_day = min_articles_per_day
        if dimensionality_reduction is None:
            self.dimensionality_reduction = PCA(n_components=1)
        else:
            self.dimensionality_reduction = dimensionality_reduction

    def filter_data(self, df: pd.DataFrame) -> pd.DataFrame:
        # Convert 'day' column to Timestamp
        df["day"] = pd.to_datetime(df["day"])

        # Filter out days with less than min_articles_per_day
        article_counts = df.groupby("day").size()
        valid_days = article_counts[article_counts >= self.min_articles_per_day].index
        df_filtered = df[df["day"].isin(valid_days)]

        return df_filtered

    def calculate_metric_values(self, df: pd.DataFrame) -> Dict[str, pd.Series]:
        metric_values = {}
        for metric in self.metrics:
            metric_values[metric.__class__.__name__] = metric.calculate(df)

        return metric_values

    def create_temperature_index(
        self, metric_values: Dict[str, pd.Series]
    ) -> pd.DataFrame:
        temperature_index = pd.DataFrame(metric_values)
        return temperature_index

    def handle_missing_values(self, temperature_index: pd.DataFrame) -> np.ndarray:
        imputer = SimpleImputer(strategy="mean")
        imputed_data = imputer.fit_transform(temperature_index)
        return imputed_data

    def standardize_data(self, imputed_data: np.ndarray) -> np.ndarray:
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(imputed_data)
        return scaled_data

    def perform_pca(self, scaled_data: np.ndarray) -> np.ndarray:
        pca = PCA(
            n_components=1
        )  # Set the number of components to 1 for a single index
        pca.fit(scaled_data)
        principal_component_scores = pca.transform(scaled_data)
        return principal_component_scores

    def normalize_index(self, temperature_index: pd.DataFrame) -> pd.DataFrame:
        min_max_scaler = lambda x: (x - x.min()) / (x.max() - x.min())
        normalized_index = temperature_index.apply(min_max_scaler)
        return normalized_index

    def perform_dimensionality_reduction(self, scaled_data: np.ndarray) -> np.ndarray:
        self.dimensionality_reduction.fit(scaled_data)
        reduced_data = self.dimensionality_reduction.transform(scaled_data)
        return reduced_data

    def calculate_scores(
        self, df: pd.DataFrame, smoothing_function=(lambda x: x)
    ) -> None:
        # Filter the data
        filtered_df = self.filter_data(df)

        # Calculate metric values
        metric_values = self.calculate_metric_values(filtered_df)

        # Create temperature index dataframe
        temperature_index = self.create_temperature_index(metric_values)

        smoothed_index = smoothing_function(temperature_index)

        # Get first non-NaN index to use as a reference for missing values
        first_non_nan_index = smoothed_index.apply(lambda x: x.first_valid_index())

        smoothed_index = smoothed_index.loc[
            first_non_nan_index["ArticleCountMetric"] : smoothed_index.index[-2]
        ]

        # Handle missing values
        imputed_data = self.handle_missing_values(smoothed_index)

        # Standardize the data
        scaled_data = self.standardize_data(imputed_data)

        # Perform dimensionality reduction
        reduced_data = self.perform_dimensionality_reduction(scaled_data)

        # Add the reduced data scores to the temperature index dataframe
        smoothed_index.loc[:, "temperature_score"] = reduced_data

        # Normalize the index
        normalized_index = self.normalize_index(smoothed_index)

        self.index = normalized_index

    def display_top_news(self, top_n: int = 10) -> None:
        if self.index is None:
            raise ValueError(
                "Temperature index not calculated. Call calculate_scores() first."
            )

        # Display the top news articles based on the temperature score
        top_news = self.index.sort_values(by="temperature_score", ascending=False).head(
            top_n
        )
        print(top_news)

    def get_index(self):
        return self.index["temperature_score"]
