#! usr/bin/python3

# open_links.py - Downloads every available link for a given
# url. Reports any links that have 404 status codes and prints
# them to the console.

# USAGE: python3 open_links.py <web url> - For a given <web url>,
# searches for all url links on that web page. Each url link
# is downloaded unless it has a 404 status code, in which case,
# it is flagged and printed onto the console.


import bs4, requests, os, sys


def get_web_url_html():

    """This function checks if the command line arguments contain
    a valid web url to download. It will check if the web url
    in the command line can be accessed and return it in https
    format if it is valid. Otherwise, it will prompt the user
    to input url links until the format is acceptable.
    """

    valid_url = False
    # If no url is given, prompt user for url link until valid
    # link is given
    if len(sys.argv) < 2:
        while not valid_url:
            url_input = input('Enter a web url address to download links for: ')
            if url_input.startswith('http'):
                web_url = url_input
            else:
                web_url = 'http://' + url_input
            try:
                url_data = requests.get(web_url)
                url_data.raise_for_status()
                valid_url = True
                print('The web url: %s is valid.' % web_url)

            except Exception as err:
                print('The link provided is not valid.')
                print('An error has occurred: %s' % err)
                print('Please provide a different web url.')
        print('Web url data has been obtained. Preparing to download links...')
        return web_url, url_data

    # Take the web url from the command line and attempt to
    # connect to the web url. If unsuccessful, prompt the user
    # for new url inputs until a valid one is found.
    else:
        url_input = sys.argv[1]
        while not valid_url:
            if url_input.startswith('http'):
                web_url = url_input
            else:
                web_url = 'http://' + url_input
            try:
                url_data = requests.get(web_url)
                url_data.raise_for_status()
                valid_url = True
                print('The web url: %s is valid.' % web_url)

            except Exception as err:
                print('The link provided is not valid.')
                print('An error has occurred: %s' % err)
                print('Please provide a different web url.')
                url_input = input('Enter a web url to download links for: ')
        print('Web url data has been obtained. Preparing to download links...')
        return web_url, url_data


def get_link_data(url_address, page_data):

    """Gets a list of all of the links on a web page for the
    url address. For each link, download the linked page. For
    links that have a 404 status code, flag the link.
    """

    # Make a soup object from the downloaded web url page.
    # Obtain the html elements that contain urls to other pages.
    print('Preparing to download the links for the web url: %s' % url_address)
    web_url_soup_object = bs4.BeautifulSoup(page_data.text, "lxml")
    link_elem= web_url_soup_object.select('a[href]')
    if len(link_elem) == 0:
        sys.exit('No links could be downloaded for the web url: %s' % url_address)
    else:
        # Create a Desktop folder to store the downloaded links
        folder_name_path = os.path.join((os.getenv('HOME') + '/Desktop'), 'Link_Data')
        os.makedirs(folder_name_path, exist_ok=True)
        print('This file contains the downloaded links for: ' + url_address + '\n')
        # For each link element, attempt to download linked
        # page data to a html file in the created folder
        for index in range(len(link_elem)):
            try:
                href = link_elem[index].get('href')
                href_data = requests.get(href)
                href_data.raise_for_status()
                print('\n')
                href_soup = bs4.BeautifulSoup(href_data.text, "lxml")
                title_elem = href_soup.select('title')
                file_name = title_elem[0].getText()
                file_name_path = os.path.join((os.getenv('HOME') + '/Desktop' + '/Link_Data'), (file_name + '.html'))
                with open(file_name_path, 'wb') as file_handler:
                    for chunk in href_data.iter_content(100000):
                        file_handler.write(chunk)
                print('The link: %s has been successfully downloaded to: %s' % (href, file_name_path))

            except Exception as err:
                print('An error has occurred: %s' % err)
                print('FLAG: The link: %s could not be downloaded.' % href)
                print('\n' + 'This link has a 404 status code.\n')

        print('The links have finished downloading.')
        sys.exit('Exiting now.')


# Obtain the url for the web page to download links for
main_url, main_url_data = get_web_url_html()
get_link_data(main_url, main_url_data)