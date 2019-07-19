#! usr/bin/python3

# flickr_img_dl - Downloads images from a flickr search result

# USAGE: python3 flickr_img_dl.py <search term> <# of images>
# Uses the Flickr search function to find the command line
# search term. Downloads the top appearing images from the
# search result a number of times equal to the user input
# term for number of images.


import bs4, os, re, requests, sys


def command_line_args(*cl_args):

    """Checks if the number of command line arguments are
    valid and if each argument makes sense. If so, returns
    the values of the Flickr search term. Otherwise, print
    that the script usage is incorrect.
    """

    # Command line input must have at least two arguments
    if len(cl_args[0]) < 2:
        print('Improper command line arguments. The number of'
              ' arguments cannot be less than 2. Please refer'
              ' to the usage explanation: \n'
              'USAGE: python3 flickr img_dl.py <search term>')
        search_term = input('Enter the search term here: ')

    # Take in the remainder of command line argument as the
    # search term
    else:
        search_term = ' '.join(cl_args[0][1:])

    return search_term


def number_to_dl():

    """Prompt the user to input the number of images to
    download from the top-appearing images of the search
    result. Re-prompt the user until a non-negative integer
    is inputted.
    """

    # Prompt user to input non-negative integer until that
    # is actually the input.
    valid_input = False
    while not valid_input:
        try:
            user_input = int(input('How many images to download from Flickr?\n'))
        except ValueError as err:
            print(err)

        try:
            if user_input > 0:
                valid_input = True
            elif user_input == 0:
                sys.exit('No further action to download zero images.')
            else:
                print('The number of images to download cannot be negative.')
        except ValueError:
            print('The input must be in integer form.')

    return user_input


def search_flickr(term):

    """Use the Flickr search engine to perform a search for
    the user-defined search term. Returns a html copy of the
    search results page to be parsed.
    """

    # Retrieve the html data for the search results page from
    # Flickr website search engine.
    search_address = 'http://flickr.com/search/?text=' + term
    res = requests.get(search_address)

    try:
        res.raise_for_status()
        print('Successfully retrieved data from search results page for %s' % term)
    except Exception as err:
        print('An error has occurred: %s' % err)
        sys.exit('Data from the search results page could not be retrived currently.'
                 '\nExiting now.')

    return res


def image_downloader(html_object, search_word, number_images):

    """Parses through the html data from the search results
    page. Finds the elements for the image files and downloads
    the top-appearing images for the number of times specified
    by the user.
    """

    # Parses through the html data for the search results page.
    # Find elements for the image files and downloads the next
    # top-appearing image for the user-specified amount.
    bs4_object = bs4.BeautifulSoup(html_object.text, "lxml")
    link_elem = bs4_object.select('.photo-list-photo-view')

    # Search the element containing the image file link for the url
    url_regex = re.compile(r'((//c1.staticflickr.com/).+(\.jpg))')

    # Check to see how many images to download based on the
    # number of search results
    if len(link_elem) < number_images:
        print('There are only %s search results for: %s.' % (len(link_elem), search_word))
        number_images = len(link_elem)
        print('Preparing to download the top % s images' % number_images)
    else:
        print('Preparing to download the top %s images' % number_images)

    # Create a directory in Desktop to store the downloaded
    # images.
    dir_name = os.path.join((os.getenv('HOME') + '/Desktop'), 'Search_Result_Images')
    os.makedirs(dir_name, exist_ok=True)

    # Search for the image url from the html data
    for image_index in range(number_images):
        image_link = url_regex.search(str(link_elem[image_index])).group()
        image_url = 'http:' + image_link
        image_file = requests.get(image_url)
        print('Downloading the image file at %s...' % image_url)

        try:
            # Search for the image file name from the image file html
            image_file.raise_for_status()
            file_name_regex = re.compile(r'(/(\d+)_(\w+)(\.jpg))')
            file_name = file_name_regex.search(image_link).group()

            # Write the image data to the folder: Search_Result_Images
            image_file_path = dir_name + file_name
            print('Downloading image file to: ' + image_file_path + '\n')
            with open(image_file_path, 'wb') as handler:
                for chunk in image_file.iter_content(100000):
                    handler.write(chunk)

        except Exception as err:
            print('An error has occurred: %s' % err)
            print('The image at: ' + image_url + ' could not be downloaded.')
            print('Moving on to the next image...\n')

    print('Finished downloading.')
    sys.exit('Image files written to: %s' % dir_name)


# Determine search keyword from command line arguments
search_keyword = command_line_args(sys.argv)

# Prompt user for how many files to download
files_to_download = number_to_dl()

# Returns a soup object that contains the html for the Flickr
# search results for the search keyword
flickr_search_obj = search_flickr(search_keyword)

# Attempts to download the specified number of images from
# the search results page into a folder called: 'Search_Result_Images.'
image_downloader(flickr_search_obj, search_keyword, files_to_download)