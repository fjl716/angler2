from wechatpy import WeChatClient

from angler.service import IService


from wechatpy.session import SessionStorage


class CustomStorage(SessionStorage):

    def __init__(self, *args, **kwargs):
        pass

    def get(self, key, default=None):
        pass

    def set(self, key, value, ttl=None):
        pass

    def delete(self, key):
        pass


class WeChat(IService):
    def __init__(self, name, app_id, secret):
        IService.__init__(self, name)
        self.app_id = app_id
        self.secret = secret
        self.client = None

    def create_temp_qrcode(self, expire_seconds, scene_id):
        return self.client.qrcode.create({
            'expire_seconds': 1800,
            'action_name': 'QR_LIMIT_SCENE',
            'action_info': {
                'scene': {'scene_id': scene_id},
            }
        })

    def create_qrcode(self, scene_id):
        return self.client.qrcode.create({
            'expire_seconds': 1800,
            'action_name': 'QR_SCENE',
            'action_info': {
                'scene': {'scene_id': scene_id},
            }
        })

    def stop(self):
        pass

    def start(self, angler):
        print(angler.services.keys())
        self.client = WeChatClient(
            self.app_id,
            self.secret,
            session=angler.services['cache']
        )


def factory(name, conf):
    return WeChat(
        name,
        conf['app_id'],
        conf['secret'],
    )
