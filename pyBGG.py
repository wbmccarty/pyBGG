'''
BGG.py

Modules for using the BoardGameGeek.com web site.

To Do:
test
- Cache collection data.
- Implement getWishlistByUserId to return a collection of items (within a channel, within an rss):

  <item>
   <title>
    Item For Sale: Liberty Roads
   </title>
   <description>
    &lt;p&gt;by &lt;a  href='http://boardgamegeek.com/user/jjdenver'&gt;jjdenver&lt;/a&gt;&lt;/p&gt;
	
		&lt;a  href="http://boardgamegeek.com/geekstore.php3?action=viewitem&amp;itemid=522244"   &gt;$42.00&lt;/a&gt;
			for Board Game:
			&lt;a  href="http://boardgamegeek.com/boardgame/39188/liberty-roads"   &gt;Liberty Roads&lt;/a&gt;&lt;br&gt;
			Condition: Like New&lt;br&gt;
			Location: United States
   </description>
   <link>
    http://boardgamegeek.com/geekstore.php3?action=viewitem&amp;itemid=522244
   </link>
   <guid>
    http://boardgamegeek.com/geekstore.php3?action=viewitem&amp;itemid=522244
   </guid>
   <pubDate>
    Sun, 29 Sep 2013 03:09:27 +0000
   </pubDate>
   <dc:creator>
    jjdenver
   </dc:creator>
  </item>

    <item>
   <title>
    Item For Sale: The Supreme Commander
   </title>
   <description>
    &lt;p&gt;by &lt;a  href='http://boardgamegeek.com/user/cdatkins'&gt;cdatkins&lt;/a&gt;&lt;/p&gt;
	
		&lt;a  href="http://boardgamegeek.com/geekstore.php3?action=viewitem&amp;itemid=522177"   &gt;$35.00&lt;/a&gt;
			for Board Game:
			&lt;a  href="http://boardgamegeek.com/boardgame/39066/the-supreme-commander"   &gt;The Supreme Commander&lt;/a&gt;&lt;br&gt;
			Condition: New&lt;br&gt;
			Location: United States
   </description>
   <link>
    http://boardgamegeek.com/geekstore.php3?action=viewitem&amp;itemid=522177
   </link>
   <guid>
    http://boardgamegeek.com/geekstore.php3?action=viewitem&amp;itemid=522177
   </guid>
   <pubDate>
    Sat, 28 Sep 2013 20:55:02 +0000
   </pubDate>
   <dc:creator>
    cdatkins
   </dc:creator>
  </item>
 
- Use hash.update()
- Get BGG marketplace items for specified game:
  http://www.boardgamegeek.com/xmlapi/boardgame/111&marketplace=1
- Get eBay auctions for wishlist of logged-in user:
  http://www.boardgamegeek.com/geekbay/browse?filterwanttobuy=1&sort=endtime
- Parse wishlistcomment
- Support JSON or CSV dump of results
- Load and save history file of seen marketplace offers and eBay auctions--by
  date so that
  restart and recovery are possible.
- Capture history of all sales offers and auctions, in order to be able to
  refine purchase offers: date, place (BGG/eBay), offer/auction id, BGG Id,
  seller, price, description/condition.
- Search history.  
- Create proper docstrings.
- Add and extract versions information:
  http://www.boardgamegeek.com/xmlapi/boardgame/701&versions=1
- Ibid. videos=1, comments=1, ratingcomments=1
- See http://boardgamegeek.com/guild/1229
- N.B.: Unless accessed via collection and then game ID, game record is NOT complete. 

'''

'''
Search by name: http://www.boardgamegeek.com/xmlapi2/search?query=house

Parameter	 Description 
query=SEARCH_QUERY	 Returns all types of Items that match SEARCH_QUERY. Spaces in the SEARCH_QUERY are replaced by a +
type=TYPE	 Return all items that match SEARCH_QUERY of type TYPE. TYPE might be rpgitem, videogame, boardgame, or boardgameexpansion. You can return multiple types by listing them separated by commas, e.g. type=TYPE1,TYPE2,TYPE3
exact=1	 Limit results to items that match the SEARCH_QUERY exactly
'''


