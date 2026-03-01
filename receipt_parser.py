import re
import json

def parse_receipt(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    bin_match = re.search(r'БИН (\d{12})', content)
    bin_val = bin_match.group(1) if bin_match else None

    products = re.findall(r'\d+\.\s+(.+)', content)

    prices = re.findall(r'=\s*(\d+,\d{2})', content)

    total_match = re.search(r'ИТОГО:\s*(\d+,\d{2})', content)
    total = total_match.group(1) if total_match else "0,00"

    date_time = re.search(r'(\d{2}\.\d{2}\.\d{4}\s\d{2}:\d{2}:\d{2})', content)
    dt_val = date_time.group(1) if date_time else None

    payment_method = "Наличные" if re.search(r'Наличные', content) else "Карта"

    receipt_data = {
        "bin": bin_val,
        "items": products,
        "prices": prices,
        "total_amount": total,
        "date_time": dt_val,
        "payment_method": payment_method
    }

    return receipt_data

if __name__ == "__main__":
    data = parse_receipt('raw.txt')
    print(json.dumps(data, indent=4, ensure_ascii=False))
    with open('parsed_receipt.json', 'w', encoding='utf-8') as out:
        json.dump(data, out, indent=4, ensure_ascii=False)