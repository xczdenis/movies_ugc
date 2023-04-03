from models.mixins import StrUUIDMixin, OrjsonConfigMixin


class User(StrUUIDMixin, OrjsonConfigMixin):
    pass