'''
Collection XMLAPI
Base URI: /xmlapi2/collection?parameters

Parameter	 Description
username=NAME	 Name of the user to request the collection for.
version=1	 Returns version info for each item in your collection.
subtype=TYPE	 Specifies which collection you want to retrieve. TYPE may be boardgame, boardgameexpansion, rpgitem, videogame; the default is boardgame
excludesubtype=TYPE	 Specifies which subtype you want to exclude from the results.
id=NNN	 Filter collection to specifically listed item(s). NNN may be a comma-delimited list of item ids.
brief=1	 Returns more abbreviated results.
stats=1	 Returns expanded rating/ranking info for the collection.
own=[0,1]	 Filter for owned games. Set to 0 to exclude these items so marked. Set to 1 for returning owned games and 0 for non-owned games.
rated=[0,1]	 Filter for whether an item has been rated. Set to 0 to exclude these items so marked. Set to 1 to include only these items so marked.
played=[0,1]	 Filter for whether an item has been played. Set to 0 to exclude these items so marked. Set to 1 to include only these items so marked.
comment=[0,1]	 Filter for items that have been commented. Set to 0 to exclude these items so marked. Set to 1 to include only these items so marked.
trade=[0,1]	 Filter for items marked for trade. Set to 0 to exclude these items so marked. Set to 1 to include only these items so marked.
want=[0,1]	 Filter for items wanted in trade. Set to 0 to exclude these items so marked. Set to 1 to include only these items so marked.
wishlist=[0,1]	 Filter for items on the wishlist. Set to 0 to exclude these items so marked. Set to 1 to include only these items so marked.
wishlistpriority=[1-5]	 Filter for wishlist priority. Returns only items of the specified priority.
wanttoplay=[0,1]	 Filter for items marked as wanting to play. Set to 0 to exclude these items so marked. Set to 1 to include only these items so marked.
wanttobuy=[0,1]	 Filter for ownership flag. Set to 0 to exclude these items so marked. Set to 1 to include only these items so marked.
prevowned=[0,1]	 Filter for games marked previously owned. Set to 0 to exclude these items so marked. Set to 1 to include only these items so marked.
hasparts=[0,1]	 Filter on whether there is a comment in the Has Parts field of the item. Set to 0 to exclude these items so marked. Set to 1 to include only these items so marked.
wantparts=[0,1]	 Filter on whether there is a comment in the Wants Parts field of the item. Set to 0 to exclude these items so marked. Set to 1 to include only these items so marked.
minrating=[1-10]	 Filter on minimum personal rating assigned for that item in the collection.
maxrating=[1-10]	 Filter on maximum personal rating assigned for that item in the collection.
minbggrating=[1-10]	 Filter on minimum BGG rating for that item in the collection.
maxbggrating=[1-10]	 Filter on maximum BGG rating for that item in the collection.
minplays=NNN	 Filter by minimum number of recorded plays.
maxplays=NNN	 Filter by maximum number of recorded plays.
showprivate=1	 Filter to show private collection info. Only works when viewing your own collection and you are logged in.
collid=NNN	 Restrict the collection results to the single specified collection id. Collid is returned in the results of normal queries as well.
modifiedsince=YY-MM-DD	 Restricts the collection results to only those whose status (own, want, fortrade, etc.) has changed or been added since the date specified (does not return results for deletions). Time may be added as well: modifiedsince=YY-MM-DD%20HH:MM:SS
'''

'''
Note: Additional elements and attributes (e.g., wishlishcomment) are available
to a logged-in user.

Known additional elements and attributes:

acquiredfrom
acquisitiondate
comment
currvalue
cv_currency
numplays
originalname
pp_currency
pricepaid
privatecomment
privateinfo
quantity
rating
wishlistcomment
'''

from bs4 import BeautifulSoup
from bs4 import element
import ConfigParser
import lxml.html
import requests
import sys
import traceback
import urllib

def httpGet(url, session = None):
    if session == None:
        return urllib.urlopen(url).read()
    else:
        return session.get(url).text.encode('UTF-8')

def login(loginurl = None, username = None, password = None, configfile = None):
    config = None
    if loginurl == None or username == None or password == None:
        if configfile == None:
            configfile = '../../Gaming/BGG Scripts/bgg_config.ini'
        config = ConfigParser.ConfigParser()
        config.read(configfile)
    if loginurl == None:
        loginurl = config.get('Login', 'LoginURL')
    if username == None:
        username = config.get('Login', 'UserID')
    if password == None:
        password = config.get('Login', 'Password')
    payload = { u'username':username, u'password':password }
##    print >>sys.stderr, 'loginurl:', loginurl
##    print >>sys.stderr, 'payload:', payload
    session = requests.Session()
    r = session.post(loginurl, data=payload)
##    print >>sys.stderr, 'status_code:', r.status_code
##    print >>sys.stderr, r.headers
##    text = r.text.encode('UTF-8') 
##    print >>sys.stderr, BeautifulSoup(httpSessionGet('http://www.boardgamegeek.com/geekbay/browse?filterwanttobuy=1&sort=endtime'), 'xml').prettify()
    return session
        
def parseGameObject(soup):
    '''
    Parse a BeautifulSoup object containing the BGG representation of a game. Return a hash of the fields.
    '''
