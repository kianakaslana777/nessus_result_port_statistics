import re

ports = ['21', '22', '23', '69', '1433', '1521', '3306', '3389', '5432', '6379', '27017']
services = ['ftp', 'ssh', 'telnet', 'tftp', 'mssql', 'oracle', 'mysql', 'msrdp', 'postgres', 'redis', 'mongodb']
ip_pattern = re.compile(r'\d+\.\d+\.\d+\.\d+')
service_pattern = re.compile(r'\s[a-z]+\s\t')
port_pattern = re.compile(r'\n\d+\s')


def create_pattern(services, ports):
    services_pattern = locals()
    for i in services:
        # services_pattern['pattern_ps_' + str(i)] = re.compile(r'\n{}\s/\stcp\s/\s{}\s\t\n(\d+\.\d+\.\d+\.\d+\n)+'.format(i, ports[services.index(i)]))
        services_pattern['pattern_ps_' + str(i)] = re.compile(r'\n{}\s/\stcp\s/\s{}\s\t\n[\d+\.\d+\.\d+\.\d+\n]+'.format(ports[services.index(i)], i))
        services_pattern['pattern_s_' + str(i)] = re.compile(r'\n\d+\s/\stcp\s/\s{}\s\t\n[\d+\.\d+\.\d+\.\d+\n]+'.format(i))
        services_pattern['pattern_p_' + str(i)] = re.compile(r'\n{}\s/\stcp\s\t\n[\d+\.\d+\.\d+\.\d+\n]+'.format(ports[services.index(i)]))
    return services_pattern


def create_list(services):
    service_list = locals()
    for i in services:
        service_list[str(i) + '_list'] = []
    return service_list


def find(s, services, ports):
    services_pattern = create_pattern(services, ports)
    service_list = create_list(services)
    print(s)
    for i in services:
        print(i + ':' + '\n')
        print(services_pattern['pattern_ps_' + str(i)])
        sps = services_pattern['pattern_ps_' + str(i)].findall(s)
        ss = services_pattern['pattern_s_' + str(i)].findall(s)
        sp = services_pattern['pattern_p_' + str(i)].findall(s)
        # print(ss)
        r = list(set(sps + ss + sp))
        for j in r:
            service = i
            port = port_pattern.findall(j)[0].strip()
            ip = ip_pattern.findall(j)
            for k in ip:
                r = k + ':' + port + '/' + service
                service_list[service + '_list'].append(r)
        # service_list[str(i) + '_list'] = r
    # print(services_pattern)
    print(service_list)
    return service_list


def write2txt(service_list, services):
    with open('result.txt', 'a') as f:
            for i in services:
                for j in service_list[str(i) + '_list']:
                    f.write(j + '\n')
    f.close()


def read_file():
    with open('/Users/kiana/Desktop/自有资产端口统计.txt') as f:
        s = ''
        for i in f.readlines():
            s += i
        return s


if __name__ == '__main__':
    s = read_file()
    services_list = find(s, services, ports)
    write2txt(services_list, services)

