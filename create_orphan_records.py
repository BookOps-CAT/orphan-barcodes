# creates MARC records for ReCAP orphan barcodes problem


from pymarc import Record, Field, MARCWriter
import csv

fh_in = 'orphan_barcodes.csv'
fh_out = 'orphan_barcodes.mrc'


def create_bib(file, barcode, cust_code):
    # generates MARC records with barcode and customer code
    # entered in appropriate fields

    record = Record()

    # MARC record leader
    mat_type = 'a' # material type is a mandatory element and no option for unspecified type; 'a' type is for monographs
    record.leader = '00000n{}m a2200000u  4500'.format(
        mat_type)

    tags = []

    # title
    title = '{} orphan barcodes on file at ReCAP'.format(
        cust_code)
    tags.append(Field(
        tag='245',
        indicators=['0', '0'],
        subfields=['a', title]))

    # call number
    tags.append(Field(
        tag='852',
        indicators=['8', ' '],
        subfields=['h', barcode]))

    # Sierra format fields (949 tag)
    bcode3 = 'n'
    lang = '---'
    country = ''
    location = 'rc'
    cat_date = '---'
    skip = '0'  # can't find mapping for skip, let's see if any default setting on the load table will kick in to populate it
    bib_level = '-'
    mat_type = '-'

    tags.append(Field(
        tag='949',
        indicators=[' ', ' '],
        subfields=[
            'a', '*la={};cy={};bn={};ct={};b1={};b2={};b3={}'.format(
                lang,
                country,
                location,
                cat_date,
                bib_level,
                mat_type,
                bcode3)
        ]))

    # item tag 949
    tags.append(Field(
        tag='949',
        indicators=[' ', '1'],
        subfields=[
            'r', 's',  # ICODE2 (60) SUPPRESS
            't', '0',  # ITEM TYPE (61) Default
            'l', 'rc',  # LOCATION (79)
            'o', '2',  # OPACMSG (108) ADV REQUEST
            'h', '43',  # Agency (127)
            'i', barcode,  # barcode
            'z', '8528',  # 
            'a', barcode,  # CallNo
            'n', 'Barcode on file at ReCAP {} 2017/10/01'.format(cust_code)
        ]))

    # add MARC fields to record object
    for tag in tags:
        record.add_ordered_field(tag)

    # append newly created record to file
    writer = MARCWriter(open(file, 'a'))
    writer.write(record)
    writer.close()


with open(fh_in, 'r') as file:
    reader = csv.reader(file)
    reader.next()  # skip header row
    for row in reader:
        barcode = row[0]
        cust_code = row[1]
        create_bib(fh_out, barcode, cust_code)
