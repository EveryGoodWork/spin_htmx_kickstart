#!/usr/bin/env python3
import json
import csv
from urllib.parse import urlparse

def get_name_from_url(url):
    """Extract a meaningful name from the URL"""
    parsed = urlparse(url)
    host = parsed.netloc.replace('www.', '')
    path = parsed.path.strip('/')

    # Get the last meaningful path segment
    if path:
        segments = [s for s in path.split('/') if s and not s.startswith('baf') and len(s) < 50]
        if segments:
            name = segments[-1].replace('-', ' ').replace('_', ' ').title()
            return f"{host} - {name}"
    return host

def categorize(url, description):
    """Attempt to categorize based on URL and description"""
    text = (url + ' ' + description).lower()

    if any(w in text for w in ['news', 'headline', 'article']):
        return 'News'
    elif any(w in text for w in ['defi', 'pool', 'liquidity', 'yield', 'swap', 'tvl', 'apr']):
        return 'DeFi'
    elif any(w in text for w in ['trading', 'indicator', 'technical', 'signal', 'price', 'crypto', 'token', 'coin']):
        return 'Trading/Crypto'
    elif any(w in text for w in ['ai', 'agent', 'chat', 'llm']):
        return 'AI/Agents'
    elif any(w in text for w in ['url', 'fetch', 'extract', 'metadata', 'content', 'preview']):
        return 'Web Scraping'
    elif any(w in text for w in ['bridge', 'cross-chain']):
        return 'Cross-Chain'
    elif any(w in text for w in ['verify', 'proof', 'encrypt', 'security']):
        return 'Security/Verification'
    elif any(w in text for w in ['twitter', 'x.com', 'social']):
        return 'Social Media'
    elif any(w in text for w in ['pinata', 'ipfs', 'cid', 'content']):
        return 'Content/Storage'
    elif any(w in text for w in ['polymarket', 'prediction', 'market']):
        return 'Prediction Markets'
    else:
        return 'Other'

def parse_resources(json_file, output_csv):
    with open(json_file, 'r') as f:
        data = json.load(f)

    rows = []
    for item in data.get('items', []):
        url = item.get('resource', '')
        accepts = item.get('accepts', [])

        if not accepts:
            continue

        # Get the first payment option
        accept = accepts[0]

        # Get price - can be 'maxAmountRequired' or 'amount'
        price_raw = accept.get('maxAmountRequired') or accept.get('amount', '0')
        try:
            price_usdc = float(price_raw) / 1_000_000
        except:
            price_usdc = 0

        # Get description
        description = accept.get('description', '')
        if not description:
            description = 'No description provided'

        # Clean description
        description = description.replace('\n', ' ').replace('\r', ' ').replace('"', "'")
        if len(description) > 200:
            description = description[:197] + '...'

        # Generate name and category
        name = get_name_from_url(url)
        category = categorize(url, description)

        rows.append({
            'Name': name,
            'Description': description,
            'URL': url,
            'Category': category,
            'Cost': f"${price_usdc:.4f}"
        })

    # Sort by category then cost
    rows.sort(key=lambda x: (x['Category'], float(x['Cost'].replace('$', ''))))

    # Write CSV
    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['Name', 'Description', 'URL', 'Category', 'Cost'])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Total endpoints: {len(rows)}")

if __name__ == '__main__':
    parse_resources('x402_resources.json', 'x402_full_list.csv')
