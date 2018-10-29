'''
Created on 2018年10月8日

@author: moonlit
'''
import wmi
print('修改ip中，耐心候着')

wmiService = wmi.WMI()

colNicConfigs = wmiService.Win32_NetworkAdapterConfiguration(IPEnabled = True)

# for col in colNicConfigs :
#     print(col)

if len(colNicConfigs) < 1:
    print('没有找到可用的网络适配器')
    exit()

# 获取第一个网络适配器的设置
objNicConfig = colNicConfigs[1]

for objNicConfig in colNicConfigs :
    if objNicConfig.Description == "Realtek PCIe GBE Family Controller" :
        break ;

#写入自己的IP地址
arrIPAddresses = ['172.24.195.131']
# arrIPAddresses = ['10.0.0.100']
arrSubnetMasks = ['255.255.255.0']
arrDefaultGateways = ['172.24.195.254']
arrGatewayCostMetrics = [1]
#设置DNS
arrDNSServers = ['223.5.5.5', '114.114.114.114']
intReboot = 0

returnValue = objNicConfig.EnableStatic(IPAddress = arrIPAddresses, SubnetMask = arrSubnetMasks)
if returnValue[0] == 0:
    print('  设置IP ok了')
elif returnValue[0] == 1:
    print('  设置IP ok了')
    intReboot += 1
else:
    print('我靠，出错了')
    exit()

returnValue = objNicConfig.SetGateways(DefaultIPGateway = arrDefaultGateways, GatewayCostMetric = arrGatewayCostMetrics)
if returnValue[0] == 0:
    print(' 网关任务达成')
elif returnValue[0] == 1:
    print('网关任务达成')
    intReboot += 1
else:
    print('我靠，出错了')
    exit()

returnValue = objNicConfig.SetDNSServerSearchOrder(DNSServerSearchOrder = arrDNSServers)
if returnValue[0] == 0:
    print('  成功设置DNS')
elif returnValue[0] == 1:
    print('  成功设置DNS')
    intReboot += 1
else:
    print('我靠，出错了')
    exit()

if intReboot > 0:
    print('重新启动计算机')
else:
    print('')
    print('  修改后的配置为：')
    print('  IP: ', ', '.join(objNicConfig.IPAddress))
    print('  掩码:', ', '.join(objNicConfig.IPSubnet))
    print('  网关:', ', '.join(objNicConfig.DefaultIPGateway))
    print('  DNS:', ', '.join(objNicConfig.DNSServerSearchOrder))

print('收工')
