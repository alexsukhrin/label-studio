def permission_required(*permissions, fn=None):

    def decorator(view):
        def wrapped_view(self, request, *args, **kwargs):

            obj = fn(request, *args, **kwargs) if callable(fn) else fn
            missing_permissions = [perm for perm in permissions
                                   if not request.user.has_perm(perm, obj)]
            if any(missing_permissions):
                # raises a permission denied exception causing a 403 response
                self.permission_denied(
                    request,
                    message=('Permission denied: {}'
                             .format(', '.join(missing_permissions)))
                )

            return view(self, request, *args, **kwargs)

        return wrapped_view

    return decorator