##    print >>sys.stderr, 'Parse target:', soup.prettify()
    TYPEFLOAT = 0
    TYPEINT = 1
    TYPESTRING = 2
    TYPELIST = 3
    TEXTFIELDS = {
        'age':TYPEINT,
        'average':TYPEFLOAT,
        'averageweight':TYPEFLOAT,
        'bayesaverage':TYPEFLOAT,
        'boardgameartist':TYPELIST,
        'boardgamecategory':TYPELIST,
        'boardgamedesigner':TYPELIST,
        'boardgamefamily':TYPELIST,
        'boardgamehonor':TYPELIST,
        'boardgamemechanic':TYPELIST,
        'boardgamepodcastepisode':TYPELIST,
        'boardgamepublisher':TYPELIST,
        'boardgamesubdomain':TYPELIST,
        'boardgameversion':TYPELIST,
        'comment':TYPESTRING,
        'description':TYPESTRING,
        'image':TYPESTRING,
        'maxplayers':TYPEINT,
        'median':TYPEFLOAT,
        'minplayers':TYPEINT,
        'name':TYPELIST,
        'numcomments':TYPEINT,
        'numweights':TYPEINT,
        'owned':TYPEINT,
        'playingtime':TYPEINT,
        'stddev':TYPEFLOAT,
        'thumbnail':TYPESTRING,
        'trading':TYPEINT,
        'usersrated':TYPEINT,
        'videogamebg':TYPELIST,
        'wanting':TYPEINT,
        'wishing':TYPEINT,
        'wishlistcomment':TYPESTRING,
        'yearpublished':TYPEINT,
    }
    STATUSFIELDS = [
        'fortrade',
        'lastmodified',
        'own',
        'preordered',
        'prevowned',
        'want',
        'wanttobuy',
        'wanttoplay',
        'wishlist',
        'wishlistpriority',
    ]
    STATSFIELDS = [
        'maxplayers',
        'minplayers',
        'numowned',
        'playingtime',
    ]

    PRIVATEINFO = [
        ('acquiredfrom', TYPESTRING),
        ('acquisitiondate', TYPESTRING),
        ('comment', TYPESTRING),
        ('currvalue', TYPEFLOAT),
        ('cv_currency', TYPESTRING),
        ('numplays', TYPEINT),
        ('originalname', TYPESTRING),
        ('pp_currency', TYPESTRING),
        ('pricepaid', TYPEFLOAT),
        ('privatecomment', TYPESTRING),
        ('privateinfo', TYPESTRING),
        ('quantity', TYPEINT),
        ('rating', TYPEFLOAT),
        ('wishlistcomment', TYPESTRING),
    ]

    # Handled ad hoc, because a mixture of attribute and text values:
    MARKETPLACE = [
        ('listdate', TYPESTRING),
        ('price', TYPEFLOAT), # has attribute currency
        ('condition', TYPESTRING),
        ('notes', TYPESTRING),
    ]

    try:
        game = { }
        for rank in soup.find_all('rank'):
            try:
                game[rank.get('friendlyname').encode('ascii', 'ignore').upper().replace(' ', '')] = int(rank.get('value'))
            except:
                pass
        marketplace = soup.find('marketplacelistings')
        if marketplace:
            n = 0
            for listing in marketplace.find_all('listing'):
                n += 1
                for mlname, mltype in MARKETPLACE:
                    ml = listing.find(mlname)
                    if mltype == TYPEFLOAT:
                        try:
                            game['LISTING%03d_' % n + mlname.upper()] = \
                                float(ml.get_text('', strip=True))
                        except:
                            pass
                    elif mltype == TYPEINT:
                        try:
                            game['LISTING%03d_' % n + mlname.upper()] = \
                                int(ml.get_text('', strip=True))
                        except:
                            pass
                    elif mltype == TYPESTRING:
                        try:
                            game['LISTING%03d_' % n + mlname.upper()] = \
                                ml.get_text('', strip=True)
                        except:
                            pass
                    else: #TYPELIST
                        try:
                            game['LISTING%03d_' % n + mlname.upper()] = \
                                [x.get_text() for x in listing.find_all(mlname)]
                        except:
                            pass
                    # ad hoc
                    try:
                        game['LISTING%03d_' % n + 'PRICECURRENCY'] = \
                            listing.find('price').get('currency')
                    except:
                        pass
                    try:
                        game['LISTING%03d_' % n + 'LINKHREF'] = \
                            listing.find('link').get('href')
                    except:
                        pass
                    try:
                        game['LISTING%03d_' % n + 'LINKTITLE'] = \
                            listing.find('link').get('title')
                    except:
                        pass
        status = soup.find('status')
        if status:
            for sf in STATUSFIELDS:
                if status.get(sf):
                    game['STATUS_' + sf.upper()] = status.get(sf)
        stats = soup.find('stats')
        if stats:
            for sf in STATSFIELDS:
                if stats.get(sf):
                    game['STATS_' + sf.upper()] = stats.get(sf)
        for tf in TEXTFIELDS.keys():
            tftype = TEXTFIELDS[tf]
            if tftype == TYPEFLOAT:
                try:
                    game[tf.lower()] = \
                        float(soup.find(tf).get_text('', strip=True))
                except:
                    pass
            elif tftype == TYPEINT:
                try:
                    game[tf.lower()] = \
                        int(soup.find(tf).get_text('', strip=True))
                except:
                    pass
            elif tftype == TYPESTRING:
                try:
                    game[tf.lower()] = \
                        soup.find(tf).get_text('', strip=True)
                except:
                    pass
            else: #TYPELIST
                try:
                    game[tf.lower()] = [x.get_text() for x in soup.find_all(tf)]
                except:
                    pass
        privateinfo = soup.find('privateinfo')
        if privateinfo:
##            print >>sys.stderr, 'Found privateinfo'
            for pvname, pvtype in PRIVATEINFO:
##                print >>sys.stderr, pvname, pvtype
                pv = privateinfo.find(pvname)
                if not pv:
