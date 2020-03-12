import requests
from bs4 import BeautifulSoup
import csv


def appending_links(url_list):
    """receiving links from txt file in same folder"""

    with open('list_of_links.txt', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            url_list.append(row[0])

        return url_list

def grp_link_srch(url):
    """use scrapped link to search for Mündener TC"""

    link_in_list = requests.get(url)  # saves the get request

    link_soup = BeautifulSoup(link_in_list.content, 'html5lib')

    link_table = link_soup.find('table', attrs={'class': 'result-set'})  # specific class in html body

    for row in link_table.find_all('a'):
        # string to search for in the given website
        if row.text == 'Mündener Tennisclub e. V.':  # first string to search for
            # print("True")
            return True
        elif row.text == 'TuS Schededörfer 04':  # second string to search for if necessary
            # print("True")
            return True
        else:
            continue


def find_grp_title(url):
    """getting the group title"""

    link_in_list = requests.get(url)  # saves the get request

    link_soup = BeautifulSoup(link_in_list.content, 'html5lib')

    link_table = link_soup.find(id='content-row2')  # specific class in html body

    for row in link_table.find_all('h1'): # get table title and strip it of whitespaces
        return(row.get_text('', strip=True).replace('TNB Sommer 2020',''))

    return


def main():
    """main func"""

    main_url = []

    appending_links(main_url) # func to append urls from txt file, returns list

    grp_links = [] # list for the final results

    for link in main_url:

        main_page = requests.get(link)

        soup = BeautifulSoup(main_page.content, 'html5lib')

        table = soup.find('table', attrs={'class': 'result-set'})  # specific table class to search for

        i = 0  # just for visual output and in case I want to stop it manually at a specific number of iterations

        for row in table.find_all('a'):
            i = i + 1
            grp_link = {}  # dict to save all groups in, more keys can be added
            if i % 50 == 0:
                print(i)
            # if i==60:
            #     break
            if grp_link_srch('https://tnb.liga.nu' + row.get('href')):
                title = find_grp_title('https://tnb.liga.nu' + row.get('href'))
                print(title)
                grp_link['Teams'] = title
                grp_links.append(grp_link)

            else:
                continue

    filename = 'hrefs.csv'
    with open(filename, 'w') as f:
        print("writing file")
        w = csv.DictWriter(f, ['Teams'])
        w.writeheader()
        for link in grp_links:
            w.writerow(link)


main()
