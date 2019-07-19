#! usr/bin/python3

# downloadxkcd.py - Downloads all of the XKCD comics from the internet


import requests, os, sys, bs4


# starting url to check for images
start_url = 'http://xkcd.com'
url = start_url

# store XKCD comics in /home/austin/Desktop/XKCD Comics
xkcd_dir = '/home/austin/Desktop/XKCD Comics'
os.makedirs(xkcd_dir , exist_ok=True)

# for a given url, download the XKCD comic image and update the next
# url to open and retrieve the next comic image. Stop the for loop
# to continue updating the url and downloading comic images when the
# url ends with '#'.
while not url.endswith('#'):
    # Download the current web page given by url
    res = requests.get(url)
    try:
        res.raise_for_status()
        print('%s has successfully been downloaded.' % url)
    except Exception as err:
        print('The web page could not be downloaded: %s' % err)
        sys.exit('Cancelling subsequent downloads. Ending program now.')

    # parse the html portion of the downloaded web page with beautifulsoup
    soup = bs4.BeautifulSoup(res.text, 'html5lib')

    # find the url of the comic image
    comic_elem = soup.select('#comic img')
    if comic_elem == []:
        print('The comic image could not be retrieved at %s.' % url)
    else:
        try:
            comic_url = 'http:' + comic_elem[0].get('src')
            # Download the comic image
            print('Downloading image %s' % (comic_url))
            res = requests.get(comic_url)
            res.raise_for_status()
        except Exception as err:
            # report that the comic could not be downloaded and cancel
            # subsequent downloads as well
            print('The comic image at url: %s could not be downloaded.' % (comic_url))
            sys.exit('Cancelling subsequent downloads. Ending program now.')
        # write the comic image file to the XKCD folder
        with open(os.path.join(xkcd_dir, os.path.basename(comic_url)), 'wb') as image_file:
            for chunk in res.iter_content(100000):
                image_file.write(chunk)

    # Get the previous link url
    prev_url = soup.select('a[rel="prev"]')[0]
    url = start_url + prev_url.get('href')

print('Done.')
print('The XKCD comic images have been downloaded to: ' + xkcd_dir + '.')
