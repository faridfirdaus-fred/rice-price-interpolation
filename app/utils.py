def fetch_rice_price_data(api_url):
    import requests
    import numpy as np

    try:
        response = requests.get(api_url)
        response.raise_for_status()
        result = response.json()

        datacontent = result.get("datacontent", {})
        tahun_list = result.get("tahun", [])
        turtahun_list = result.get("turtahun", [])
        if not datacontent:
            raise ValueError("API response does not contain 'datacontent' or it is empty.")

        # Build mapping from val to label for year and month
        tahun_map = {str(t["val"]): int(t["label"]) for t in tahun_list}
        # Use val (1-12) directly for months
        bulan_map = {str(b["val"]): b["val"] for b in turtahun_list if isinstance(b["val"], int) and 1 <= b["val"] <= 12}

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
                # Key format: [quality][var][tahun][bulan], e.g. 150001131 (1=quality, 50001=var, 13=year, 1=month)
                # Extract quality
                quality_code = key[0:1]
                # Extract year and month val (handle 1 or 2 digit month)
                # Find the year and month val by matching against all possible combinations
                found = False
                for yval in tahun_map:
                    for bval in bulan_map:
                        if key.endswith(f"{yval}{bval}"):
                            year = tahun_map[yval]
                            month = bulan_map[bval]
                            month_value = year + (month - 1) / 12.0
                            if quality_code == '1':
                                months_dict["premium"].append(month_value)
                                prices_dict["premium"].append(float(price))
                            elif quality_code == '2':
                                months_dict["medium"].append(month_value)
                                prices_dict["medium"].append(float(price))
                            elif quality_code == '3':
                                months_dict["low_quality"].append(month_value)
                                prices_dict["low_quality"].append(float(price))
                            found = True
                            break
                    if found:
                        break
                # If not found, skip
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