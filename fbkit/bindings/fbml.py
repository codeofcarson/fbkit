from .. import proxies

BINDINGS = {
    'refreshImgSrc': [
        ('url', str, {}),
    ],
    'refreshRefUrl': [
        ('url', str, {}),
    ],
    'setRefHandle': [
        ('handle', str, {}),
        ('fbml', str, {}),
    ],
}

Proxy = proxies.build_proxy('fbml', BINDINGS)
