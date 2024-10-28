import requests
from config import HUGGINGFACE_API_URL, HUGGINGFACE_API_TOKEN

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
        generated_text = response.json()[0]['generated_text'].strip()  # Clean up whitespace
        return generated_text  # Return the generated recommendation
    except requests.RequestException as e:
        print("Error fetching recommendation:", e)
        return None

# Example usage
if __name__ == '__main__':
    # Sample financial metrics for JP Morgan
    pe_ratio = 12.364294
    pb_ratio = 1.9305954
    dividend_yield = 0.0225
    payout_ratio = 0.2557
    expense_ratio = 0.32658258064834356
    interest_rate = 5.13
    cpi = 315.301

    recommendation = get_recommendation(pe_ratio, pb_ratio, dividend_yield, payout_ratio, expense_ratio, interest_rate, cpi)
    if recommendation:
        print("Recommendation:", recommendation)
    else:
        print("No recommendation could be generated.")
