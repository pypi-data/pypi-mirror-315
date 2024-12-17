import lord_ahrs_driver
import rerun as rr
import json
import time
import gzip

rr.init('imu', spawn=True)

client = lord_ahrs_driver.BufferedAHRSClient("/dev/tty.usbserial-ALBGb121474", 115200, 100, False)
#"/dev/tty.usbserial-ALBGb121474", 115200


now = time.strftime('%Y-%m-%d_%H-%M-%S')
with open(f'full_dump_{now}.json', 'wt') as out:
#with gzip.open(f'full_dump_{now}.json.gz', 'wt') as out:
    while True:
        for ts, data in client.take():
            data['ts'] = ts
            out.write(json.dumps(data) + '\n')
            if data.get('type') == 'sensor':
                #print(data)
                if 'ScaledAccVector' in data:
                    rr.log('acc/acc_x', rr.Scalar(data['ScaledAccVector']['y']))
                    rr.log('acc/acc_y', rr.Scalar(data['ScaledAccVector']['y']))
                    rr.log('acc/acc_z', rr.Scalar(data['ScaledAccVector']['z']))

            if data.get('type') == 'estimate':
                if 'PressureAltitude' in data:
                    rr.log('altitude', rr.Scalar(data['PressureAltitude']['pressure_altitude']))
                if 'LinearAcceleration' in data:
                    rr.log('lin_acc/x', rr.Scalar(data['LinearAcceleration']['x']))
                    rr.log('lin_acc/y', rr.Scalar(data['LinearAcceleration']['y']))
                    rr.log('lin_acc/z', rr.Scalar(data['LinearAcceleration']['z']))
                print(data)

        #    print(data['LinearAcceleration'])