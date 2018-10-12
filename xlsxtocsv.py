import xlrd
import csv

def csv_from_excel():
    wb = xlrd.open_workbook('C:\\Users\sauravkhandelwal\Desktop\Scraper\LinksSAP.xlsx')
    sh = wb.sheet_by_name('Sheet1')
    link = open('link.csv', 'w')
    wr = csv.writer(link, quoting=csv.QUOTE_ALL)

    for rownum in range(sh.nrows):
        wr.writerow(sh.row_values(rownum))

    link.close()

# runs the csv_from_excel function:
csv_from_excel()