##                    print >>sys.stderr, 'Failed to find pv', pvname, pvtype
                    continue
##                print >>sys.stderr, 'Found pv', pvname, pvtype, pv.get_text('', strip=True)
                if pvtype == TYPEFLOAT:
                    try:
                        game['PRIVATEINFO_' + pvname.upper()] = \
                            float(pv.get_text('', strip=True))
                    except:
                        pass
                elif pvtype == TYPEINT:
                    try:
                        game['PRIVATEINFO_' + pvname.upper()] = \
                            int(pv.get_text('', strip=True))
                    except:
                        pass
                elif pvtype == TYPESTRING:
                    try:
                        game['PRIVATEINFO_' + pvname.upper()] = \
                            pv.get_text('', strip=True)
                    except:
                        pass
                else: #TYPELIST
                    try:
                        game['PRIVATEINFO_' + pvname.upper()] = [x.get_text() for x in privateinfo.find_all(pvname)]
                    except:
                        pass
    except Exception as e:
        print >>sys.stderr, e
        traceback.print_exc()
        try:
            print >>sys.stderr, soup.prettify()
        except:
            pass
    return game

def getElementsAndAttributes(session = None):
    structure = { }
    URL = 'http://www.boardgamegeek.com/xmlapi/collection/wbmccarty'
    soup = BeautifulSoup(httpGet(URL, session = session), 'xml')
##    print soup.prettify()
    # root element: items
    e = soup.find('items')
    while e:
        if type(e) == element.Tag and e.name != 'items' and e.name != 'item':
##            print >>sys.stderr, 'e tag:', 'name=', e.name, 'attrs=', e.attrs
            if e.name not in structure:
                structure[e.name] = True
                print >>sys.stderr, e.name, e.get_text()
            for attr in e.attrs.keys():
                if e.name + '.' + attr not in structure:
                    structure[e.name + '.' + attr] = True
                    print >>sys.stderr, e.name + '.' + attr, e.get(attr)
        e = e.next_element
    print >>sys.stderr, 'structure after collection:', structure
    URL = 'http://www.boardgamegeek.com/xmlapi/boardgame/12333?stats=1'
    soup = BeautifulSoup(httpGet(URL, session))
    # root element: boardgames
    e = soup.find('boardgames')
    while e:
        if type(e) == element.Tag and e.name != 'boardgames' and e.name != 'boardgame':
##            print >>sys.stderr, 'e tag:', 'name=', e.name, 'attrs=', e.attrs
            if e.name not in structure:
                structure[e.name] = True
                print >>sys.stderr, e.name, e.get_text()
            for attr in e.attrs.keys():
                if e.name + '.' + attr not in structure:
                    structure[e.name + '.' + attr] = True
                    print >>sys.stderr, e.name + '.' + attr, e.get(attr)
        e = e.next_element
    print >>sys.stderr, 'structure after stats:', structure
    return structure
    
def prettyPrintCollectionByUserAndId(user, id, session = None):
    '''
    Pretty print from the specified user's collection all game records
    specified by the given BGG ID.
    '''
    URL = 'http://www.boardgamegeek.com/xmlapi/collection/%s'
    url = URL % user
    soup = BeautifulSoup(httpGet(url, session = session), 'xml')
    collection = [ ]
    for item in soup.find_all('item', objectid=str(id)):
        print item.prettify()
        print

def prettyPrintGameById(id, session = None):
    '''
    Pretty print the game record specified by the given BGG ID.
    '''
    URL = 'http://www.boardgamegeek.com/xmlapi/boardgame/%d?stats=1'
    url = URL % int(id)
    soup = BeautifulSoup(httpGet(url, session = session), 'xml')
    print soup.prettify()
    print

def getCollectionByUserAndId(user, id=0, session = None):
    URL = 'http://www.boardgamegeek.com/xmlapi/collection/%s'
    url = URL % user
    soup = BeautifulSoup(httpGet(url, session = session), 'xml')
    collection = [ ]
    if id == 0:
        items = soup.find_all('item')
    else:
        items = soup.find_all('item', objectid=str(id))
    for item in items:
##        print >>sys.stderr, 'item:', item.prettify()
        game = parseGameObject(item)
        game['TITLE'] = item.find('name').get_text('', strip=True)
        game['BGGID'] = int(item.get('objectid'))
        game2 = getGameById(game['BGGID'],session = session)
        for key in game.keys():
            game2[key] = game[key]
        collection.append(game2)
    return collection

def prettyPrintWishlistByUserId(userid, session = None):
    '''
    Pretty print the game record specified by the given BGG ID.
    '''
    URL = 'http://www.boardgamegeek.com/recentadditions/rss?subdomain=&colfilters%%5B0%%5D=wishlist&infilters%%5B0%%5D=storeitem&domain=boardgame&userid=%d'
    url = URL % int(userid)
    soup = BeautifulSoup(httpGet(url, session = session), 'xml')
    print soup.prettify()
    print

