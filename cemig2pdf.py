from operator import is_
import click, json
import cemigweb
from settings import CEMIG_USERNAME, CEMIG_PASSWORD

customer = cemigweb.Customer(CEMIG_USERNAME, CEMIG_PASSWORD)

@click.command()
@click.option('--site', '-s', default=0, help='Site number')
@click.option('--pdf', '-p', default=False, help='Get PDF', is_flag=True)
@click.option('--identifier', '-i' , default=None, help='Bill identifier')
@click.option('--all', '-a', default=False, help='Get all bills', is_flag=True)

def main(site,pdf,identifier,all):
    if site:
        site = str(site)
    if pdf and site and identifier:
        get_pdf(site, identifier)
    elif site and identifier:
        get_bill_details(site, identifier)
    elif site:
        get_bills(site, all)
    else:
        get_sites()
        
def get_bill_details(site, identifier):
    print(json.dumps(customer.get_bill_details(customer.sites[site]['id'], identifier), indent=4))

def get_pdf(site, identifier):
    customer.get_bill_pdf(customer.sites[site], identifier)
    print(f'PDF saved as conta-{site}-{identifier}.pdf')
        
def get_bills(site, all=False):
    bills_history = customer.get_bills_history(customer.sites[site])
    bills = [{'referenceMonth': bill['referenceMonth'],
              'billIdentifier': bill['billIdentifier'], 
              'status': bill['status'],
              'value': bill['value'], 
              'dueDate': bill['dueDate']} for bill in bills_history]
    if not all:
        bills = [bill for bill in bills if bill['status'] != 'Paid']
    print(json.dumps(bills, indent=4))
    
def get_sites():
    print(json.dumps(customer.sites, indent=4))
    
    
if __name__ == '__main__':
    main()