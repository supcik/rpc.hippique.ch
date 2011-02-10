from SimpleXMLRPCServer import SimpleXMLRPCDispatcher
from django.http import HttpResponse
from django.conf import settings
from lxml import etree
from urllib2 import urlopen
import re

try: # Try to import memcache
    import memcache
    memcache_loaded = True
except ImportError:
    memcache_loaded = False 

dispatcher = SimpleXMLRPCDispatcher(allow_none=False, encoding=None)

def rpc_handler(request):

    if len(request.POST):
        response = HttpResponse(mimetype="application/xml")
        response.write(dispatcher._marshaled_dispatch(request.raw_post_data))
    else:
        response = HttpResponse()
        response.write("<b>This is an XML-RPC Service.</b><br>")
        response.write("You need to invoke it using an XML-RPC Client!<br>")
        response.write("The following methods are available:<ul>")
        methods = dispatcher.system_listMethods()

        for method in methods:
            sig = dispatcher.system_methodSignature(method)
            help =  dispatcher.system_methodHelp(method)
            response.write("<li><b>%s</b>: [%s] %s" % (method, sig, help))

        response.write("</ul>")
        response.write('<a href="http://www.djangoproject.com/"> <img src="http://media.djangoproject.com/img/badges/djangomade124x25_grey.gif" border="0" alt="Made with Django." title="Made with Django."></a>')

    response['Content-length'] = str(len(response.content))
    return response

def record_info (rec_class, rec_id):
    if memcache_loaded:
        mc = memcache.Client([settings.MEMCACHED_HOST], debug=0)
        mc_key = "fnch:%s:%s" % (rec_class, rec_id)
        mc_val = mc.get(mc_key)
        if mc_val is not None:
            return mc_val

    url = 'http://www.fnch.ch/component/option,com_fnch_yearbook/' + \
          'Itemid,175/task,%s/id,%s/' % (rec_class, rec_id)

    fd     = urlopen(url)
    parser = etree.HTMLParser()
    tree   = etree.parse(fd, parser)
    result = {
        'rec_id'   : rec_id,
        'rec_class': rec_class
    }

    # Get general Inio
    table = tree.find(".//table[@class='%s']" % rec_class)
    if table is not None:
        for tr in table.iterfind('tr'):
            td = tr.findall('td')
            if len(td) >= 2:
                key = td[0].text
                if td[1].text is not None:
                    value = td[1].text
                else:
                    value = ''.join(map(lambda x: x.text, list(td[1])))
                if key is not None and value is not None:
                    result[key] = value

    # Get earning and points
    for tclass in ['sumsyearbook', 'pointsyearbook']:
        table = tree.find(".//table[@class='%s']" % tclass)
        if table is not None:
            for tr in table.iterfind('tr'):
                (key, val) = (None, None)
                td = tr.findall('td')
                if len(td) >= 2:
                    key = td[0].text
                    val = re.sub(r'\D', '', td[1].text)
                    if tclass not in result:
                        result[tclass] = {key: val}
                    elif not key in result[tclass]:
                        result[tclass][key] = val

    if memcache_loaded:
        mc.set(mc_key, result, time=settings.MEMCACHED_TTL)
    return result

def rider_info (id):
    return record_info('rider', id)

def horse_info (id):
    return record_info('horse', id)

dispatcher.register_function(horse_info, 'horse_info')
dispatcher.register_function(rider_info, 'rider_info')

