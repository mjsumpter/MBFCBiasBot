def url_to_domain(urlstring):

    domain = urlstring

    str_to_remove = "http://"

    index = domain.find(str_to_remove)
    if index != -1:
        domain = domain[index + len(str_to_remove):]

    str_to_remove = "https://"
    index = domain.find(str_to_remove)
    if index != -1:
        domain = domain[index + len(str_to_remove):]

    str_to_remove = "www."
    index = domain.find(str_to_remove)
    if index != -1:
        domain = domain[index + len(str_to_remove):]

    str_to_remove = "m."
    index = domain.find(str_to_remove)
    if index != -1:
        domain = domain[index + len(str_to_remove):]

    str_to_remove = '/'
    index = domain.find(str_to_remove)
    if index != -1:
        domain = domain[:index]

    return domain
