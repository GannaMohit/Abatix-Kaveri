from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.db.models import Sum
from .models import Product
import os

def PrintTag(request, pk):
    product = Product.objects.get(pk=pk)
    if product.calculation == "Making Charges":
        calculation = "M.C."
        calculation_value = f"₹{product.making_charges}"
    elif product.calculation == "Wastage":
        calculation = "WST."
        calculation_value = f"{product.wastage} %"
    else:
        calculation = "MRP."
        calculation_value = f"₹{product.mrp}"

    gram_weight = product.studs.filter(unit__unit="gram").aggregate(Sum('weight'))["weight__sum"]
    carat_weight = product.studs.filter(unit__unit="carat").aggregate(Sum('weight'))["weight__sum"]

    if gram_weight is None:
        if carat_weight is None:
            studs_weight = ""
        else:
            studs_weight = f"{carat_weight}ct"
    else:
        if carat_weight is None:
            studs_weight = f"{gram_weight}g"
        else:
            studs_weight = f"{gram_weight}g+{carat_weight}ct"

    if product.category.category == 'Bangle':
        zpl = render_to_string("stock/tags/bangle.txt", context=locals())
    elif abs( product.gross_weight - product.net_weight ) > 0.0005:
        zpl = render_to_string("stock/tags/mangalsutra.txt", context=locals())
    else:
        zpl = render_to_string("stock/tags/normal.txt", context=locals())
    tag_file = open("temp_tag.zpl","w")
    tag_file.write(zpl)
    tag_file.close()
    os.system(f"lpr -P CL-E321Z -o raw '{os.path.abspath(tag_file.name)}'")
    # os.remove("temp_tag.zpl")
    return redirect("product_detail", pk=pk)
