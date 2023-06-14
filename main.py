import requests
import bs4
import json


def get_data_part(page_num):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    response = requests.get(
        'https://spb.hh.ru/search/vacancy?text=python+Django+Flask&area=1&area=2&st=vacancy_simple&page=' + str(
            page_num), headers=headers)
    bs = bs4.BeautifulSoup(response.text, 'lxml')
    sc = bs.find("div", id="a11y-main-content")
    return sc.findAll("div", class_="vacancy-serp-item-body__main-info")


if __name__ == '__main__':
    vacancy_list = []
    page = 0
    chunk = get_data_part(page)
    while len(chunk) > 0:
        for part in chunk:
            link = part.findNext("a", class_="serp-item__title")
            vHref = link["href"]
            vTitle = link.text
            zp = part.findNext("span", class_="bloko-header-section-3")
            if zp is not None:
                vilkaZp = zp.text
            else:
                vilkaZp = "не указана"
            vAddress = part.findNext("div", class_="vacancy-serp-item__info").contents[1].text
            # если нужен фильтр по зарплатам в баксах
            # if vilkaZp.__contains__("$") or vilkaZp.__contains__("USD"):
            vacancy_list.append({'Title': vTitle, 'href': vHref, 'Salary': vilkaZp, 'Address': vAddress})
        page += 1
        chunk = get_data_part(page)

    json = json.dumps(vacancy_list)
    with open('data.json', 'w') as f:
        f.write(json)