##def getWishlistByUserId(userid, session = None):
##    '''
##    Return a hash containing the fields of the specified BGG game record.
##    '''
##    URL = 'http://www.boardgamegeek.com/xmlapi/boardgame/%d&marketplace=1'
##    url = URL % int(id)
##    soup = BeautifulSoup(httpGet(url, session = session), 'xml')
##    game = parseGameObject(soup)
##    game['TITLE'] = soup.find('name', primary='true').get_text('', strip=True)
##    game['BGGID'] = int(soup.find('boardgame').get('objectid'))
##    if 'description' in game:
####        print >>sys.stderr, 'found description'
##        game['DESCRIPTION'] = unicode(lxml.html.fromstring(game['description']).text_content())
####        print >>sys.stderr, game['description']
####        print >>sys.stderr, game['DESCRIPTION']
##    return game


def prettyPrintMarketplaceById(id, session = None):
    '''
    Pretty print the game record specified by the given BGG ID.
    '''
    URL = 'http://www.boardgamegeek.com/xmlapi/boardgame/%d&marketplace=1'
    url = URL % int(id)
    soup = BeautifulSoup(httpGet(url, session = session), 'xml')
    print soup.prettify()
    print


def getMarketplaceById(id, session = None):
    '''
    Return a hash containing the fields of the specified BGG game record.
    '''
    URL = 'http://www.boardgamegeek.com/xmlapi/boardgame/%d&marketplace=1'
    url = URL % int(id)
    soup = BeautifulSoup(httpGet(url, session = session), 'xml')
    game = parseGameObject(soup)
    game['TITLE'] = soup.find('name', primary='true').get_text('', strip=True)
    game['BGGID'] = int(soup.find('boardgame').get('objectid'))
    if 'description' in game:
##        print >>sys.stderr, 'found description'
        game['DESCRIPTION'] = unicode(lxml.html.fromstring(game['description']).text_content())
##        print >>sys.stderr, game['description']
##        print >>sys.stderr, game['DESCRIPTION']
    return game



def getGameById(id, session = None):
    '''
    Return a hash containing the fields of the specified BGG game record.
    '''
    URL = 'http://www.boardgamegeek.com/xmlapi/boardgame/%d?stats=1'
    url = URL % int(id)
    soup = BeautifulSoup(httpGet(url, session = session), 'xml')
    game = parseGameObject(soup)
    game['TITLE'] = soup.find('name', primary='true').get_text('', strip=True)
    game['BGGID'] = int(soup.find('boardgame').get('objectid'))
    if 'description' in game:
##        print >>sys.stderr, 'found description'
        game['DESCRIPTION'] = unicode(lxml.html.fromstring(game['description']).text_content())
##        print >>sys.stderr, game['description']
##        print >>sys.stderr, game['DESCRIPTION']
    return game



if __name__ == '__main__':

    session = login()

    userid = 696454
    prettyPrintWishlistByUserId(userid, session = session)
    sys.exit(0)

    id = 111
    prettyPrintMarketplaceById(id, session = session)
    try:
        game = getMarketplaceById(id, session = session)
        print 
        for key in sorted(game.keys(), key=str.lower):
            if type(game[key]) is list:
                for v in game[key]:
                    print '%s: %s' % (key, v)
            else:    
                print '%s: %s' % (key, game[key])
    except Exception as e:
        print e
    sys.exit(0)
    
    for user in ['wbmccarty']:
        for id in [0]:
            for game in getCollectionByUserAndId(user, id, session = session):
                print 
                for key in sorted(game.keys(), key=str.lower):
                    if type(game[key]) is list:
                        for v in game[key]:
                            print '%s: %s' % (key, v)
                    else:    
                        print '%s: %s' % (key, game[key])
        sys.exit(0)
    
    prettyPrintCollectionByUserAndId('wbmccarty', 54457, session = session)
    sys.exit(0)
    
    prettyPrintCollectionByUserAndId('wbmccarty', 3312, session = session)
    sys.exit(0)
    
    prettyPrintGameById(12333, session = session)
    sys.exit(0)
    
    s = getElementsAndAttributes(session = session)
    for key in sorted(s.keys(), key=str.lower):
        print key
    sys.exit(0)
  
    for id in [5, 701]:
        try:
            game = getGameById(id, session = session)
            print 
            for key in sorted(game.keys(), key=str.lower):
                if type(game[key]) is list:
                    for v in game[key]:
                        print '%s: %s' % (key, v)
                else:    
                    print '%s: %s' % (key, game[key])
        except Exception as e:
            print e
    sys.exit(0)

    for user in ['wbmccarty']:
        for id in [3312]:
            for game in getCollectionByUserAndId(user, id, session = session):
                print 
                for key in sorted(game.keys(), key=str.lower):
                    if type(game[key]) is list:
                        for v in game[key]:
                            print '%s: %s' % (key, v)
                    else:    
                        print '%s: %s' % (key, game[key])
        for id in [0]:
            for game in getCollectionByUserAndId(user, id, session = session):
                print 
                for key in sorted(game.keys(), key=str.lower):
                    if type(game[key]) is list:
                        for v in game[key]:
                            print '%s: %s' % (key, v)
                    else:    
                        print '%s: %s' % (key, game[key])
        sys.exit(0)
    
    id = 3312
    try:
        game = getGameById(id, session = session)
        print 
        for key in sorted(game.keys(), key=str.lower):
            if type(game[key]) is list:
                for v in game[key]:
                    print '%s: %s' % (key, v)
            else:    
                print '%s: %s' % (key, game[key])
    except Exception as e:
        print e
    sys.exit(0)

   



    






