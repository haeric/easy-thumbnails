import hashlib

from django.core.files.storage import FileSystemStorage, get_storage_class
from django.utils import six
from django.utils.functional import LazyObject

from easy_thumbnails.conf import settings

class ThumbnailFileSystemStorage(FileSystemStorage):
    """
    Standard file system storage.

    The default ``location`` and ``base_url`` are set to
    ``THUMBNAIL_MEDIA_ROOT`` and ``THUMBNAIL_MEDIA_URL``, falling back to the
    standard ``MEDIA_ROOT`` and ``MEDIA_URL`` if the custom settings are blank.
    """
    def __init__(self, location=None, base_url=None, *args, **kwargs):
        if location is None:
            location = settings.THUMBNAIL_MEDIA_ROOT or None
        if base_url is None:
            base_url = settings.THUMBNAIL_MEDIA_URL or None
        super(ThumbnailFileSystemStorage, self).__init__(
            location, base_url, *args, **kwargs)


class ThumbnailDefaultStorage(LazyObject):
    def _setup(self):
        self._wrapped = get_storage_class(
            settings.THUMBNAIL_DEFAULT_STORAGE)()


def default_storage_hasher(storage):
    """
    Return a hex string hash for a storage object (or string containing
    'full.path.ClassName' referring to a storage object).
    """
    # If storage is wrapped in a lazy object we need to get the real thing.
    if isinstance(storage, LazyObject):
        if storage._wrapped is None:
            storage._setup()
        storage = storage._wrapped
    if not isinstance(storage, six.string_types):
        storage_cls = storage.__class__
        storage = '%s.%s' % (storage_cls.__module__, storage_cls.__name__)
    return hashlib.md5(storage.encode('utf8')).hexdigest()


thumbnail_default_storage = ThumbnailDefaultStorage()
