from rest_framework import generics, mixins
from api import settings

# NOTE: these provide similar functionality to the built-in generics API views (but we can make small changes)

# BASE class for the other generic API views to inherit from
class GenericAPIView(generics.GenericAPIView):

    permission_classes = settings.STANDARD_PERMISSIONS
    is_user = False

    def get_queryset(self):
        queryset = super(GenericView, self).get_queryset()

        user = self.request.user
        profile = None
        if not user.is_anonymous():
            profile = user.profile

        if not user.is_superuser:
            if self.is_user:
                queryset = queryset.filter(id=user.id)

        return queryset

# view for API model instance
class CreateAPIView(mixins.CreateModelMixin, GenericAPIView):

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save()

# view for listing API queryset
class ListAPIView(mixins.ListModelMixin, GenericAPIView):

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

# view for retrieving API model instance
class RetrieveAPIView(mixins.RetrieveModelMixin, GenericAPIView):

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

# view for listing API queryset or creating API model instance
class ListCreateAPIView(mixins.ListModelMixin, mixins.CreateModelMixin, GenericAPIView):

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_Create(self, serializer):
        serializer.save()

# view for retrieving/updating API model instance
class RetrieveUpdateAPIView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, GenericAPIView):

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


# view for retrieving/updating/deleting API model instance
class RetrieveUpdateDestroyAPIView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericAPIView):

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
