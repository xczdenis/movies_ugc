from models.mixins import OrjsonConfigMixin, StrUUIDMixin


class User(StrUUIDMixin, OrjsonConfigMixin):
    pass