from bs4 import BeautifulSoup

import datetime
import json
import re
import urllib
import urllib2
import ConfigParser
import requests
import sys
import webbrowser

ITEMS_URL = 'http://www.boardgamegeek.com/geekbay/browse?filterwanttobuy=1&sort=endtime'
COLLECTION_URL = 'http://www.boardgamegeek.com/xmlapi/collection/wbmccarty'
GAME_URL = 'http://www.boardgamegeek.com/boardgame/%d/'
##GAMEXMLAPI_URL = 'http://www.boardgamegeek.com/xmlapi/boardgame/%d?wishlist=1'
AUCTION_FILE = 'ScanEbay.dat'
HTML_FILE = 'ScanEBay.html'
DONTWANT = '0'
DONTBUY = '5'
MAX_PRICE = 10000.0
# Skip action for old news
SKIP_OFF = 0
SKIP_WARN = 1
SKIP_NOWARN = 2

SKIP_STATUS = SKIP_OFF
SKIP_STATUS = SKIP_WARN

def getWTBGame(bggid_text, collection):
    '''
    Find all instances in the specified collection element of games,
    represented as item elements, having the specified BGG ID. Return
    the item element corresponding to the first such game that's WTB, if
    any. This function is necessary because a single title may be both
    owned and WTB, especially if the owned version differs from the
    WTB version.
    '''
    for item in collection.find_all(objectid=bggid_text):
        status = item.find('status')
        wishlist = status.get('wishlist')
        if wishlist != DONTWANT:
            return item
    return None

def parseComment(s):
    '''
    Parse the wishlist comment, returning a hash of name-value pairs.
    '''
##    print >>sys.stderr, 'Parsing wishlist comment:', s
    parsedComment = { }
    save_s = s
    s = s.strip()
    try:
        while True:
            m = config_item_re.match(s)
            if not m:
##                print >>sys.stderr, 'Parse complete.'
                break
##            print >>sys.stderr, 'Match Object:', m.group(), m.start(), m.end()
            item = m.group(0).strip().lower()
##            print >>sys.stderr, 'Found item:', item
            s = s[m.end():]
            m = config_assign_re.match(s)
            if not m: raise Exception('Bad comment syntax: Expected assignment character.')
##            print >>sys.stderr, 'Match Object:', m.group(), m.start(), m.end()
            s = s[m.end():]
            m = config_value_re.match(s)
            if not m: raise Exception('Bad comment syntax: Expected value.')
##            print >>sys.stderr, 'Match Object:', m.group(), m.start(), m.end()
            if m.group(0).startswith('"'):
                value = m.group(0)[1:-1]
            else:
                value = m.group(0).strip()
            parsedComment[item] = value
            s = s[m.end():]
##            print >>sys.stderr, 'len:', len(s)
            m = config_separator_re.match(s)
##            print >>sys.stderr, 'Match Object:', m.group(), m.start(), m.end()
            s = s[m.end():]
    except Exception as e:
        print >>sys.stderr, e
        print >>sys.stderr, 'Syntax error in wishlist comment:'
        print >>sys.stderr, save_s
        keys = parsedComment.keys()
        keys.sort()
        print >>sys.stderr, 'Parsed wishlist comment:'
        for key in keys:
            print >>sys.stderr, key, '=', parsedComment[key]
    return parsedComment        

##hash = parseComment('WTB=30')
##keys = hash.keys()
##keys.sort()
##print >>sys.stderr, 'Parsed wishlist comment:'
##for key in keys:
##    print >>sys.stderr, key, '=', hash[key]
##sys.exit(0)


def loadSeenFile():
    try:
        seen_file = open(AUCTION_FILE, 'r')
    except IOError:
        seen_file = open(AUCTION_FILE, 'w+')
    auctions_seen = { }
    for line in seen_file.xreadlines():
        auctionid = line.strip()
        auctions_seen[auctionid] = True
    seen_file.close()
    return auctions_seen

def saveSeenFile(auctions_seen):
    seen_file = open(AUCTION_FILE, 'w')
    auctionids = auctions_seen.keys()
    auctionids.sort()
    for auctionid in auctionids:
        print >>seen_file, auctionid
    seen_file.close()

game_re = re.compile(r'http://boardgamegeek.com/boardgame/(\d+)/')
wtb_re  = re.compile(r'WTB[=:](\d+)')
config_item_re = re.compile(r'\w+\s*')
config_assign_re = re.compile(r'(=\s*)|(:\s*)')
config_value_re = re.compile(r'("[^"]*"\s*)|(\w+\s*)')
config_separator_re = re.compile(r'$|,\s*|;\s*')
auction_re = re.compile(r'http://boardgamegeek.com/geekstore.php3\?action=viewitem&itemid=(\d*)')

