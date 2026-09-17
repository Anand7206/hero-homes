import struct

def get_image_info(filepath):
    with open(filepath, 'rb') as f:
        data = f.read()
    
    # PNG check
    if data.startswith(b'\x89PNG\r\n\x1a\n'):
        w, h = struct.unpack('>II', data[16:24])
        return 'PNG', w, h
    
    # WEBP check
    if data.startswith(b'RIFF') and data[8:12] == b'WEBP':
        # VP8 / VP8L / VP8X
        if data[12:16] == b'VP8X':
            w = 1 + struct.unpack('<I', data[24:27] + b'\x00')[0]
            h = 1 + struct.unpack('<I', data[27:30] + b'\x00')[0]
            return 'WEBP (VP8X)', w, h
        elif data[12:16] == b'VP8L':
            b1, b2, b3, b4 = data[21:25]
            w = 1 + (((b2 & 0x3f) << 8) | b1)
            h = 1 + (((b4 & 0x0f) << 12) | (b3 << 4) | ((b2 & 0xc0) >> 6))
            return 'WEBP (VP8L)', w, h
        elif data[12:16] == b'VP8 ':
            w = struct.unpack('<H', data[26:28])[0] & 0x3fff
            h = struct.unpack('<H', data[28:30])[0] & 0x3fff
            return 'WEBP (VP8)', w, h
        return 'WEBP', 0, 0

    return 'UNKNOWN', 0, 0

print("hero-homes-logo.png:", get_image_info("assets/hero-homes-logo.png"))
print("lucknow-homes-logo.webp:", get_image_info("assets/lucknow-homes-logo.webp"))
