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

    new_metal = Metal(metal="None",
                    symbol=None,
                    colour=None,
                    melting_point=None,
                    boiling_point=None,
                    density=None)
    new_metal.save()

    purities = db.execute("SELECT * FROM Purities ORDER BY id").fetchall()
    for purity in purities:
        obj = Purity(purity=purity['purity'],
                    karatage=purity['karatage'],
                    display_name=purity['display_name'])
        obj.save()
    
    new_purity = Purity(purity=0.00,
                    karatage='0KT',
                    display_name=" ")
    new_purity.save()

    types = db.execute("SELECT * FROM Types ORDER BY id")
    for type in types:
        obj = Type(type=type['type'],
                    hsn=HSN.objects.get(pk=type['hsn_id']),
                    abbreviation=type['abbreviation'])
        obj.save()
    
    new_type = Type(type="None",
                    hsn=HSN.objects.get(code=7113),
                    abbreviation='NA')
    new_type.save()

    categories = db.execute("SELECT * FROM Categories ORDER BY id").fetchall()
    for category in categories:
        obj = Category(category=category['category'],
                    abbreviation=category['abbreviation'])
        obj.save()

    new_category = Category(category="None",
                    abbreviation="None")
    new_category.save()

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

    new_vendor = Vendor(name="None",
                    firm="",
                    contact="",
                    email="",
                    old_id="",
                    old_description="")
    new_vendor.save()

    products = db.execute("SELECT * FROM Products ORDER BY id").fetchall()
    for product in products:
        # TODO: Take care of blank entries in the db.
        obj = Product(register_id= product['register_id'],
                    metal=Metal.objects.get(metal="None") if product['metal'] == '' else Metal.objects.get(pk=product['metal']),
                    purity = Purity.objects.get(purity=0.00) if product['purity'] == '' or product['purity']=='0' else Purity.objects.get(pk=product['purity']),
                    type=Type.objects.get(type='None') if product['type'] == '' else Type.objects.get(pk=product['type']),
                    category=Category.objects.get(category="None") if product['category'] == '' else Category.objects.get(pk=product['category']),
                    pieces=0 if product['pieces']=='' else product['pieces'],
                    gross_weight=0.00 if product['gross_weight']=='' else product['gross_weight'],
                    studs_weight=product['studding'], #TODO: studs_weight calculated
                    less_weight=product['less_weight'], #TODO: less_weight calculated
                    net_weight=product['net_weight'], #TODO: net_weight calculated
                    rate=5100.00 if product['rate'] == "" else float(product['rate']), #TODO: Take care of blank entries of rate (maybe using date?)
                    calculation="Making Charges" if product['calculation'] == '' else product['calculation'],
                    making_charges=None if product['making_charges'] == "" else float(product['making_charges']),
                    wastage=None if product['wastage'] == "" else float(product['wastage']),
                    mrp=None if product['mrp'] == "" else float(product['mrp']),
                    description=product['description'],
                    vendor=Vendor.objects.get(name='None') if product['vendor_id'] == '' else Vendor.objects.get(pk=product['vendor_id']), #TODO: Take care of products without a vendor
                    purchase_date=product['purchase_date'],
                    lot_number= None if product['lot_number'] == '' else product['lot_number'],
                    design_code=product['design_code'],
                    old_id=product['old_id'],
                    sold=int(product['sold']) == 1)
        obj.save()
        studs = db.execute("SELECT * FROM Product_Studs ORDER BY id WHERE product_id=?", (product.pk,)).fetchall()
        for stud in studs:
            obje = Stud(product=Product.objects.get(pk=stud['product_id']),
                        type=Stud_Type.objects.get(pk=stud['type']),
                        less=int(stud['less']) == 1,
                        colour=stud['colour'],
                        shape=stud['shape'],
                        quantity=1 if stud['quantity'] == "" else stud["quantity"],
                        weight=stud['weight'],
                        unit=Unit.objects.get(pk=stud['unit']),
                        rate=0.0 if stud['rate'] == "" else stud["rate"],
                        value=0.0 if stud['value'] == "" else stud["value"])
            obje.save()

