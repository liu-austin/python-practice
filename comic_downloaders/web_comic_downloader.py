#! usr/bin/python3
# web_comic_downloader.py - This script can download
# all of the comic images from Lunar Baboon, Moonbeard, and
# Wonderella.


import bs4, os, requests, threading


comic_names = ['Lunar Baboon', 'Moonbeard', 'Wonderella']  # Global list
comic_main_urls = {'Moonbeard': 'http://moonbeard.com',
                   'Wonderella': 'http://nonadventures.com',
                   'Lunar Baboon': 'http://lunarbaboon.com'}


def create_folders():

    """This function creates a main folder in Desktop that contains
    sub-folders for storing Lunar Baboon, Moonbeard, and Wonderella comics.
    The return value is a dictionary containing the paths of the
    comic subfolders."""

    # Make main folder and create sub-folders for each comic type.
    main_folder_path = os.path.join(os.path.join(os.getenv('HOME'), 'Desktop'), 'Comic_Folder')
    os.makedirs(main_folder_path, exist_ok=True)
    comic_subfolders = {}
    for comic_type in comic_names:
        comic_subfolder_path = os.path.join(main_folder_path, comic_type)
        comic_subfolders[comic_type] = comic_subfolder_path
        os.makedirs(comic_subfolder_path, exist_ok=True)

    return comic_subfolders


def download_all_comics():

    """This function attempts to download every comic image from XKCD,
    Moonbeard, and Wonderella and stores them in the comic folder on the
    Desktop. Comic images that cannot be downloaded are flagged on the
    console. Each comic image is downloaded in its separate thread."""

    # For each comic website, download the main url.
    for comic_site in comic_names:
        comic_url = comic_main_urls[comic_site]
        request_object = requests.get(comic_url)
        try:
            request_object.raise_for_status()
            access_site = True
        except Exception as error:
            print('The website for: %s could not be downloaded.' % comic_site)
            print('An error has occurred: %s\n' % error)
            access_site = False
        # If the comic website could be obtained, attempt to download
        # all comics in separate threads by page.
        if access_site:
            print('%s has been retrieved.\nPreparing to download comic images...')
            comic_page_soup = bs4.BeautifulSoup(request_object.text, "html5lib")
            download_threads = []
            # Download procedure for Lunar Baboon
            if comic_site == 'Lunar Baboon':
                # Determine the number of pages to download from
                page_elems = comic_page_soup.select('.paginationPageNumber')
                num_pages = int(page_elems[len(page_elems) - 1].getText())
                current_page = 1
                while current_page < num_pages:
                    thread_object = threading.Thread(target=download_lunar_baboon, args=[comic_page_soup])
                    download_threads.append(thread_object)
                    thread_object.start()
                    print('Preparing to download page %s for: %s...' % (str(current_page), comic_site))
                    current_page += 1
                    # Prepare next url from Previous button
                    comic_url = comic_main_urls[comic_site] + '/comics/?currentPage=' + str(current_page)
                    request_object = requests.get(comic_url)
                    try:
                        request_object.raise_for_status()
                        comic_page_soup = bs4.BeautifulSoup(request_object.text, "html5lib")
                    except Exception as error:
                        print('The web page # %s for: %s could not be downloaded.' % (str(current_page), comic_site))
                        print('An error has occurred: %s\n' % error)
            # Download procedure for Wonderella
            elif comic_site == 'Wonderella':
                last_comic_indicator = (comic_page_soup.select('a[rel="prev"]') == [])
                while not last_comic_indicator:
                    thread_object = threading.Thread(target=download_wonderella, args=[comic_page_soup])
                    download_threads.append(thread_object)
                    thread_object.start()
                    comic_title = comic_page_soup.select('a[title^="Permanent Link"]')[0].getText()
                    print('Preparing to download page %s for: %s...' % (comic_title, comic_url))
                    # Prepare next url from Previous button
                    comic_url = comic_page_soup.select('a[rel="prev"]')[0].get('href')
                    request_object = requests.get(comic_url)
                    try:
                        request_object.raise_for_status()
                        comic_page_soup = bs4.BeautifulSoup(request_object.text, "html5lib")
                    except Exception as error:
                        print('The web page for %s at %s could not be downloaded.' % (comic_title, comic_site))
                        print('An error has occurred: %s\n' % error)
            # Download procedure for Moonbeard
            else:
                last_comic_indicator = (comic_page_soup.select('a.navi-prev') == [])
                while not last_comic_indicator:
                    thread_object = threading.Thread(target=download_moonbeard, args=[comic_page_soup])
                    download_threads.append(thread_object)
                    thread_object.start()
                    comic_title = comic_page_soup.select('#content .post-title a')[0].getText()
                    print('Preparing to download page %s for: %s...' % (comic_title, comic_url))
                    # Prepare next url from Previous button
                    comic_url = comic_page_soup.select('a.navi-prev')[0].get('href')
                    request_object = requests.get(comic_url)
                    try:
                        request_object.raise_for_status()
                        comic_page_soup = bs4.BeautifulSoup(request_object.text, "html5lib")
                    except Exception as error:
                        print('The web page # %s for: %s could not be downloaded.' % (comic_title, comic_site))
                        print('An error has occurred: %s\n' % error)
        else:
            print('Skipping downloading comics for: %s.\n' % comic_site)
            continue


