import random


def factory(result):
    def invoke(services, packet, response):
        qrcode = services['wechat'].create_temp_qrcode(1800, int(random.randint(1, 100000)))
        response.send({
            'event': result,
            'data': qrcode['ticket'],
            'remote': True
        })
    return {
        'result': [result],
        'invoke': invoke
    }
