import requests
from src.config import HUGGINGFACE_API_URL, HUGGINGFACE_API_TOKEN

def get_recommendation(pe_ratio, pb_ratio, dividend_yield, payout_ratio, expense_ratio, interest_rate, cpi):
    prompt = (
        f"Given the following financial metrics for JP Morgan:\n"
        f"Current P/E Ratio: {pe_ratio}\n"
        f"Current P/B Ratio: {pb_ratio}\n"
        f"Dividend Yield: {dividend_yield}\n"
        f"Payout Ratio: {payout_ratio}\n"
        f"Expense Ratio: {expense_ratio}\n"
        f"Current Federal Funds Rate: {interest_rate}\n"
        f"Current Consumer Price Index (CPI): {cpi}\n\n"
        "Based on these financial metrics, provide a buy or sell recommendation."
    )

    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"}
    payload = {"inputs": prompt, "parameters": {"max_length": 150}}

    try:
        response = requests.post(HUGGINGFACE_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()[0]['generated_text']
    except requests.RequestException as e:
        print("Error fetching recommendation:", e)
        return None
