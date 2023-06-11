import requests
from flask import Flask, request

from datetime import datetime, timedelta

headers = {"Content-Type": "application/json"}
url = 'https://b24-mej2h3.bitrix24.ru/rest/1/ushez2nefb807rcd/'

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def receiver():
    deal_id = request.args.get('deal_id')
    action = request.args.get('action')

    if action == 'confirm':
        update_deal_stage(deal_id)

    elif action == 'decline':
       create_activity(deal_id)

       
    return 'ok'


def update_deal_stage(deal_id):

    params = {
        "id": deal_id,
        "fields": {
            "STAGE_ID": 1
        }
    }

    requests.post(f'{url}crm.deal.update.json', headers=headers, json=params)


def create_activity(deal_id):

    activity_deadline = datetime.now() + timedelta(hours=1)
    requests.get(f'{url}crm.activity.todo.add?ownerTypeId=2&ownerId={deal_id}&deadline={activity_deadline}&description=Запись отменена клиентом. Связаться с клиентом')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8002, debug=True)