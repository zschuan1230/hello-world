#coding=utf-8
import jenkins
import time
# url = 'http://jenkins.ysskj.com/view/%E4%BA%91%E5%B9%B3%E5%8F%B0-QA/'
url = 'http://jenkins.ysskj.com/'
jenkinsObject = jenkins.Jenkins(url=url, username='liyuan', password='liyuan')
# job_info = jenkinsObject.get_job_info('qa-supervise-cloud')
# print(job_info)
#
# build_info = jenkinsObject.get_build_info('qa-supervise-cloud', 31)
#
# print("*"*20)
# print(build_info)

# report_info = jenkinsObject.get_all_jobs()
# print(report_info)

# jenkinsObject.build_job('qa-supervise-eeop')
#
# time.sleep(40)
# runningObject = jenkinsObject.get_running_builds()
# print(runningObject)


# last_build_info = jenkinsObject.get_job_info('qa-supervise-eeop')
# print(last_build_info)

result = jenkinsObject.get_build_info('qa-yss-pay-consumer', 30)
print(result)

