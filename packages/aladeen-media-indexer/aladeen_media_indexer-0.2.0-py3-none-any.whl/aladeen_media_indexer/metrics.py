import pandas as pd
from abc import ABC, abstractmethod
from typing import Any
import requests


class Metric(ABC):
    @abstractmethod
    def calculate(self, df: pd.DataFrame) -> pd.Series:
        pass

    def get7ma(self, df: pd.DataFrame) -> pd.Series:
        return df.rolling(window=7).mean()


class ArticleCountMetric(Metric):
    def calculate(self, df: pd.DataFrame) -> pd.Series:
        return df.groupby("day").size()


class EngagementRateMetric(Metric):
    def calculate(self, df: pd.DataFrame) -> pd.Series:
        return df.groupby("day")["engagement"].mean()


class SourceDiversityMetric(Metric):
    def calculate(self, df: pd.DataFrame) -> pd.Series:
        return df.groupby("day")["source"].nunique()


class ArticleVelocityMetric(Metric):
    def calculate(self, df: pd.DataFrame) -> pd.Series:
        return df.groupby("day").size().diff()


class MomentumMetric(Metric):
    # Divide today's engagement by the 7-day moving average of engagement
    def calculate(self, df: pd.DataFrame) -> pd.Series:
        return (
            df.groupby("day")["engagement"].sum()
            / df.groupby("day")["engagement"].rolling(window=7).mean().mean()
        )


class WeekEngagementDifferenceMetric(Metric):
    def calculate(self, df: pd.DataFrame) -> pd.Series:
        # Calculate the engagement for each day
        daily_engagement = df.groupby("day")["engagement"].sum()

        # Shift the daily engagement by 7 days to align with the previous week
        prev_week_engagement = daily_engagement.shift(7)

        # Calculate the difference in engagement from the same day last week
        week_difference = daily_engagement - prev_week_engagement

        return week_difference


class EngagementCountMetric(Metric):
    def calculate(self, df: pd.DataFrame) -> pd.Series:
        return df.groupby("day")["engagement"].count()


class TopicSimilarityMetric(Metric):
    def __init__(self, title_embeddings: Any) -> None:
        self.title_embeddings = title_embeddings

    def calculate(self, df: pd.DataFrame) -> pd.Series:
        # Implement the topic similarity calculation logic here
        raise NotImplementedError("Topic similarity calculation not implemented")


# WIP
class GELUSDExchangeRateMetric(Metric):
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def calculate(self, df: pd.DataFrame) -> pd.Series:
        # Get the start and end dates from the input DataFrame
        start_date = pd.to_datetime(df["day"].min())
        end_date = pd.to_datetime(df["day"].max())

        # Set up the API endpoint and parameters
        url = "https://www.alphavantage.co/query"
        params = {
            "function": "FX_DAILY",
            "from_symbol": "GEL",
            "to_symbol": "USD",
            "apikey": self.api_key,
            "outputsize": "full",
        }

        # Make the API request
        response = requests.get(url, params=params)
        data = response.json()

        # Check if the API request was successful
        if "Error Message" in data:
            raise ValueError(f"API request failed: {data['Error Message']}")

        # Extract the exchange rate data
        exchange_rates = data["Time Series FX (Daily)"]

        # Convert the exchange rate data to a DataFrame
        exchange_rate_df = pd.DataFrame.from_dict(
            exchange_rates, orient="index", columns=["4. close"]
        )
        exchange_rate_df.index = pd.to_datetime(exchange_rate_df.index)
        exchange_rate_df.columns = ["GEL/USD"]

        # Filter the exchange rate data based on the input DataFrame's date range
        mask = (exchange_rate_df.index >= start_date) & (
            exchange_rate_df.index <= end_date
        )
        exchange_rate_series = exchange_rate_df.loc[mask, "GEL/USD"]
        # convert to float
        exchange_rate_series = exchange_rate_series.astype(float)

        # Check if the filtered series is empty
        if exchange_rate_series.empty:
            print(
                f"No exchange rate data found for the date range: {start_date} to {end_date}"
            )
            print("Available exchange rate data:")
            print(exchange_rate_df)

        # fill missing values with the previous value
        # exchange_rate_series = exchange_rate_series.ffill()
        # exchange_rate_series = exchange_rate_series.bfill()
        print(exchange_rate_series)

        return exchange_rate_series
