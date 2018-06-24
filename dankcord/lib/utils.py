def format_money(number):
    if number >= 1000000000:
        return "%s bil" % "{:,.0f}".format(number/1000000000)
    else:
        return "{:,.0f}".format(number)

def format_number(number):
    return "{:,.0f}".format(number)
