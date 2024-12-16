from .models import OptionsData, Profeed
import httpx


class BlotterSDK:
    def __init__(self):

        pass



    # Async function to fetch and display combined DataFrame
    async def options_chains(self, ticker):
        """
        Fetch options chain data for a given ticker, parse it, and display combined options.
        Args:
            ticker (str): Stock symbol.
        """
        async with httpx.AsyncClient() as client:
            try:
                # Fetch data
                response = await client.get(f"https://blotter.fyi/get_options_chains_api?symbol={ticker}")
                response.raise_for_status()
                raw_data = response.json()

                # Process data using OptionsData
                options_data = OptionsData(raw_data)

    


                return options_data

            except httpx.HTTPStatusError as e:
                print(f"HTTP error occurred: {e}")
            except Exception as e:
                print(f"An error occurred: {e}")


    async def get_blotter_trades(self):
        """Gets pro-feed trade data."""

        async with httpx.AsyncClient() as client:
            data = await client.get("https://blotter.fyi/get_top_trades_for_feed_web?feed_name=pro")

            data = data.json()
            data = data['data']

            return Profeed(data)



