import re
import os
import datetime
import time
from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def receiver():
    phone_number  = request.args.get('phone')
    deal_date = request.args.get('deal_date')
    deal_id = request.args.get('deal_id')

    if not phone_number or not deal_date or not deal_id:
        print("Missing variables", 400)
        return "Missing variables", 400

    # Проверка номера телефона
    phone_pattern = r'^7\d{10}$'
    if not re.match(phone_pattern, phone_number):
        print("Invalid phone number format", 400)
        return "Invalid phone number format", 400

    datetime_obj = datetime.datetime.strptime(deal_date, "%d.%m.%Y %H:%M:%S")
    unix_time = time.mktime(datetime_obj.timetuple())

    call_file = open(f'tmp/{phone_number}_{deal_id}.call', 'a+')
    call_file.write(f'Channel: PJSIP/{phone_number}@tele2\n')
    call_file.write(f'MaxRetries: 5\n')
    call_file.write(f'RetryTime: 60\n')
    call_file.write(f'WaitTime: 30\n')
    call_file.write(f'Priority: 1\n')
    call_file.write(f'Context: autodialer\n')
    call_file.write(f'Extension: 100\n')
    call_file.write(f'CallerID: "AutoDialer" <{phone_number}>\n')
    call_file.write(f'Set: DEALID={deal_id}\n')
    call_file.write(f'Set: say_time={unix_time}')
    call_file.close()

    os.rename(f'tmp/{phone_number}_{deal_id}.call', f'/var/spool/asterisk/outgoing/{phone_number}_{deal_id}.call')

    return "File created successfully", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8001, debug=True)