config = ConfigParser.ConfigParser()
config.read('bgg_config.ini')
loginurl = config.get('Login', 'LoginURL')
bgg_username_name  = u'username'
bgg_username_value = config.get('Login', 'UserID')
bgg_password_name  = u'password'
bgg_password_value = config.get('Login', 'Password')

auctions = { }
auctions_seen = loadSeenFile()

html = open(HTML_FILE, 'w')
print >>html, '<HTML>'
print >>html, '<BODY>'
print >>html, '<head>'
print >>html, '<style>'
print >>html, 'table th, td'
print >>html, '{'
print >>html, 'border:1px solid black;'
print >>html, '}'
print >>html, 'table'
print >>html, '{'
print >>html, 'border-collapse:collapse;'
print >>html, 'width:800px;'
print >>html, '}'
print >>html, '</style>'
print >>html, '</head>'

collection = BeautifulSoup(urllib2.urlopen(COLLECTION_URL))

config = ConfigParser.ConfigParser()
config.read('bgg_config.ini')
loginurl = config.get('Login', 'LoginURL')
bgg_username_name  = u'username'
bgg_username_value = config.get('Login', 'UserID')
bgg_password_name  = u'password'
bgg_password_value = config.get('Login', 'Password')

payload = { bgg_username_name:bgg_username_value,
    bgg_password_name:bgg_password_value }
s = requests.Session()
r = s.post(loginurl, data=payload)
##print >>sys.stderr, 'status_code:', r.status_code
##print >>sys.stderr, r.headers
##text = r.text.encode('UTF-8') 
##with open('results1.html', 'w') as f:
##    f.write(text)
##webbrowser.open('results1.html')    
r = s.get(ITEMS_URL)
##print >>sys.stderr, 'status_code:', r.status_code
##print >>sys.stderr, r.headers
##text = r.text.encode('UTF-8') 
##with open('results2.html', 'w') as f:
##    f.write(text)
##webbrowser.open('results2.html')    

soup = BeautifulSoup(r.text.encode('UTF-8'))
##print >>sys.stderr, soup.prettify()
table = soup.find('table', class_='forum_table sf')
##print >>sys.stderr, table.prettify()
for tr in table.find_all('tr')[1:]:
##    print >>sys.stderr, tr.prettify()
    gamelink = tr.find('a')
    gameurl = gamelink.get('href')
    gameurl_re = re.compile(r'/\w+/(\d+)')
    m = gameurl_re.match(gameurl)
    if not m:
        print >>sys.stderr, 'no match for url:', gameurl
    else:
        bggid = int(m.group(1))
    title = gamelink.get_text().strip()
    script = tr.find('script').get_text().strip()
    script_re = re.compile(r'''document.writeln\("<a rel=\'[^']*\' href=\\"([^"]*)">([^<]*)</a>"\);''')
    script_re = re.compile(r'''document.writeln\("<a rel=\'[^']*\' href=\\"([^\\]*)\\">([^<]*)</a>"\);''')
    m = script_re.match(script)
    if not m:
        print >>sys.stderr, 'no match for script'
    else:
        auctionurl = 'http://www.boardgamegeek.com' + m.group(1)
        auctiontitle = m.group(2)
    td = tr.find_all('td')
    timeleft = td[2].get_text().strip()
    price = tr.find('span', class_='price').get_text().strip()
##    print >>sys.stderr, 'price:', price
    ndx = price.rfind(' ')
    currency = price[:ndx]
    price = float(price[ndx + 1:])

##    print >>sys.stderr, 'gameurl:', gameurl
##    print >>sys.stderr, 'title:', title
##    print >>sys.stderr, 'auctionurl:', auctionurl
##    print >>sys.stderr, 'auctiontitle:', auctiontitle
##    print >>sys.stderr, 'timeleft:', timeleft
##    print >>sys.stderr, 'currency:', currency
##    print >>sys.stderr, 'price:', price
##    print >>sys.stderr

    if bggid in auctions:
        auctions[bggid].append( (title, auctionurl, auctiontitle, timeleft, currency, price) )
    else:
        auctions[bggid] = [ (title, auctionurl, auctiontitle, timeleft, currency, price) ]

keys = auctions.keys()
keys.sort()
for bggid in keys:
    bggid_text = '%d' % bggid
    item = getWTBGame(bggid_text, collection)
    if not item:
        print >>sys.stderr, 'ERROR: Unable to find WTB game record for BGG ID', bggid_text
        continue
##    print >>sys.stderr, item.prettify()
##    sys.exit(0)
    try:
        year = '(%d)' % int(item.find('yearpublished').get_text().strip())
    except:
        year = ''
    try:
        average = '%.4f' % float(item.find('average').get('value').strip())
    except:
        average = 'N/A'
    try:
        usersrated =  '%d' % int(item.find('usersrated').get('value').strip())
    except:
        usersrated = 'N/A'
    try:
        bayes = '%.4f' % float(item.find('bayesaverage').get('value').strip())
    except:
        bayes = 'N/A'
    try:
        numowned = int(item.find('stats').get('numowned').strip())
    except:
        numowned = 0
    status = item.find('status')
    priority = status.get('wishlistpriority')
    if priority == DONTBUY: continue
    for title, auctionurl, auctiontitle, timeleft, currency, price in auctions[bggid]:
        
