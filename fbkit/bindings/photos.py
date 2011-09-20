import httplib
import mimetypes
import urllib2
import urlparse
try:
    import cStringIO as StringIO
except ImportError:
    import StringIO

from .. import proxies, urlread

class PhotosProxy(proxies.Proxy):
    """Special proxy for facebook.photos."""

    def upload(self, image, aid=None, uid=None, caption=None, size=(720, 720), filename=None, callback=None):
        """Facebook API call. See http://developers.facebook.com/documentation.php?v=1.0&method=photos.upload

        size -- an optional size (width, height) to resize the image to before uploading. Resizes by default
                to Facebook's maximum display dimension of 720.
        """
        args = {}

        if uid is not None:
            args['uid'] = uid

        if aid is not None:
            args['aid'] = aid

        if caption is not None:
            args['caption'] = caption

        if self._client.oauth2:
            url = self._client.facebook_secure_url
        else:
            url = self._client.facebook_url

        args = self._client._build_post_args('facebook.photos.upload', args)

        # check for a filename specified...if the user is passing binary data in
        # image then a filename will be specified
        if filename is None:
            try:
                import Image
            except ImportError:
                data = StringIO.StringIO(open(image, 'rb').read())
            else:
                img = Image.open(image)
                if size:
                    img.thumbnail(size, Image.ANTIALIAS)
                data = StringIO.StringIO()
                img.save(data, img.format)
        else:
            # there was a filename specified, which indicates that image was not
            # the path to an image file but rather the binary data of a file
            data = StringIO.StringIO(image)
            image = filename

        content_type, body = self.__encode_multipart_formdata(list(args.iteritems()), [(image, data)])
        urlinfo = urlparse.urlsplit(url)
        try:
            content_length = len(body)
            chunk_size = 4096

            if self._client.oauth2:
                h = httplib.HTTPSConnection(urlinfo[1])
            else:
                h = httplib.HTTPConnection(urlinfo[1])
            h.putrequest('POST', urlinfo[2])
            h.putheader('Content-Type', content_type)
            h.putheader('Content-Length', str(content_length))
            h.putheader('MIME-Version', '1.0')
            h.putheader('User-Agent', 'PyFacebook Client Library')
            h.endheaders()

            if callback:
                count = 0
                while len(body) > 0:
                    if len(body) < chunk_size:
                        data = body
                        body = ''
                    else:
                        data = body[0:chunk_size]
                        body = body[chunk_size:]

                    h.send(data)
                    count += 1
                    callback(count, chunk_size, content_length)
            else:
                h.send(body)

            response = h.getresponse()

            if response.status != 200:
                raise Exception('Error uploading photo: Facebook returned HTTP '
                                '%s (%s)' % (response.status, response.reason))
            response = response.read()
        except:
            # sending the photo failed, perhaps we are using GAE
            try:
                try:
                    response_headers = {
                        'POST':urlinfo[2],
                        'Content-Type':content_type,
                        'MIME-Version':'1.0'
                    }
                    response = urlread.urlread(url=url,
                                               data=body,
                                               headers=response_headers)
                except urllib2.URLError:
                    raise Exception('Error uploading photo: Facebook returned '
                                    '%s' % (response))
            except ImportError:
                # could not import from google.appengine.api, so we are not running in GAE
                raise Exception('Error uploading photo.')

        return self._client._parse_response(response, 'facebook.photos.upload')


    def __encode_multipart_formdata(self, fields, files):
        """Encodes a multipart/form-data message to upload an image."""
        boundary = '-------tHISiStheMulTIFoRMbOUNDaRY'
        crlf = '\r\n'
        l = []

        for (key, value) in fields:
            l.append('--' + boundary)
            l.append('Content-Disposition: form-data; name="%s"' % str(key))
            l.append('')
            l.append(str(value))
        for (filename, value) in files:
            l.append('--' + boundary)
            l.append('Content-Disposition: form-data; filename="%s"' % (str(filename), ))
            l.append('Content-Type: %s' % self.__get_content_type(filename))
            l.append('')
            l.append(value.getvalue())
        l.append('--' + boundary + '--')
        l.append('')
        body = crlf.join(l)
        content_type = 'multipart/form-data; boundary=%s' % boundary
        return content_type, body


    def __get_content_type(self, filename):
        """Returns a guess at the MIME type of the file from the filename."""
        return str(mimetypes.guess_type(filename)[0]) or 'application/octet-stream'

BINDINGS = {
    'addTag': [
        ('pid', int, {}),
        ('tag_uid', int, {'default': 0}),
        ('tag_text', str, {'default': ''}),
        ('x', float, {'default': 50}),
        ('y', float, {'default': 50}),
        ('tags', proxies.json, {'optional': True}),
    ],
    'createAlbum': [
        ('name', str, {}),
        ('location', str, {'optional': True}),
        ('description', str, {'optional': True}),
    ],
    'get': [
        ('subj_id', int, {'optional': True}),
        ('aid', int, {'optional': True}),
        ('pids', list, {'optional': True}),
    ],
    'getAlbums': [
        ('uid', int, {'optional': True}),
        ('aids', list, {'optional': True}),
    ],
    'getTags': [
        ('pids', list, {}),
    ],
}

Proxy = proxies.build_proxy('photos', BINDINGS, PhotosProxy)
