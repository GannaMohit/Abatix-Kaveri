from django.shortcuts import redirect
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
            studding_weight = ""
        else:
            studding_weight = f"{carat_weight}ct"
    else:
        if carat_weight is None:
            studding_weight = f"{gram_weight}g"
        else:
            studding_weight = f"{gram_weight}g+{carat_weight}ct"

    if product.gross_weight == product.net_weight:
        zpl = f'''^XA
^PR12
^LRY
^MD30
^PW560
^LL120
^PON
^FO30,13.5,0^ADN^FD{product.type.abbreviation}^FS
^FO50,13.5,0^ADN^FD-^FS
^FO70,13.5,0^ADN^FD{product.category.category}^FS
^FO30,38.5,0^ADN^FD{product.purity.display_name}^FS
^FO160,38.5,0^ADN^FDR{product.register_id}^FS
^FO30,60,0^B3N,N,30,Y,N^FD{pk}^FS
^FO320,13.5,0^ADN^FDG. WT.^FS
^FO420,13.5,0^ADN^FD:^FS
^FO440,13.50,0^A0N,24,24^FD{product.gross_weight} g^FS
^FO320,63.5,0^A0N,24,24^FD{studding_weight}^FS
^FO320,88.5,0^ADN^FD{product.vendor.old_id}^FS
^FO420,88.5,0^A0N,24,24^FD{calculation_value}^FS
^PQ1
^XZ'''
    else:
        zpl = f'''^XA
^PR12
^LRY
^MD30
^PW560
^LL120
^PON
^FO30,13.5,0^ADN^FD{product.type.abbreviation}^FS
^FO50,13.5,0^ADN^FD-^FS
^FO70,13.5,0^ADN^FD{product.category.category}^FS
^FO30,38.5,0^ADN^FD{product.purity.display_name}^FS
^FO160,38.5,0^ADN^FDR{product.register_id}^FS
^FO30,60,0^B3N,N,30,Y,N^FD{pk}^FS
^FO320,13.5,0^ADN^FDG. WT.^FS
^FO420,13.5,0^ADN^FD:^FS
^FO440,13.50,0^A0N,24,24^FD{product.gross_weight} g^FS
^FO320,38.5,0^ADN^FDN. WT.^FS
^FO420,38.5,0^ADN^FD:^FS
^FO440,38.50,0^A0N,24,24^FD{product.net_weight} g^FS
^FO320,63.5,0^A0N,24,24^FD{studding_weight}^FS
^FO320,88.5,0^ADN^FD{product.vendor.old_id}^FS
^FO420,88.5,0^A0N,24,24^FD{calculation_value}^FS
^PQ1
^XZ'''
    tag_file = open("temp_tag.zpl","w")
    tag_file.write(zpl)
    tag_file.close()
    os.system("lpr -P CL-E321Z -o raw '/home/kaveri/.var/www/Abatix/temp_tag.zpl'")
    os.remove("temp_tag.zpl")
    return redirect("product_detail", pk=pk)
