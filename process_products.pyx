#!python
#cython: language_level=3


cdef dict get_product_dict(dict product):
    cdef:
        int i
        int num_entries
        list prod_images = product.get("images").split(",")
        list prod_sizes = product.get("sizes").split(",")
        list images = []
        list sizes = []
        list specifics = product.get("specifics").strip().split("\n")
        list details = []
        str image, size, detail

    num_entries = len(prod_images)
    for i in range(num_entries):
        image = prod_images[i]
        if image:
            images.append(image.replace("@", ",").strip())
    product["images"] = images

    num_entries = len(prod_sizes)
    j = 0
    for i in range(num_entries):
        size = prod_sizes[i].strip()
        if len(size):
            sizes.append(size)
    product["sizes"] = sizes

    product["categories"] = product.get("categories").lower().split(",")
    product["tags"] = product.get("tags").lower().split(",")
    product["description"] = product.get("description").strip().split("\n")

    num_entries = len(specifics)
    for i in range(num_entries):
        detail = specifics[i]
        if len(detail):
            details.append(detail.rpartition(":"))
    product["specifics"] = details
    return product


cpdef dict process_product(product):
    return get_product_dict(dict(product))


cpdef list process_product_array(list products):
    cdef:
        int num_products = len(products)
        int i
        dict product
    for i in range(num_products):
        product = dict(products[i])
        products[i] = get_product_dict(product)
    return products
