import json

with open('harvest_result.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("Title:", data.get('title'))
print("Phone numbers:", data.get('phone_numbers'))
print("WhatsApp numbers:", data.get('whatsapp_numbers'))
print("Text phones:", data.get('text_phones'))
print("Map iframes:", data.get('map_iframes'))
print("RERA text:", data.get('rera_text'))
print(f"\nFound Images ({len(data.get('images', []))} total):")
for idx, img in enumerate(data.get('images', [])):
    print(f"{idx+1}. src: {img['src']} | alt: {img['alt']} | dims: {img['width']}x{img['height']}")
