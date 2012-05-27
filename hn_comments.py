from wsgiref.simple_server import make_server
import urllib2
from bs4 import BeautifulSoup
import os
import time

COMMENTS_CACHE = '/home/pktck/hn_comments_cache/'

def getPage(uri):
    if uri == '':
        filename = os.path.join(COMMENTS_CACHE, 'index')
    else:
        filename = os.path.join(COMMENTS_CACHE, uri)

    # the file exists and is less than 15 min. old
    if os.path.exists(filename) and os.path.getmtime(filename) > time.time() - 15 * 60:
        with open(filename) as fd:
            html = fd.read()
    else:
        print 'fetching %s' % uri
        html = urllib2.urlopen('http://news.ycombinator.com/%s' % uri).read()
        with open(filename, 'w') as fd:
            fd.write(html)

    return html



def generateBody():
    #html = urllib2.urlopen('http://news.ycombinator.com/').read()
    html = getPage('') # get the front page
    #html = open('/home/pktck/hn.html').read()
    soup = BeautifulSoup(html)

    subtexts = soup.find_all(attrs={'class':'subtext'})

    for subtext in subtexts:
        links = subtext.find_all('a')

        if len(links) >= 2:
            comment_uri = links[1].get('href')
            comment_html = getPage(comment_uri)
            comment_soup = BeautifulSoup(comment_html[:10000])
            first_comment = comment_soup.find(attrs={'class':'default'})

            if first_comment:
                first_comment.font.attrs['color'] = '#555'
                row = BeautifulSoup('<tr><td colspan=2></td>%s</tr>' % first_comment)
                subtext.parent.insert_after(row)

    body = str(soup)

    return body





def application(environ, start_response):

   # Sorting and stringifying the environment key, value pairs
   #response_body = ['%s: %s' % (key, value)
                    #for key, value in sorted(environ.items())]
   #response_body = '\n'.join(response_body)

   response_body = generateBody()

   status = '200 OK'
   response_headers = [('Content-Type', 'text/html'),
                  ('Content-Length', str(len(response_body)))]
   start_response(status, response_headers)

   return [response_body]

# Instantiate the WSGI server.
# It will receive the request, pass it to the application
# and send the application's response to the client
if __name__ == '__main__':
    httpd = make_server(
       '0.0.0.0', # The host name.
       8051, # A port number where to wait for the request.
       application # Our application object name, in this case a function.
       )

    # Wait for a single request, serve it and quit.
    httpd.handle_request()
