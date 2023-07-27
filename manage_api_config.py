import base64

manage_url = ""
companyid = ""
clientid = ""
publickey = ""
privatekey = ""


def generate_token(companyid, publickey, privatekey):
    token = "{}+{}:{}".format(companyid, publickey, privatekey)
    token = base64.b64encode(bytes(token, "utf-8"))
    token = token.decode("utf-8")
    return token


call_header = {
    "Authorization": "Basic " + generate_token(companyid, publickey, privatekey),
    "clientId": clientid,
    "Content-Type": "application/json",
}
