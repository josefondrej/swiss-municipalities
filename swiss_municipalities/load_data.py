import fiona

if __name__ == '__main__':
    file_path = "./src/swissBOUNDARIES3D_1_3_TLM_HOHEITSGEBIET.shp"

    shape = fiona.open(file_path)
    shape_iterator = iter(shape)
    first = next(shape_iterator)

    print(first)
