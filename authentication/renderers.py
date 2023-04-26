from rest_framework import renderers
import json

class UserRenderer(renderers.JSONRenderer):
    charset='utf-8'
    #override render function
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response=''
        #customizing our way of sending the response , if error details is present in the response then
        if 'ErrorDetail' in str(data):
            response=json.dumps({'Oops! We got something wrong.':data})
        else:
            response=json.dumps({'Here is your data.':data})
        # import pdb
        # pdb.set_trace()
        return response