def migrate_invoice():
    invoices = db.execute("SELECT * FROM Bills ORDER BY id").fetchall()
    for invoice in invoices:
        obj1 = Customer(name=invoice["name"],
                    firm=invoice['firm'],
                    pan=invoice['pan'],
                    gst=invoice['gst'],
                    aadhar="",
                    contact=invoice['contact'],
                    email=invoice['email'],
                    address=invoice['address'],
                    pincode=invoice['pincode'],
                    city=invoice['city'],
                    state=GST_State.objects.get(state=invoice["state"]) if invoice["state"] != "" else GST_State.objects.get(pk=invoice["gst_state"]),
                    country="India")
        obj1.save()
        obj2 = Invoice(invoice_number=invoice["bill_number"],
                    date=invoice['date'],
                    gst_invoice=invoice['gst_bill'],
                    gst_state=GST_State.objects.get(pk=invoice['gst_state']),
                    subtotal=invoice['subtotal'],
                    sgst=invoice['sgst'],
                    cgst=invoice['cgst'],
                    igst=invoice['igst'],
                    tcs=invoice['tcs'],
                    total=invoice['total'],
                    customer=obj1,
                    rates=invoice['rates'])
        obj2.save()
    
    invoice_untagged = db.execute("SELECT * FROM Bill_Untagged ORDER BY id").fetchall()
    for product in invoice_untagged:
        obj = Untagged(invoice=Invoice.objects.get(pk=product["bill_id"]),
                    metal=Metal.objects.get(pk=product['metal']),
                    purity_id=product['purity'],
                    type_id=2,
                    category=Category.objects.get(pk=product['category']),
                    gross_weight=0.0 if product['gross_weight']=="" else product["gross_weight"],
                    less_weight=0.0 if product['less_weight']=="" else product["less_weight"],
                    net_weight=0.0 if product['net_weight']=="" else product["net_weight"])
        obj.save()

    invoice_products = db.execute("SELECT * FROM Bill_Products ORDER BY id").fetchall()
    for invoice_product in invoice_products:
        obj = Invoice_Product(invoice_id=invoice_product["bill_id"],
                                product_id=invoice_product["product_id"])
        obj.save()

def migrate_home_sale():
    home_sales = db.execute("SELECT * FROM Home_Sales ORDER BY id").fetchall()
    for home_sale in home_sales:
        obj = Home_Sale(date=home_sale['date'])
        obj.save()

        home_sale_products = db.execute("SELECT * FROM Home_Sale_Products ORDER BY id WHERE home_sale_id=?", (home_sale.pk,)).fetchall()
        for home_sale_product in home_sale_products:
            obj = Home_Sale_Product(home_sale_id=home_sale_product["home_sale_id"],
                                    product_id=home_sale_product["product_id"])
            obj.save()

def migrate_advance():
    advances = db.execute("SELECT * FROM Advances ORDER BY id").fetchall()
    for advance in advances:
        obj1 = Customer(name=advance["name"],
                    firm=advance['firm'],
                    pan=advance['pan'],
                    gst=advance['gst'],
                    aadhar="",
                    contact=advance['contact'],
                    email=advance['email'],
                    address=advance['address'],
                    pincode=advance['pincode'] or "",
                    city=advance['city'] or "",
                    state = GST_State.objects.get(state=invoice["state"]) if invoice["state"] != "" else "",
                    country="India")
        obj1.save()
        obj2 = Advance(date=advance['date'], customer=obj1)
        obj2.save()

    bill_advances = db.execute("SELECT * FROM Bill_Advances ORDER BY id").fetchall()
    for bill_advance in bill_advances:
        advance = Advance.objects.get(pk=bill_advance["advance_id"])
        advance.invoice = Invoice.objects.get(pk=bill_advance["bill_id"])
        advance.redeemed = True
        advance.save()

