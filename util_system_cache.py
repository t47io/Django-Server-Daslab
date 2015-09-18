# from collections import defaultdict
# from datetime import date, datetime, timedelta
import os
import pickle
import simplejson
import subprocess
import sys
import time
import traceback

sys.path.append(os.path.abspath('.'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings") 

from src.settings import *
from src.console import *
from src.dash import *


def pickle_aws(request, name):
    f_name = '%s/cache/aws/%s_%s_%s.pickle' % (MEDIA_ROOT, request['tp'], name, request['qs'])
    f = open(f_name + '_tmp', 'wb')
    pickle.dump(cache_aws(request), f)
    f.close()
    subprocess.check_call("mv %s_tmp %s" % (f_name, f_name), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

def pickle_git(request):
    f_name = '%s/cache/git/%s_%s.pickle' % (MEDIA_ROOT, request['repo'], request['qs'])
    f = open(f_name + '_tmp', 'wb')
    pickle.dump(cache_git(request), f)
    f.close()
    subprocess.check_call("mv %s_tmp %s" % (f_name, f_name), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

def pickle_slack(request):
    f_name = '%s/cache/slack/%s.pickle' % (MEDIA_ROOT, request['qs'])
    f = open(f_name + '_tmp', 'wb')
    pickle.dump(cache_slack(request), f)
    f.close()
    subprocess.check_call("mv %s_tmp %s" % (f_name, f_name), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

def pickle_dropbox(request):
    f_name = '%s/cache/dropbox/%s.pickle' % (MEDIA_ROOT, request['qs'])
    f = open(f_name + '_tmp', 'wb')
    pickle.dump(cache_dropbox(request), f)
    f.close()
    subprocess.check_call("mv %s_tmp %s" % (f_name, f_name), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def main():
    t0 = time.time()
    print time.ctime()
    t = time.time()

    if len(sys.argv) > 1:
        is_3, is_15, is_30 = False, False, False
        is_3 = (sys.argv[1] == '3')
        is_15 = (sys.argv[1] == '15')
        is_30 = (sys.argv[1] == '30')
    else:
        is_3, is_15, is_30 = True, True, True

    try:
        if is_3:
            # slack
            print "#4: Requesting \033[94mSLACK\033[0m..."
            requests = ['home']
            for i, request in enumerate(requests):
                print "    SLACK: %s / %s (%s)..." % (i + 1, len(requests), request)
                request = {'qs':request}
                git_init = cache_slack(request)
                pickle_slack(request)
        else:
            print "#4: Skip SLACK \033[94mhome\033[0m..."


        if is_15:
            # aws init
            print "#1: Requesting \033[94mAWS\033[0m..."
            request = {'qs':'init'}
            aws_init = cache_aws(request)
            f = open('%s/cache/aws/init.pickle' % MEDIA_ROOT, 'wb')
            pickle.dump(aws_init, f)
            f.close()
            aws_init = simplejson.loads(aws_init)
            print "    AWS \033[94minit\033[0m finished with \033[92mSUCCESS\033[0m."

            # aws each
            for i, ec2 in enumerate(aws_init['ec2']):
                print "    AWS \033[94mEC2\033[0m: %s / %s (%s)..." % (i + 1, len(aws_init['ec2']), ec2['id']),
                request = {'qs':'cpu', 'tp':'ec2', 'id':ec2['id']}
                pickle_aws(request, ec2['id'])
                request.update({'qs':'net'})
                pickle_aws(request, ec2['id'])
                print " \033[92mSUCCESS\033[0m"

            for i, elb in enumerate(aws_init['elb']):
                print "    AWS \033[94mELB\033[0m: %s / %s (%s)..." % (i + 1, len(aws_init['elb']), elb['name']),
                request = {'qs':'lat', 'tp':'elb', 'id':elb['name']}
                pickle_aws(request, elb['name'])
                request.update({'qs':'req'})
                pickle_aws(request, elb['name'])
                print " \033[92mSUCCESS\033[0m"

            for i, ebs in enumerate(aws_init['ebs']):
                print "    AWS \033[94mEBS\033[0m: %s / %s (%s)..." % (i + 1, len(aws_init['ebs']), ebs['id']),
                request = {'qs':'disk', 'tp':'ebs', 'id':ebs['id']}
                pickle_aws(request, ebs['id'])
                print " \033[92mSUCCESS\033[0m"

            # ga
            print "#2: Requesting \033[94mGA\033[0m..."
            f = open('%s/cache/ga.pickle' % MEDIA_ROOT, 'wb')
            pickle.dump(cache_ga(), f)
            f.close()
            print "    GA \033[94minit\033[0m finished with \033[92mSUCCESS\033[0m."
        else:
            print "#1: Skip \033[94mAWS\033[0m..."
            print "#2: Skip \033[94mGA\033[0m..."


        if is_30:
            # git init
            print "#3: Requesting \033[94mGIT\033[0m..."
            request = {'qs':'init'}
            git_init = cache_git(request)
            f = open('%s/cache/git/init.pickle' % MEDIA_ROOT, 'wb')
            pickle.dump(git_init, f)
            f.close()
            git_init = simplejson.loads(git_init)
            print "    GIT \033[94minit\033[0m finished with \033[92mSUCCESS\033[0m."

            # git each
            for i, repo in enumerate(git_init['git']):
                print "    GIT \033[94mrepo\033[0m: %s / %s (%s)..." % (i + 1, len(git_init['git']), repo['name']),
                request = {'qs':'num', 'repo':repo['name']}
                pickle_git(request)
                request.update({'qs':'c'})
                pickle_git(request)
                request.update({'qs':'ad'})
                pickle_git(request)
                print " \033[92mSUCCESS\033[0m"

            # slack
            print "#4: Requesting \033[94mSLACK\033[0m..."
            requests = ['users', 'channels', 'files', 'plot_files', 'plot_msgs']
            for i, request in enumerate(requests):
                print "    SLACK: %s / %s (%s)..." % (i + 1, len(requests), request),
                request = {'qs':request}
                git_init = cache_slack(request)
                pickle_slack(request)
                print " \033[92mSUCCESS\033[0m"

            # dropbox
            print "#5: Requesting \033[94mDROPBOX\033[0m..."
            requests = ['sizes', 'folders', 'history']
            for i, request in enumerate(requests):
                print "    DROPBOX: %s / %s (%s)..." % (i + 1, len(requests), request),
                request = {'qs':request}
                git_init = cache_dropbox(request)
                pickle_dropbox(request)
                print " \033[92mSUCCESS\033[0m"

            # schedule
            print "#6: Requesting \033[94mSchedule Spreadsheet\033[0m..."
            f = open('%s/cache/schedule.pickle' % MEDIA_ROOT, 'wb')
            pickle.dump(cache_schedule(), f)
            f.close()
            print "    Schedule finished with \033[92mSUCCESS\033[0m."

            # cal
            print "#7: Requesting \033[94mGoogle Calendar\033[0m..."
            f = open('%s/cache/calendar.pickle' % MEDIA_ROOT, 'wb')
            pickle.dump(cache_cal(), f)
            f.close()
            print "    Calendar finished with \033[92mSUCCESS\033[0m."
        else:
            print "#3: Skip \033[94mGIT\033[0m..."
            print "#4: Skip \033[94mSLACK\033[0m..."
            print "#5: Skip \033[94mDROPBOX\033[0m..."
            print "#7: Skip \033[94mSchedule Spreadsheet\033[0m..."
            print "#7: Skip \033[94mGoogle Calendar\033[0m..."
    except:
        print traceback.format_exc()
        print "Finished with \033[41mERROR\033[0m!"
        print "Time elapsed: %.1f s." % (time.time() - t0)
        sys.exit(1)

    print "Finished with \033[92mSUCCESS\033[0m!"
    print "Time elapsed: %.1f s." % (time.time() - t0)
    sys.exit(0)


if __name__ == "__main__": 
    main()
