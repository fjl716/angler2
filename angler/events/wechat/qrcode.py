import random


def factory(params):
    result_event = params.get('result')

    def invoke(services, packet, response):
        result = services['wechat'].create_temp_qrcode(1800, int(random.randint(1, 100000)))
        response.send({
            'event': result_event,
            'data': result,
            'remote': True
        })
    return {
        'result': [result_event],
        'invoke': invoke
    }
