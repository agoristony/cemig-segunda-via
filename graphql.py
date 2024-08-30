GRAPHQL_QUERIES = {
    'siteList':['SiteListByBusinessPartnerV2', 'query SiteListByBusinessPartnerV2($input: SiteListByBusinessPartnerV2InputDTO!) {\n  siteListByBusinessPartnerV2(input: $input) {\n    sites {\n      id\n      owner\n      clientNumber\n      siteNumber\n      address\n      status\n      contract\n      contractAccount\n      classSubClassDescription\n      siteType\n    }\n    pagesCount\n    sitesCount\n  }\n}\n'],
    'billsHistory': ['BillsHistory', 'query BillsHistory($input: BillsHistoryInputDTO!) {\n  billsHistory(input: $input) {\n    bills {\n      billIdentifier\n      status\n      value\n      referenceMonth\n      site {\n        id\n        contract\n        siteNumber\n        contractAccount\n        clientNumber\n      }\n      dueDate\n      consumption\n      documentContractAccount\n    }\n  }\n}\n'],
    'getConsumptionHistory': ['getConsumptionHistory', 'query getConsumptionHistory($input: BillsHistoryInputDTO!) {\n  getConsumptionHistory(input: $input) {\n    bills {\n      billIdentifier\n      referenceMonth\n      consumption\n      dailyConsumption\n      billableDays\n    }\n  }\n}\n'],
    'billDetails': ['BillsDetails', 'query BillsDetails($billsDetailsInput: BillDetailsInputDTO!) {\n  billDetails(input: $billsDetailsInput) {\n    bills {\n      value\n      consumption\n      barCode\n      pix\n      debtLockCode\n      debtLockDescription\n      composition {\n        description\n        value\n        percentValue\n      }\n      billIdentifier\n      dueDate\n      referenceMonth\n      comparativeBoard {\n        period\n        readingType\n        billableDays\n        installment\n        fine\n        otherValues\n        streetLighting\n        dailyConsumption\n        monthlyConsumption\n        icms\n        compensations\n        fees\n        restitutions\n        class\n        billableDaysThreeMonths\n        installmentThreeMonths\n        fineThreeMonths\n        otherValuesThreeMonths\n        streetLightingThreeMonths\n        dailyConsumptionThreeMonths\n        monthlyConsumptionThreeMonths\n        icmsThreeMonths\n        compensationsThreeMonths\n        feesThreeMonths\n        restitutionsMonths\n        classThreeMonths\n      }\n      billingData {\n        price\n        description\n        quantity\n        amount\n      }\n      comparativeInfos {\n        description\n        value\n        valueLastThreeMonths\n        comparative\n        classComparative {\n          actual\n          previous\n        }\n        details {\n          monthYearReference\n          text\n        }\n      }\n    }\n  }\n}\n'],
    'billPDF': ['BillPDF', 'query BillPDF($billPDFInput: BillDetailsInputDTO!) {\n  billPDF(input: $billPDFInput) {\n    pdfBase64\n  }\n}\n'],
}

def site_list_query():
    return GRAPHQL_QUERIES['siteList'] + [{"input":{"pageNumber":1,"pageSize":10}}]

def bills_history_query(siteId):
    return GRAPHQL_QUERIES['billsHistory'] + [{"input":{"siteId":siteId}}]

def get_consumption_history_query(siteId):
    return GRAPHQL_QUERIES['getConsumptionHistory'] + [{"input":{"siteId":siteId}}]

def bill_details_query(siteId, billIdentifier):
    return GRAPHQL_QUERIES['billDetails'] + [{"billsDetailsInput":{"siteId":siteId,"billIdentifier":billIdentifier}}]

def bill_pdf_query(siteId, billIdentifier):
    return GRAPHQL_QUERIES['billPDF'] + [{"billPDFInput":{"siteId":siteId,"billIdentifier":billIdentifier}}]

def graphql_query(client, operationName, query, variables):
        url = 'https://www.atendimento.cemig.com.br/graphql'
        json_data = {
            'query': query,
            'variables': variables,
            'operationName': operationName,
        }
        response = client.post(url, json=json_data)
        return response.json()