##        print >>sys.stderr, 'title:', title
##        print >>sys.stderr, 'bggid:', bggid

        if priority == DONTBUY:
            print 'Skipping id=%d title "%s", due to DON\'T BUY' \
                  % (bggid, title, currency)
            print
            continue
        try:
            wishlist = item.find('wishlistcomment').get_text()
##            print >>sys.stderr, 'got wishlist'
        except:
            wishlist = ''
##            print >>sys.stderr, 'failed wishlist'
##            if bggid == 701:
##                print >>sys.stderr, item.prettify()
##        print >>sys.stderr, 'wishlist:', wishlist
        try:
            parseHash = parseComment(wishlist)
            if 'wtb' in parseHash:
##                print 'wtb:', parseHash['wtb']
                target_price = float(parseHash['wtb'])
##                print >>sys.stderr, 'got target_price'
            else:
                target_price = MAX_PRICE
        except:
            parseHash = { }
            target_price = MAX_PRICE
##            print >>sys.stderr, 'failed target_price'
##        print >>sys.stderr, 'wishlist:', wishlist
##        print >>sys.stderr, 'target_price:', target_price
        # auctionurl needs to be an id
        if (SKIP_STATUS == SKIP_WARN or SKIP_STATUS == SKIP_NOWARN) \
           and auctions_seen.has_key(auctionurl):
                if SKIP_STATUS == SKIP_WARN:
                    print '\nSkipping title "%s", due to old news' \
                      % title
                continue
        auctions_seen[auctionurl] = True
        if currency != '$':
                print 'Skipping id=%d title "%s", due to non-US currency: %s' \
                      % (bggid, title, currency)
                print
                continue
        if price > target_price:
                print 'Skipping id=%d title "%s", price $%.2f exceeds target $%.2f' \
                      % (bggid, title, price, target_price)
                print
                continue
##        print 'bggid:', bggid
##        print 'title:', title
##        print 'auctionurl:', auctionurl
##        print 'auctiontitle:', auctiontitle
##        print 'timeleft:', timeleft
##        print 'currency:', currency
##        print 'price:', '%.2f' % price
##        if target_price == MAX_PRICE:
##            print 'target price: None set'
##        else:
##            print 'target price:', '%.2f' % target_price
##        print
        gameurl = GAME_URL % bggid
        print >>html, '<div style="font-size:125%%;">&nbsp;<A target="_blank" HREF="%s"><B>%s %s</B></A></div>' % (gameurl, title, year)
        print >>html, '<TABLE>'
        print >>html, '<colgroup>'
        print >>html, '    <col width="40%">'
        print >>html, '    <col width="40%">'
        print >>html, '    <col width="20%">'
        print >>html, '</colgroup>'
        print >>html, '<TR>'
        print >>html, '<TD colspan="3"><div style="background-color:#E8E8E8;"><B>&nbsp;Auction Title: </B><A target="_blank" HREF="%s">%s</A></div></TD>' % (auctionurl, auctiontitle)
        print >>html, '</TR>'
        if target_price == MAX_PRICE:
            target = ''
        else:
            target = '(<b>Target: </b>$ %.2f)' % target_price
        print >>html, '<TR>'
        print >>html, '<TD><div style="background-color:#E8E8E8;" ><P><B>&nbsp;Price: </B> %s %.2f&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;%s</P></div></TD>' % (currency, price, target)
        if priority == '1':
            priorityname = 'Must Have'
        elif priority == '2':
            priorityname = 'Love to Have'
        elif priority == '3':
            priorityname = 'Like to Have'
        elif priority == '4':
            priorityname = 'Thinking About It'
        elif priority == '5':
            priorityname = 'DO NOT BUY'
        else:
            priorityname = 'UNKNOWN PRIORITY'
        print >>html, '<TD><div style="background-color:#E8E8E8;" ><P><B>&nbsp;Priority: </B> %s</P></div></TD>' % priorityname
        print >>html, '<TD><div style="background-color:#E8E8E8;" ><P><B>&nbsp;Time Left: </B> %s</P></div></TD>' % timeleft
        print >>html, '</TR>'
        print >>html, '<TR>'
        print >>html, '<TD colspan="3"><div style="background-color:#E8E8E8;"><b>&nbsp;Average: </b>%s&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>Users Rated: </b>%s&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>Bayes: </b>%s&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>Number Owned: </b>%d</div></TD>' % (average, usersrated, bayes, numowned)
        print >>html, '</TR>'
        if wishlist != '':
            print >>html, '<TR>'
            print >>html, '<TD colspan="3"><div style="background-color:#E8E8E8;"><B>&nbsp;Wishlist: </B>%s</div></TD>' % (wishlist)
            print >>html, '</TR>'
        print >>html, '</TABLE>'
        print >>html, '<br/>'
        print >>html, '<br/>'

saveSeenFile(auctions_seen)
##print
##print
##print 'Game bargains found: %d' % n
print >>html, '</BODY>'
print >>html, '</HTML>'
html.close()
webbrowser.open(HTML_FILE)
sys.exit(0)
