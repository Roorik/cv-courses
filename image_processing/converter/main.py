# Написать конвертер из png в bmp, используя только считывание файлов побитно через массивы
import struct
import zlib

from pathlib import Path

BASE_DIR = Path(__file__).parent
png_dir = BASE_DIR.joinpath('input.png')
bmp_dir = BASE_DIR.joinpath('output.bmp')

def apply_filter(filter_type, current_row, previous_row):
    row_data = bytearray()
    for i in range(len(current_row)):
        left = row_data[i - 3] if i >= 3 else 0
        up = previous_row[i] if previous_row else 0
        upper_left = previous_row[i - 3] if previous_row and i >= 3 else 0

        if filter_type == 0:  # None
            row_data.append(current_row[i])
        elif filter_type == 1:  # Sub
            row_data.append((current_row[i] + left) % 256)
        elif filter_type == 2:  # Up
            row_data.append((current_row[i] + up) % 256)
        elif filter_type == 3:  # Average
            row_data.append((current_row[i] + (left + up) // 2) % 256)
        elif filter_type == 4:  # Paeth
            p = left + up - upper_left
            pa = abs(p - left)
            pb = abs(p - up)
            pc = abs(p - upper_left)
            predictor = left if pa <= pb and pa <= pc else up if pb <= pc else upper_left
            row_data.append((current_row[i] + predictor) % 256)
        else:
            raise ValueError(f"Неизвестный тип фильтра: {filter_type}")

    return row_data

def png_reader():
    with open(png_dir, 'rb') as file:
        signature = file.read(8)

        chunks = []

        chunk_type = ''

        while chunk_type != 'IEND':
            # Читаем 4 байта длины чанка
            chunk_length_data = file.read(4)
            chunk_length = struct.unpack('>I', chunk_length_data)[0]  
            # Читаем 4 байта типа чанка
            chunk_type = file.read(4).decode('ascii')
            # Читаем данные чанка
            chunk_data = file.read(chunk_length)
            # Читаем 4 байта CRC (контрольная сумма)
            chunk_crc = file.read(4)
            # Сохраняем информацию о чанке
            chunks.append((chunk_type, chunk_data))

        # отдаём тюпл, где каждый элемент - дикт с инфой о типе и содержимом чанка
        return chunks        
    
def create_bmp(chunks):
    # парс чанков
    width = height = bit_depth = color_type = 0
    # перебираем тип и данные каждого чанка
    temp = list()
    for chunk_type, chunk_data in chunks:
        if chunk_type == 'IHDR':
            # распаковываем слайс в 13 первых байтов чанка на отдельные переменные
            # '>IIBBBBB' форма, где > - старшинство слева направо, I - 4 байта как беззнаковое число, B - 1 байт как беззнаковое число
            width, height, bit_depth, color_type, _, _, _ = struct.unpack('>IIBBBBB', chunk_data[:13])
            if color_type != 2 or bit_depth != 8:  # RGB
                raise NotImplementedError("Только 24-битный PNG поддерживается этим кодом.")
        elif chunk_type == 'IDAT':
            temp.append(chunk_data)
    decompressed = zlib.decompress(b''.join(temp))

    previous_row = None
    
    bmp_data = bytearray()
    offset = 0
    row_size = (width * 3 + 3) & ~3
    rows  = []
    for _ in range(height):
        filter_type = decompressed[offset]
        scanline = decompressed[offset + 1: offset + 1 + width * 3]
        offset += 1 + width * 3

        decoded_row = apply_filter(filter_type, scanline, previous_row)

        previous_row=decoded_row
        row_data = bytearray()
        
        for x in range(width):
            r, g, b = decoded_row[x * 3:(x + 1) * 3]
            row_data.extend([b, g, r])  # BMP использует порядок BGR
                
        rows.append(row_data + b'\x00' * (row_size - len(row_data)))
        previous_row = decoded_row
        
    # Записываем строки в bmp_pixels в обратном порядке
    for row_data in reversed(rows):
        bmp_data.extend(row_data)

    # Подготовка заголовка BMP
    file_size = 14 + 40 + len(bmp_data)  # File header + DIB header + image data
    bmp_header = struct.pack('<2sIHHI', b'BM', file_size, 0, 0, 54)
    dib_header = struct.pack('<IiiHHIIIIII', 40, width, height, 1, 24, 0, len(bmp_data), 0, 0, 0, 0)

    # Запись данных в BMP файл
    with open(bmp_dir, 'wb') as bmp_file:
        bmp_file.write(bmp_header)  # Заголовок файла BMP
        bmp_file.write(dib_header)  # Заголовок DIB
        bmp_file.write(bmp_data)    # Данные изображения
    


if __name__ == '__main__':
    png_data = png_reader()
    # вызываем создание бмп файла скармливая ему декод чанков 
    create_bmp(png_data)
