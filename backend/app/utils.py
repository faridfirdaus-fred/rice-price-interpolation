def fetch_rice_price_data(api_url):
    import requests
    import numpy as np

    try:
        response = requests.get(api_url)
        response.raise_for_status()
        result = response.json()

        datacontent = result.get("datacontent", {})
        if not datacontent:
            raise ValueError("API response does not contain 'datacontent' or it is empty.")

        months_dict = {
            "premium": [],
            "medium": [],
            "low_quality": [],
        }
        prices_dict = {
            "premium": [],
            "medium": [],
            "low_quality": [],
        }

        for key, price in datacontent.items():
            try:
                if len(key) >= 9:
                    quality_code = key[0:1]
                    year_code = int(key[5:7])
                    month_code = int(key[7:])

                    year = 1900 + year_code if year_code >= 100 else 2000 + year_code
                    month_value = year + (month_code - 1) / 12.0

                    if quality_code == '1':
                        months_dict["premium"].append(month_value)
                        prices_dict["premium"].append(float(price))
                    elif quality_code == '2':
                        months_dict["medium"].append(month_value)
                        prices_dict["medium"].append(float(price))
                    elif quality_code == '3':
                        months_dict["low_quality"].append(month_value)
                        prices_dict["low_quality"].append(float(price))

            except (ValueError, TypeError, AttributeError):
                continue

        processed_data = {}
        for quality in ["premium", "medium", "low_quality"]:
            months = np.array(months_dict[quality])
            prices = np.array(prices_dict[quality])

            if len(months) == 0 or len(prices) == 0:
                continue

            sorted_indices = np.argsort(months)
            months = months[sorted_indices]
            prices = prices[sorted_indices]

            unique_months, unique_indices = np.unique(months, return_index=True)
            months = unique_months
            prices = prices[unique_indices]

            if not np.all(np.diff(months) > 0):
                raise ValueError(f"Month data for {quality} is not strictly increasing after processing.")

            processed_data[quality] = (months, prices)

        if not processed_data:
            raise ValueError("No valid data found after processing.")

        return processed_data

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error fetching data from API: {e}")
    except ValueError as e:
        raise RuntimeError(f"Data processing error: {e}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error: {e}")