def migrate_payment():
    payments = db.execute("SELECT * FROM Bill_Payments ORDER BY id")
    for payment in payments:
        obj = Payment(method=payment["method"],
                    amount=payment["amount"],
                    date=payment["date"],
                    name=payment["name"],
                    card_bank=payment["card_bank"],
                    card_number=payment["card_number"],
                    cheque_number=payment["cheque_number"],
                    cheque_branch=payment["cheque_branch"],
                    cheque_account_number=payment["cheque_account_number"],
                    cheque_ifsc=payment["cheque_ifsc"],
                    upi_vpa=payment["upi_vpa"],
                    upi_mobile=payment["upi_mobile"],
                    wire_account_number=payment["wire_account_number"],
                    wire_utr=payment["wire_utr"],
                    wire_bank=payment["wire_bank"],
                    invoice=Invoice.objects.get(pk=payment["bill_id"]))
        obj.save()

        payments = db.execute("SELECT * FROM Advance_Payments ORDER BY id")
        for payment in payments:
            obj = Payment(method=payment["method"],
                        amount=payment["amount"],
                        date=payment["date"],
                        name=payment["name"],
                        card_bank=payment["card_bank"],
                        card_number=payment["card_number"],
                        cheque_number=payment["cheque_number"],
                        cheque_branch=payment["cheque_branch"],
                        cheque_account_number=payment["cheque_account_number"],
                        cheque_ifsc=payment["cheque_ifsc"],
                        upi_vpa=payment["upi_vpa"],
                        upi_mobile=payment["upi_mobile"],
                        wire_account_number=payment["wire_account_number"],
                        wire_utr=payment["wire_utr"],
                        wire_bank=payment["wire_bank"],
                        advance=Advance.objects.get(pk=payment["advance_id"]))
            obj.save()

def migrate_vouchers():
    vouchers = db.execute("SELECT * FROM Vouchers ORDER BY id").fetchall()
    for voucher in vouchers:
        obj1 = Customer(name=voucher["name"],
                    firm=voucher['firm'],
                    pan=voucher['pan'],
                    gst=voucher['gst'],
                    aadhar=voucher['aadhar'],
                    contact=voucher['contact'],
                    email=voucher['email'],
                    address=voucher['address'],
                    pincode=voucher['pincode'],
                    city=voucher['city'],
                    state=GST_State.objects.get(state=invoice["state"]) if invoice["state"] != "" else "",
                    country=voucher['country'])
        obj1.save()
        obj2 = Voucher(voucher_number=voucher["voucher_number"],
                    type=voucher["type"],
                    date=voucher["date"],
                    gross_weight=voucher["gross_weight"],
                    net_weight=voucher["net_weight"],
                    pure_weight=voucher["pure_weight"],
                    amount=voucher["amount"],
                    customer=obj1)
        obj2.save()

    particulars = db.execute("SELECT * FROM Voucher_Particulars ORDER BY id").fetchall()
    for particular in particulars:
        obj = Particular(voucher=Voucher.objects.get(pk=particular["voucher_id"]),
                        metal=Metal.objects.get(pk=particular["metal"]),
                        purity=Purity.objects.get(pk=particular["purity"]),
                        category=Category.objects.get(pk=particular["category"]),
                        gross_weight=particular["gross_weight"],
                        net_weight=particular["net_weight"],
                        rate=particular["rate"],
                        subtotal=particular['subtotal'],
                        sgst=particular['sgst'],
                        cgst=particular['cgst'],
                        igst=particular['igst'],
                        tcs=particular['tcs'],
                        total=particular['total'])
        obj.save()

migrate_masters_gst()
migrate_masters_product()
migrate_masters_stud()
migrate_stock()
migrate_home_sale()
# migrate_payment()
# migrate_invoice()
# migrate_advance()
# migrate_vouchers()
