import sqlite3
from masters.models import *
from sales.models import *
from stock.models import *
from vouchers.models import *

db = sqlite3.connect('kaveri.db')
db.row_factory = sqlite3.Row

def migrate_masters_gst():
    gst_states = db.execute("SELECT * FROM GST_States ORDER BY id").fetchall()
    for gst_state in gst_states:
        obj = GST_State(code=gst_state['code'],
                    state=gst_state['state'],
                    apha_code=gst_state['apha_code'])
        obj.save()

    gst_rates = db.execute("SELECT * FROM GST_Rates ORDER BY id").fetchall()
    for gst_rate in gst_rates:
        obj = GST_Rate(type=gst_rate['type'],
                    percentage=gst_rate['percentage'])
        obj.save()

    hsns = db.execute("SELECT * FROM HSNs ORDER BY id").fetchall()
    for hsn in hsns:
        obj = HSN(code=hsn['code'],
                    sgst=hsn['sgst'],
                    cgst=hsn['cgst'],
                    igst=hsn['igst'],
                    description=hsn['description'])
        obj.save()

def migrate_masters_product():
    metals = db.execute("SELECT * FROM Metals ORDER BY id").fetchall()
    for metal in metals:
        obj = Metal(metal=metal['metal'],
                    symbol=metal['symbol'],
                    colour=metal['colour'],
                    melting_point=metal['melting_point'],
                    boiling_point=metal['boiling_point'],
                    density=metal['density'])
        obj.save()

    purities = db.execute("SELECT * FROM Purities ORDER BY id").fetchall()
    for purity in purities:
        obj = Purity(purity=purity['purity'],
                    karatage=purity['karatage'],
                    display_name=purity['display_name'])
        obj.save()

    types = db.execute("SELECT * FROM Types ORDER BY id")
    for type in types:
        obj = Type(type=type['type'],
                    hsn=HSN.objects.get(pk=type['hsn_id']),
                    abbreviation=type['abbreviation'])
        obj.save()

    categories = db.execute("SELECT * FROM Categories ORDER BY id").fetchall()
    for category in categories:
        obj = Category(category=category['category'],
                    abbreviation=category['abbreviation'])
        obj.save()

def migrate_masters_stud():
    stud_types = db.execute("SELECT * FROM Stud_Types ORDER BY id").fetchall()

    for stud_type in stud_types:
        obj = Stud_Type(type=stud_type['stud_type'],
                    latin_name=stud_type['latin_name'],
                    hindi_name=stud_type['hindi_name'],
                    precious=stud_type['precious'],
                    abbreviation=stud_type['abbreviation'])
        obj.save()

    units = db.execute("SELECT * FROM Units ORDER BY id").fetchall()
    for unit in units:
        obj = Unit(unit=unit['unit'],
                    symbol=unit['symbol'],
                    value_gram=unit['value_gram'])
        obj.save()

def migrate_stock():
    vendors = db.execute("SELECT * FROM Vendors ORDER BY id").fetchall()
    for vendor in vendors:
        obj = Vendor(name=vendor['name'],
                    firm=vendor['firm'],
                    contact=vendor['contact'],
                    email=vendor['email'],
                    old_id=vendor['old_id'],
                    old_description=vendor['old_description'])
        obj.save()

    products = db.execute("SELECT * FROM Products ORDER BY id").fetchall()
    for product in products:
        obj = Product(register_id= None if product['register_id'] == "" else product['register_id'],
                    metal=Metal.objects.get(pk=product['metal']),
                    purity_id=product['purity'], # TODO: Handle case for purity 0
                    type=Type.objects.get(pk=product['type']),
                    category=Category.objects.get(pk=product['category']),
                    pieces=product['pieces'],
                    gross_weight=product['gross_weight'],
                    studs_weight=product['studding'],
                    less_weight=product['less_weight'],
                    net_weight=product['net_weight'],
                    calculation=product['calculation'],
                    making_charges= 0.0 if product['making_charges'] == "" else float(product['making_charges']),
                    wastage= 0.0 if product['wastage'] == "" else float(product['wastage']),
                    mrp= 0.0 if product['mrp'] == "" else float(product['mrp']),
                    description=product['description'],
                    vendor=Vendor.objects.get(pk=product['vendor_id']),
                    purchase_date=product['purchase_date'],
                    lot_number=product['lot_number'],
                    design_code=product['design_code'],
                    old_id=product['old_id'],
                    sold=int(product['sold']) == 1)
        obj.save()
        studs = db.execute("SELECT * FROM Product_Studs ORDER BY id").fetchall()
        for stud in studs:
            obj = Stud(product=Products.objects.get(pk=stud['product_id']),
                        type=Stud_Type.objects.get(stud['stud_type']),
                        less=int(stud['less']) == 1,
                        colour=stud['colour'],
                        shape=stud['shape'],
                        quantity=stud['quantity'],
                        weight=stud['weight'],
                        unit=Unit.objects.get(stud['unit']),
                        rate=stud['rate'],
                        value=stud['value'])
            obj.save()

def migrate_invoice():
    invoices = db.execute("SELECT * FROM Bills ORDER BY id").fetchall()
    for invoice in invoices:
        obj1 = Customer(name=invoice["name"]
                    firm=invoice['firm'],
                    pan=invoice['pan'],
                    gst=invoice['gst'],
                    aadhar=invoice['aadhar'],
                    contact=invoice['contact'],
                    email=invoice['email'],
                    address=invoice['address'],
                    pincode=invoice['pincode'],
                    city=invoice['city'],
                    state=invoice['state'],
                    country=invoice['country'])
        obj1.save()
        obj2 = Invoice(invoice_number=invoice["bill_number"]
                    date=invoice['date'],
                    gst_invoice=invoice['gst_invoice'],
                    gst_state=GST_State.objects.get(pk=invoice['gst_state']),
                    subtotal=invoice['aadhar'],
                    sgst=invoice['contact'],
                    cgst=invoice['email'],
                    igst=invoice['address'],
                    tcs=invoice['pincode'],
                    total=invoice['total'],
                    customer=obj1
                    rates=invoice['rates'])
        obj2.save()

def migrate_home_sale():
    home_sales = db.execute("SELECT * FROM Home_Sales ORDER BY id").fetchall()
    for home_sale in home_sales:
        obj = Home_Sale(date=home_sale['date'])
        obj.save()

    home_sale_products = db.execute("SELECT * FROM Home_Sale_Products ORDER BY id").fetchall()
    for home_sale_product in home_sale_products:
        obj = Product.objects.get(pk=home_sale_product["product_id"])
        obj.home_sale = Home_Sale.objects.get(pk=home_sale_product["home_sale_id"])
        obj.save()

migrate_masters_gst()
migrate_masters_product()
migrate_masters_stud()
migrate_stock()
