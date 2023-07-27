import requests
from manage_api_config import call_header, manage_url

query_url = f"https://{manage_url}/v4_6_release/apis/3.0/finance/agreements"


class Agreement:
    def __init__(self, agr):
        self.id = agr["id"]
        self.name = agr["name"]
        self.type = agr["type"]["name"]
        self.company = agr["company"]["name"]
        self.additions = []

    def __str__(self):
        return f"Agreement Name:  {self.name} \nType:  {self.type} \nCompany:  {self.company}\nID:  {self.id}\n"

    def get_additions(self):
        addition_url = f'https://{manage_url}/v4_6_release/apis/3.0/finance/agreements/{str(self.id)}/additions?conditions=invoiceDescription contains ",Unassigned Licenses:"'
        r = requests.get(addition_url, headers=call_header)
        addition_list = r.json()  # List of agreement additions, each is a dict

        for addition in addition_list:
            self.additions.append(Addition(addition))


class Addition:
    def __init__(self, addition):
        self.id = addition["id"]
        # self.product = addition["id"]["identifier"]
        self.description = addition["invoiceDescription"]

    def __str__(self):
        return f"ID: {self.id}\nDescription: {self.description}\n\n"

    def truncate_note(self):
        invoicedesc = self.id


def get_agreements():
    r = requests.get(query_url, headers=call_header)
    agreement_list = r.json()  # List of agreement additions, each is a dict
    return agreement_list


def truncate_addition_notes(agreement):
    agr = Agreement(agreement)
    agr.get_additions()

    for addition in agr.additions:
        newtext, seperator, stripped = addition.description.partition(
            "\n,Unassigned Licenses:"
        )

        addition_url = f"https://{manage_url}/v4_6_release/apis/3.0/finance/agreements/{str(agr.id)}/additions/{str(addition.id)}"

        body = '[{"op": "replace", "path": "/invoiceDescription", "value":"'
        body += newtext
        body += '"}]'

        r = requests.patch(addition_url, headers=call_header, data=body)


if __name__ == "__main__":

    for agreement in get_agreements():
        truncate_addition_notes(agreement)