def download_lunar_baboon(soup_object):

    """This function downloads all of the comics from the current page to the Desktop comic folder."""

    # complete determines whether to download all of the comics on the page or only
    # the latest one.
    # Get all of the html elements that contain the comic image links on the page.
    comic_elems = soup_object.select('.journal-entry-navigation-current')
    for elem in comic_elems:
        comic_name = elem.getText() + '.png'
        comic_name_path = os.path.join(folder_names['Lunar Baboon'], comic_name)
        comic_link = comic_main_urls['Lunar Baboon'] + elem.get('href')
        # Obtain the individual page for the comic image. Download the comic
        # image to the comic folder on the Desktop.
        try:
            individual_comic_pg = requests.get(comic_link)
            individual_comic_pg.raise_for_status()
            print('Preparing to download: %s from the url: %s' % (elem.getText(), comic_link))
            individual_comic_soup = bs4.BeautifulSoup(individual_comic_pg.text, "html5lib")
            img_elem = individual_comic_soup.select('img[alt=""]')
            image_link = comic_main_urls['Lunar Baboon'] + img_elem[0].get('src')
            image_object = requests.get(image_link)
            image_object.raise_for_status()
            with open(comic_name_path, 'wb') as image_file:
                for chunk in image_object.iter_content(100000):
                    image_file.write(chunk)
            print('The comic: %s has been downloaded to: %s' % (elem.getText(), comic_name_path))
        except Exception as error:
            print('The comic image: %s located at: %s could not be downloaded.' % (elem.getText(), comic_link))
            print('An error has occurred: %s\n' % error)


def download_wonderella(soup_object):

    """This function downloads the comic from the current page to the Desktop comic folder."""

    # Download the comic image on the webpage.
    # Get all of the html elements that contain the comic image links on the page.
    img_elem = soup_object.select('div #comic img[src]')[0]
    comic_title = soup_object.select('a[title^="Permanent Link"]')[0].getText()
    comic_name_path = os.path.join(folder_names['Wonderella'], comic_title)
    comic_link = img_elem.get('src')
    # Download the comic image to the comic folder on the Desktop.
    try:
        individual_comic_pg = requests.get(comic_link)
        individual_comic_pg.raise_for_status()
        print('Preparing to download: %s from the url: %s' % (comic_title, comic_link))
        with open(comic_name_path, 'wb') as image_file:
            for chunk in individual_comic_pg.iter_content(100000):
                image_file.write(chunk)
        print('The comic: %s has been downloaded to: %s' % (comic_title, comic_name_path))
    except Exception as error:
        print('The comic image: %s located at: %s could not be downloaded.' % (comic_title, comic_link))
        print('An error has occurred: %s\n' % error)


def download_moonbeard(soup_object):

    """This function downloads the comic from the current page to the Desktop comic folder."""

    # Download the comic image on the webpage.
    # Get all of the html elements that contain the comic image links on the page.
    img_elem = soup_object.select('#comic-1 img')[0]
    comic_title = soup_object.select('#content .post-title a')[0].getText()
    comic_name_path = os.path.join(folder_names['Moonbeard'], comic_title)
    comic_link = img_elem.get('src')
    # Download the comic image to the comic folder on the Desktop.
    try:
        individual_comic_pg = requests.get(comic_link)
        individual_comic_pg.raise_for_status()
        print('Preparing to download: %s from the url: %s' % (comic_title, comic_link))
        with open(comic_name_path, 'wb') as image_file:
            for chunk in individual_comic_pg.iter_content(100000):
                image_file.write(chunk)
        print('The comic: %s has been downloaded to: %s' % (comic_title, comic_name_path))
    except Exception as error:
        print('The comic image: %s located at: %s could not be downloaded.' % (comic_title, comic_link))
        print('An error has occurred: %s\n' % error)


if __name__ == "__main__":
    folder_names = create_folders()
    download_all_comics()
