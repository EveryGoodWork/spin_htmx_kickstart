#!/usr/bin/env python3
import json
import csv
from urllib.parse import urlparse

def get_title_from_url(url):
    """Extract a meaningful title from the URL path"""
    parsed = urlparse(url)
    path = parsed.path.strip('/')
    if path:
        # Get the last meaningful segment
        segments = [s for s in path.split('/') if s and not s.startswith('baf')]
        if segments:
            return segments[-1].replace('-', ' ').replace('_', ' ').title()
    return parsed.netloc

def parse_resources(json_file, output_csv):
    with open(json_file, 'r') as f:
        data = json.load(f)

    rows = []
    for item in data.get('items', []):
        url = item.get('resource', '')
        accepts = item.get('accepts', [])

        if not accepts:
            continue

        # Get the first payment option (usually Base USDC)
        accept = accepts[0]

        # Get price - can be 'maxAmountRequired' or 'amount' depending on x402 version
        price_raw = accept.get('maxAmountRequired') or accept.get('amount', '0')

        # Convert to USDC (6 decimals)
        try:
            price_usdc = float(price_raw) / 1_000_000
        except:
            price_usdc = 0

        # Get description
        description = accept.get('description', '')
        if not description:
            # Try to infer from outputSchema or other fields
            output_schema = accept.get('outputSchema', {})
            if output_schema:
                desc_from_output = output_schema.get('output', {})
                if isinstance(desc_from_output, dict):
                    description = desc_from_output.get('description', '')

        # Generate a title
        title = get_title_from_url(url)

        # Get network
        network = accept.get('network', 'unknown')

        # Clean up description - remove newlines and limit length
        description = description.replace('\n', ' ').replace('\r', ' ')
        if len(description) > 300:
            description = description[:297] + '...'

        rows.append({
            'URL': url,
            'Title': title,
            'Description': description if description else 'No description provided',
            'Price_USDC': f"${price_usdc:.6f}",
            'Network': network
        })

    # Sort by price
    rows.sort(key=lambda x: float(x['Price_USDC'].replace('$', '')))

    # Write CSV
    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['URL', 'Title', 'Description', 'Price_USDC', 'Network'])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Created {output_csv} with {len(rows)} endpoints")
    print(f"\nPrice range: {rows[0]['Price_USDC']} to {rows[-1]['Price_USDC']}")
    print(f"\nSample entries:")
    for row in rows[:5]:
        print(f"  {row['Title']}: {row['Price_USDC']} - {row['Description'][:60]}...")

if __name__ == '__main__':
    parse_resources('x402_resources.json', 'x402_endpoints.csv')
