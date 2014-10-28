#!/usr/bin/env python

"""
mailroom assignment

This version uses a dict for the main db, and exception handling to
check input
"""

# handy utility to make pretty printing easier
from textwrap import dedent

import math

# In memory representation of the donor database
# using a tuple for each donor
# -- kind of like a record in a database table
# using a dict with a lower case version of the donor's name as the key
donor_db = {}
donor_db['william gates, iii'] = ("William Gates, III", [653772.32, 12.17])
donor_db['jeff bezos'] = ("Jeff Bezos", [877.33])
donor_db['paul allen'] = ("Paul Allen", [663.23, 43.87, 1.32])
donor_db['mark zuckerberg'] = ("Mark Zuckerberg", [1663.23, 4300.87, 10432.0])


def list_donors():
    """
    creates alist of the donors as a string, so tehy can be printed

    not calling print from here makes it more flexible and easier to
    test
    """
    listing = ["Donor list:"]
    for donor in donor_db.values():
        listing.append( donor[0] )
    return "\n".join(listing)


def find_donor(name):
    """
    find a donor in the donor db

    :param: the name of the donor

    :returns: The donor data structure -- None if not in the donor_db
    """
    key = name.strip().lower()
    return donor_db.get(key)


def add_donor(name):
    """
    add a new donor to the donr db

    :param: the name of the donor

    :returns: the new Donor data structure
    """
    name = name.strip()
    donor = (name, [])
    donor_db[name.lower()] = donor
    return donor


def main_menu_selection():
    """
    Print out the main application menu and then read the user input.
    """
    input = raw_input(dedent('''
      Choose an action:

      1 - Send a Thank You
      2 - Create a Report
      3 - Quit

      > '''))
    return input.strip()


def gen_letter(donor):
    """
    Generate a thank you letter for the donor

    :param: donor tuple

    :returns: string with letter
    """
    return dedent('''Dear %s

          Thank you for your very kind donation of %.2f.
          It will be put to very good use.

                         Sincerely,
                            -The Team
          ''' % (donor[0], donor[1][-1]) )


def send_thank_you():
    """
    Execute the logic to record a donation and generate a thank you message.
    """
    # Read a valid donor to send a thank you from, handling special commands to
    # let the user navigate as defined.
    while True:
        name = raw_input("Enter a donor's name (or list to see all donors or 'menu' to exit)> ").strip()
        if name == "list":
            print list_donors()
        elif name == "menu":
            return
        else:
            break

    # Now prompt the user for a donation amount to apply. Since this is
    # also an exit point to the main menu, we want to make sure this is
    # done before mutating the db .
    while True:
        amount_str = raw_input("Enter a donation amount (or 'menu' to exit)> ").strip()
        if amount_str == "menu":
            return
        # Make sure amount is a valid amount before leaving the input loop
        try:
            amount = float(amount_str)
            # extra check here -- unlikely that someone will type "NaN", but
            # it IS possible, and it is a valid floating point number:
            # http://en.wikipedia.org/wiki/NaN
            if math.isnan(amount) or math.isinf(amount) or round(amount, 2) == 0.00:
                raise ValueError
        # in this case, the ValueError could be raised by the float() call, or by the NaN-check
        except ValueError:
            print "error: donation amount is invalid\n"
        else:
            break

    # If this is a new user, ensure that the database has the necessary
    # data structure.
    donor = find_donor(name)
    if donor is None:
        donor = add_donor(name)

    # Record the donation
    donor[1].append(amount)
    print gen_letter(donor)


def sort_key(item):
    ## used to sort on name in donor_db
    return item[1]


def generate_donor_report():
    """
    Generate the report of the donors and amounts donated.

    :returns: the donor report as a string.
    """
    # First, reduce the raw data into a summary list view
    report_rows = []
    for (name, gifts) in donor_db.values():
        total_gifts = sum(gifts)
        num_gifts = len(gifts)
        avg_gift = total_gifts / num_gifts
        report_rows.append( (name, total_gifts, num_gifts, avg_gift) )

    #sort the report data
    report_rows.sort(key=sort_key)
    report = []
    report.append("%25s | %11s | %9s | %12s"%("Donor Name","Total Given","Num Gifts","Average Gift") )
    report.append("-"*66)
    for row in report_rows:
        report.append("%25s   %11.2f   %9i   %12.2f"%row)
    return "\n".join(report)

if __name__ == "__main__":
    running = True
    while running:
        selection = main_menu_selection()
        if selection is "1":
            send_thank_you()
        elif selection is "2":
            print generate_donor_report()
        elif selection is "3":
            running = False
        else:
            print "error: menu selection is invalid!"
