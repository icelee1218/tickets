import json
import requests
import re
import sys
from pprint import pprint
from docopt import docopt
from stations_name import stations
from stations_name import stations_res
from prettytable import PrettyTable

'''url1 = 'https://kyfw.12306.cn/otn/leftTicket/queryA?leftTicketDTO.train_date=2018-10-04&leftTicketDTO.from_station=BJP&leftTicketDTO.to_station=SHH&purpose_codes=ADULT'
txt = requests.get(url1).text
print(txt)'''


def usage():
    print("Example: tickets.py 2018-01-01 北京 上海")


def get_json(url, date, fro, to, purp):
    url = url + '?leftTicketDTO.train_date=' + date + '&leftTicketDTO.from_station=' + fro + '&leftTicketDTO.to_station=' + to + '&purpose_codes=' + purp
    return json.loads(requests.get(url).text)


def list_ticket():
    if len(sys.argv) > 3:     
        dte = sys.argv[1]
        fro = stations.get(sys.argv[2])
        too = stations.get(sys.argv[3])
        json_result = get_json('https://kyfw.12306.cn/otn/leftTicket/queryA', dte, fro, too, 'ADULT')
        '''print(json_result)'''
        list_tickets = json_result['data']['result']
        pt = PrettyTable()
        pt._set_field_names('车次 始发站 终点站 出发站 到达站 出发时间 到达时间 历时 商务座 一等座 二等座 软卧 硬卧 软座 硬座 无座 备注'.split())
        for ticket in list_tickets:
            list_ticket_item = ticket.split('|')
            pt.add_row([list_ticket_item[3], stations_res.get(list_ticket_item[4]),
                        stations_res.get(list_ticket_item[5]),
                        stations_res.get(list_ticket_item[6]), stations_res.get(list_ticket_item[7]),
                        list_ticket_item[8], list_ticket_item[9], list_ticket_item[10], list_ticket_item[32],
                        list_ticket_item[31],
                        list_ticket_item[30], list_ticket_item[23], list_ticket_item[28], list_ticket_item[24],
                        list_ticket_item[29], list_ticket_item[26], list_ticket_item[11]])
        print(pt)
    else:
        usage()


def get_station_name():
    url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9069'
    response = requests.get(url, verify=False) 
    stat = re.findall(u'([\u4e00-\u9fa5]+)+\|([A-Z]+)', response.text)
    '''pprint(dict(stat), indent=4)'''
    dict_res = dict(stat)
    dict_res = dict(zip(dict_res.values(), dict_res.keys()))
    pprint(dict_res)


list_ticket()
'''get_station_name()'''