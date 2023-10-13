import frappe
import io
import os
from erpnext import get_default_company
from frappe import _
from pyqrcode import create as qr_create
from base64 import b64encode
import datetime 
from frappe.utils import today

def generate_qr_code(doc,method):
    # Setting Expiry date for qr code 
    full_data = doc.qr_code_url
    qr_image = io.BytesIO()
    url = qr_create(full_data)
    url.png(qr_image, scale=2, quiet_zone=1)
    name = frappe.generate_hash(doc.name, 5)
    filename = f"QRCode-{name}.png".replace(os.path.sep, "__")

    _file = frappe.get_doc(
			{
				"doctype": "File",
				"file_name":filename,
				"is_private": 0,
				"content": qr_image.getvalue(),
				"attached_to_doctype": "Purchase Order",
				"attached_to_name":doc.name,
                "attached_to_field": "qr_image",
			}
		)

    _file.save()

    # assigning to document
    doc.db_set("qr_image", _file.file_url)



def convert_number(doc,method):
    words = money_in_words_arabic(doc.grand_total, doc.currency)
    doc.custom_in_wordsarabic = words
    doc.save()


def money_in_words_arabic(
    number: str | float | int,
    main_currency: str | None = None,
    fraction_currency: str | None = None,
):
    """
    Returns string in Arabic words with currency and fraction currency.
    """
    from frappe.utils import get_defaults, flt, cint

    try:
        # note: `flt` returns 0 for invalid input and we don't want that
        number = float(number)
    except ValueError:
        return ""

    number = flt(number)
    if number < 0:
        return ""

    d = get_defaults()
    if not main_currency:
        main_currency = d.get("currency", "INR")
    if not fraction_currency:
        fraction_currency = frappe.db.get_value("Currency", main_currency, "fraction", cache=True) or _(
            "Cent"
        )

    fraction_length = get_number_format_info("#,###.##")[2]

    n = f"%.{fraction_length}f" % number

    numbers = n.split(".")
    main, fraction = numbers if len(numbers) > 1 else [n, "00"]

    if len(fraction) < fraction_length:
        zeros = "0" * (fraction_length - len(fraction))
        fraction += zeros

    in_million = True
    if get_number_format_info("#,##,###.##")[0] == "":
        in_million = False

    # 0.00
    if main == "0" and fraction in ["00", "000"]:
        out = in_words(0, in_million).title() + " " + _("ريال سعودي", context="Currency")
    # 0.XX
    elif main == "0":
        out = in_words(fraction, in_million).title() + " " + "هللة"
    else:
        out = in_words(main, in_million).title() + " " + _("ريال سعودي", context="Currency")
        if cint(fraction):
            out = (
                out
                + " "
                + _("و")
                + " "
                + in_words(fraction, in_million).title()
                + " "
                + "هللة"
            )

    return out

#
# convert number to words
#
def in_words(integer: int, in_million=True) -> str:
    """
    Returns string in words for the given integer.
    """ 
    from num2words import num2words

    integer = int(integer)
    try:
        ret = num2words(integer, lang="ar")
    except NotImplementedError:
        ret = num2words(integer, lang="ar")
    except OverflowError:
        ret = num2words(integer, lang="ar")
    return ret.replace("-", " ")

number_format_info = {
    "#,###.##": (".", ",", 2),
    "#.###,##": (",", ".", 2),
    "# ###.##": (".", " ", 2),
    "# ###,##": (",", " ", 2),
    "#'###.##": (".", "'", 2),
    "#, ###.##": (".", ", ", 2),
    "#,##,###.##": (".", ",", 2),
    "#,###.###": (".", ",", 3),
    "#.###": ("", ".", 0),
    "#,###": ("", ",", 0),
    "#.########": (".", "", 8),
}


def get_number_format_info(format: str) -> tuple[str, str, int]:
    return number_format_info.get(format) or (".", ",", 2)
