"""
information extractions from the VM filename ©PCo2022
"""
import os


class VmFilename:

    def __init__(self, filename):
        """
        >>> vf.name
        'web1'
        >>> vf.ext
        '.txt'
        >>> vf.path
        'D:/Philippe/Desktop/LAC_SIO_2021/vmslinux/heartbeat-HA-FO'
        >>> vf.fullname
        'D:/Philippe/Desktop/LAC_SIO_2021/vmslinux/heartbeat-HA-FO/web1.txt'
        >>> vf.last_dir
        'heartbeat-HA-FO'
        >>> vf.url
        'file://D:/Philippe/Desktop/LAC_SIO_2021/vmslinux/heartbeat-HA-FO/web1.html'
        >>> vf.schema
        'heartbeat-HA-FO.png'
        """
        self.fullname = (os.path.normpath(os.path.abspath(filename))).replace(os.path.sep, '/')
        self.path = os.path.dirname(self.fullname)
        dirs = self.path.split('/')
        self.last_dir = dirs[-1] if len(dirs) > 0 else ""
        self.basename = os.path.basename(self.fullname)
        self.name, self.ext = os.path.splitext(self.basename)
        self.html = self.path + '/' + self.name + '.html'
        self.url = 'file://' + self.html
        self.schema = self.last_dir + '.png'
        if not os.path.isfile(self.path + '/' + self.schema):
            self.schema = None


if __name__ == "__main__":
    import doctest
    paths = (
        "D:\\Philippe\\Desktop\\LAC_SIO_2021\\vmslinux\\heartbeat-HA-FO\\web1.txt",
        "D:/Philippe/Desktop/LAC_SIO_2021/vmslinux/heartbeat-HA-FO/web1.txt",
        "../heartbeat-HA-FO/web1.txt"
    )
    for path in paths:
        doctest.testmod(extraglobs={'vf': VmFilename(path)})
