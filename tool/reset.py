import redis ,sys
sys.path.append("..")
from lib.dispatchUrl import DispatchUrl
rd = redis.Redis(host='192.168.30.128', port=6379, password='gao123456',decode_responses=True)

#任务名称 要重新执行的任务名称 切记要谨慎执行
#taskName = 'cnedu_ky'
taskName = 'csdn'
#为了安全我这里 去掉下面注释执行

dispatch =DispatchUrl(taskName)
dispatch.reset()
print("执行完毕")





