import requests

tenders = []


def appending_deals(database, id_n=1):
    # changing raw data to json type
    # id_n for numering tenders

    if database:
        database = database.json()

        def getting_deals(x):  # script to return valves from the tender

            return {
                "id": x,
                "ObjectId": deal.get("objectId"),
                "clientType": deal.get("clientType"),
                "TenderType": deal.get("TenderType"),
                "noticeType": deal.get("noticeType"),
                "noticeNumber": deal.get("noticeNumber"),
                "bzpNumber": deal.get("bzpNumber"),
                "isTenderAmountBelowEU": deal.get("isTenderAmountBelowEU"),
                "publicationDate": deal.get("publicationDate"),
                "orderObject": deal.get("orderObject"),
                "cpvCode": deal.get("cpvCode"),
                "submittingOffersDate": deal.get("submittingOffersDate"),
                "procedureResult": deal.get("procedureResult"),
                "organizationName": deal.get("organizationName"),
                "organizationCity": deal.get("organizationCity"),
                "organizationProvince": deal.get("organizationProvince"),
                "organizationCountry": deal.get("organizationCountry"),
                "organizationNationalId": deal.get("organizationNationalId"),
                "organizationId": deal.get("organizationId"),
                "tenderId": deal.get("tenderId"),
            }

        for deal in database:  # going through all tenders in list
            tenders.append(getting_deals(id_n))
            id_n = id_n + 1
        return tenders
    else:
        print("Error at appending tenders")


def extract(link):
        try:  # checking if eZam is available
            data = requests.get(link, timeout=10)
            data.raise_for_status()
            return data
        except requests.exceptions.Timeout:
            print("Network error.\nConnection to eZam timeout")
        except requests.exceptions.RequestException as error:
            print(f"{error} error")
