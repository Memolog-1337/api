from rest_framework.decorators import api_view
from rest_framework.response import Response

from .parser import StealthBrowser

QUEST_URL: str = 'https://www.mouser.com/c/?q='
MOUSER_URL: str = 'https://www.mouser.com'


@api_view(['GET'])
def get_eccn(request, partnumber):
    browser = StealthBrowser()

    if '#' in partnumber:
        partnumber_for_url = partnumber.split('#')
        partnumber_for_url = partnumber_for_url[0]
        browser.get_url(QUEST_URL + partnumber_for_url)
    elif '+' in partnumber:
        partnumber_for_url = partnumber.split('+')
        partnumber_for_url = partnumber_for_url[0]
        browser.get_url(QUEST_URL + partnumber_for_url)
    else:
        browser.get_url(QUEST_URL + partnumber)

    soup = browser.get_soup_info()

    result_eccn = False
    count = 0

    while not result_eccn and count <= 10:
        result_eccn = what_page(partnumber, soup, browser)
        count += 1
        if count == 10:
            return Response({'ECCN': 'Не пускает('})

    browser.browser.close()

    return Response({'ECCN': result_eccn})


def what_page(partnumber, soup, browser):
    is_main_page = soup.find('div', id='pdpMainContentDiv')

    if is_main_page:
        return check_eccn(soup, partnumber)

    is_result_page = soup.find('div', id='searchResultsTbl')

    if is_result_page:
        return result_page(partnumber, soup, browser)

    is_error_page = soup.find('div', class_='alert-danger')

    if is_error_page:
        return 'No ECCN'

    return False


def result_page(partnumber, soup, browser):
    results = soup.findAll('a', class_='text-nowrap')
    for result in results:
        result_text = result.text.strip()
        if partnumber == result_text:
            result_url = result['href']
            browser.get_url(MOUSER_URL + result_url)
            soup = browser.get_soup_info()
            return what_page(partnumber, soup, browser)


def check_eccn(soup, partnumber):

    partnumber_on_page = soup.find('div', id='pdpProdInfo')
    partnumber_on_page = partnumber_on_page.find('h1', class_='panel-title')
    partnumber_on_page = partnumber_on_page.text.strip()

    compliance_table = soup.find('div', class_='compliance-table')

    if not compliance_table or partnumber != partnumber_on_page:
        return 'No ECCN'

    compliances = compliance_table.findAll('dt')

    for index, compliance in enumerate(compliances):
        compliance = compliance.text.strip()
        if 'ECCN' in compliance:
            compliance_code = compliance_table.findAll('dd')
            return compliance_code[index].text.strip()
