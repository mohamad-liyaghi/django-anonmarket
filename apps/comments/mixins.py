from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType

class ObjectMixin:
    """
    Mixin to retrieve content type model and object based on content_type_id and object_id URL parameters.
    """
    def dispatch(self, request, *args, **kwargs):
        content_type = get_object_or_404(ContentType, pk=self.kwargs['content_type_id'])
        model_class = content_type.model_class()
        self.object = get_object_or_404(model_class, pk=self.kwargs['object_id'])
        return super().dispatch(request, *args, **kwargs)