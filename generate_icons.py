#!/usr/bin/env python3
"""Genera iconos PNG simples para la PWA sin dependencias externas."""
import struct, zlib, base64

def make_png(size, bg_color, emoji_placeholder=True):
    """Crea un PNG simple con color sólido."""
    width = height = size
    raw_rows = []
    r, g, b = bg_color
    for _ in range(height):
        row = b'\x00'  # filter byte
        row += bytes([r, g, b] * width)
        raw_rows.append(row)
    raw_data = b''.join(raw_rows)
    compressed = zlib.compress(raw_data, 9)
    
    def chunk(name, data):
        c = name + data
        return struct.pack('>I', len(data)) + c + struct.pack('>I', zlib.crc32(c) & 0xffffffff)
    
    png = b'\x89PNG\r\n\x1a\n'
    png += chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0))
    png += chunk(b'IDAT', compressed)
    png += chunk(b'IEND', b'')
    return png

# Color del header: #312e81 (indigo-900)
color = (49, 46, 129)

for size in [192, 512]:
    png_data = make_png(size, color)
    with open(f'icon-{size}.png', 'wb') as f:
        f.write(png_data)
    print(f'✅ icon-{size}.png creado ({len(png_data)} bytes)')

print("Iconos generados. Para un ícono con 💼 personalizado, puedes reemplazar estos archivos por cualquier PNG cuadrado.")
