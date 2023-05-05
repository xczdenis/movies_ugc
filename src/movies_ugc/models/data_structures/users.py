from movies_ugc.models.data_structures.mixins import OrjsonConfigMixin, UUIDMixin


class User(UUIDMixin, OrjsonConfigMixin):
    pass
