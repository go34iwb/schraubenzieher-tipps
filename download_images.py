import os, urllib.request, json, time

ASSETS_DIR = '/home/hermes/.hermes/projects/20261017_schraubenzieher-tipps/assets/screws'
os.makedirs(ASSETS_DIR, exist_ok=True)

# File names from Wikimedia Commons
files = [
    ('schlitz.jpg', 'File:Flat_minus_screwdriver_on_table.jpg'),
    ('phillips.png', 'File:Phillips_screwdriver_1.png'),
    ('pozidriv.png', 'File:Pozi_screwdriver_2.png'),
    ('torx.jpg', 'File:Torx_screwdriver_bits_from_set,_from_T8_to_T45_and_same_with_middle_pin.jpg'),
    ('hex.jpg', 'File:Set_of_security_screw_driver_bits.jpg'),
    ('voltage-divider.jpg', 'File:Voltage_divider.jpg'),
]

for name, title in files:
    try:
        url = f'https://api.wikimedia.org/core/v1/commons/file/{title}'
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Schraubenzieher-Tipps project (local educational project)'
        })
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()
            info = json.loads(data)
            img_url = info.get('preferred', {}).get('url', '')
            if img_url:
                img_req = urllib.request.Request(img_url, headers={
                    'User-Agent': 'Mozilla/5.0 (Schraubenzieher-Tipps project)'
                })
                with urllib.request.urlopen(img_req, timeout=15) as img_resp:
                    img_data = img_resp.read()
                    out = os.path.join(ASSETS_DIR, name)
                    with open(out, 'wb') as f:
                        f.write(img_data)
                    print(f'OK: {name} ({len(img_data)} bytes)')
            else:
                print(f'FAIL: {name} - no URL in API response')
    except Exception as e:
        print(f'FAIL: {name} - {e}')
    time.sleep(1)
