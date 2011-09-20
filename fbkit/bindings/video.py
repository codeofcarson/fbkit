import httplib
import mimetypes
import urllib2
import urlparse
try:
    import cStringIO as StringIO
except ImportError:
    import StringIO

from .. import proxies, urlread

class VideoProxy(proxies.Proxy):
    """Special proxy for facebook.video."""

    def upload(self, video, aid=None, title=None, description=None, filename=None, uid=None, privacy=None, callback=None):
        """Facebook API call. See http://wiki.developers.facebook.com/index.php/Video.upload"""
        args = {}

        if aid is not None:
            args['aid'] = aid

        if title is not None:
            args['title'] = title

        if description is not None:
            args['description'] = title
            
        if uid is not None:
            args['uid'] = uid

        if privacy is not None:
            args['privacy'] = privacy

        args = self._client._build_post_args('facebook.video.upload', args)

        # check for a filename specified...if the user is passing binary data in
        # video then a filename will be specified
        if filename is None:
            data = StringIO.StringIO(open(video, 'rb').read())
        else:
            # there was a filename specified, which indicates that video was not
            # the path to an video file but rather the binary data of a file
            data = StringIO.StringIO(video)
            video = filename

        content_type, body = self.__encode_multipart_formdata(list(args.iteritems()), [(video, data)])
        
        # Set the correct End Point Url, note this is different to all other FB EndPoints
        urlinfo = urlparse.urlsplit(FACEBOOK_VIDEO_URL)
        try:
            content_length = len(body)
            chunk_size = 4096

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
                raise Exception('Error uploading video: Facebook returned HTTP %s (%s)' % (response.status, response.reason))
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
                    response = urlread.urlread(url=FACEBOOK_VIDEO_URL,
                                               data=body,
                                               headers=response_headers)
                except urllib2.URLError:
                    raise Exception('Error uploading video: Facebook returned %s' % (response))
            except ImportError:
                # could not import from google.appengine.api, so we are
                # not running in GAE
                raise Exception('Error uploading video.')

        return self._client._parse_response(response, 'facebook.video.upload')


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
    'getUploadLimits': [],
}

Proxy = proxies.build_proxy('video', BINDINGS, VideoProxy)
