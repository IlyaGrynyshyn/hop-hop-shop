from rest_framework.renderers import JSONRenderer


class SuccessJsonResponsee(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if not renderer_context["response"].exception:
            data = {"success": True, "data": data}
        return super(SuccessJsonResponsee, self).render(
            data, accepted_media_type, renderer_context
        )
