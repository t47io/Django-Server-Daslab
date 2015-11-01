import datetime
import subprocess
import sys
import time
import traceback

from django.core.management.base import BaseCommand

from src.settings import *
from src.console import send_notify_slack


class Command(BaseCommand):
    help = 'Uploads MySQL database, static files, Apache2 settings and config settings from local backup/ folder to Google Drive, and deletes expired backup files in Google Drive. Uploaded files will be named with date.'

    def handle(self, *args, **options):
        t0 = time.time()
        self.stdout.write(time.ctime())

        d = time.strftime('%Y%m%d') #datetime.datetime.now().strftime('%Y%m%d')
        gdrive_dir = 'echo'
        if not DEBUG: gdrive_dir = 'cd %s' % APACHE_ROOT
        prefix = ''
        if DEBUG: prefix = '_DEBUG'

        flag = False
        t = time.time()
        self.stdout.write("#1: Uploading MySQL database...")
        try:
            subprocess.check_call('%s && drive upload -f %s/backup/backup_mysql.gz -t DasLab_%s_mysql%s.gz' % (gdrive_dir, MEDIA_ROOT, d, prefix), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError:
            self.stdout.write("    \033[41mERROR\033[0m: Failed to upload \033[94mMySQL\033[0m database.")
            err = traceback.format_exc()
            ts = '%s\t\t%s %s\n' % (time.ctime(), sys.argv[0], sys.argv[1])
            open('%s/cache/log_alert_admin.log' % MEDIA_ROOT, 'a').write(ts)
            open('%s/cache/log_cron_gdrive.log' % MEDIA_ROOT, 'a').write('%s\n%s\n' % (ts, err))
            if IS_SLACK: send_notify_slack(SLACK['ADMIN_NAME'], '', [{"fallback":'ERROR', "mrkdwn_in": ["text"], "color":"danger", "text":'*`ERROR`*: *%s %s* @ _%s_\n>```%s```\n' % (sys.argv[0], sys.argv[1], time.ctime(), err)}])
            flag = True
        else:
            self.stdout.write("    \033[92mSUCCESS\033[0m: \033[94mMySQL\033[0m database uploaded.")
        self.stdout.write("Time elapsed: %.1f s." % (time.time() - t))

        t = time.time()
        self.stdout.write("#2: Uploading static files...")
        try:
            subprocess.check_call('%s && drive upload -f %s/backup/backup_static.tgz -t DasLab_%s_static%s.tgz' % (gdrive_dir, MEDIA_ROOT, d, prefix), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError:
            self.stdout.write("    \033[41mERROR\033[0m: Failed to upload \033[94mstatic\033[0m files.")
            err = traceback.format_exc()
            ts = '%s\t\t%s %s\n' % (time.ctime(), sys.argv[0], sys.argv[1])
            open('%s/cache/log_alert_admin.log' % MEDIA_ROOT, 'a').write(ts)
            open('%s/cache/log_cron_gdrive.log' % MEDIA_ROOT, 'a').write('%s\n%s\n' % (ts, err))
            if IS_SLACK: send_notify_slack(SLACK['ADMIN_NAME'], '', [{"fallback":'ERROR', "mrkdwn_in": ["text"], "color":"danger", "text":'*`ERROR`*: *%s %s* @ _%s_\n>```%s```\n' % (sys.argv[0], sys.argv[1], time.ctime(), err)}])
            flag = True
        else:
            self.stdout.write("    \033[92mSUCCESS\033[0m: \033[94mstatic\033[0m files uploaded.")
        self.stdout.write("Time elapsed: %.1f s." % (time.time() - t))

        t = time.time()
        self.stdout.write("#3: Uploading apache2 settings...")
        try:
            subprocess.check_call('%s && drive upload -f %s/backup/backup_apache.tgz -t DasLab_%s_apache%s.tgz' % (gdrive_dir, MEDIA_ROOT, d, prefix), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError:
            self.stdout.write("    \033[41mERROR\033[0m: Failed to upload \033[94mapache2\033[0m settings.")
            err = traceback.format_exc()
            ts = '%s\t\t%s %s\n' % (time.ctime(), sys.argv[0], sys.argv[1])
            open('%s/cache/log_alert_admin.log' % MEDIA_ROOT, 'a').write(ts)
            open('%s/cache/log_cron_gdrive.log' % MEDIA_ROOT, 'a').write('%s\n%s\n' % (ts, err))
            if IS_SLACK: send_notify_slack(SLACK['ADMIN_NAME'], '', [{"fallback":'ERROR', "mrkdwn_in": ["text"], "color":"danger", "text":'*`ERROR`*: *%s %s* @ _%s_\n>```%s```\n' % (sys.argv[0], sys.argv[1], time.ctime(), err)}])
            flag = True
        else:
            self.stdout.write("    \033[92mSUCCESS\033[0m: \033[94mapache2\033[0m settings uploaded.")
        self.stdout.write("Time elapsed: %.1f s." % (time.time() - t))

        t = time.time()
        self.stdout.write("#4: Uploading config settings...")
        try:
            subprocess.check_call('%s && drive upload -f %s/backup/backup_config.tgz -t DasLab_%s_config%s.tgz' % (gdrive_dir, MEDIA_ROOT, d, prefix), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError:
            self.stdout.write("    \033[41mERROR\033[0m: Failed to upload \033[94mconfig\033[0m settings.")
            err = traceback.format_exc()
            ts = '%s\t\t%s %s\n' % (time.ctime(), sys.argv[0], sys.argv[1])
            open('%s/cache/log_alert_admin.log' % MEDIA_ROOT, 'a').write(ts)
            open('%s/cache/log_cron_gdrive.log' % MEDIA_ROOT, 'a').write('%s\n%s\n' % (ts, err))
            if IS_SLACK: send_notify_slack(SLACK['ADMIN_NAME'], '', [{"fallback":'ERROR', "mrkdwn_in": ["text"], "color":"danger", "text":'*`ERROR`*: *%s %s* @ _%s_\n>```%s```\n' % (sys.argv[0], sys.argv[1], time.ctime(), err)}])
            flag = True
        else:
            self.stdout.write("    \033[92mSUCCESS\033[0m: \033[94mconfig\033[0m settings uploaded.")
        self.stdout.write("Time elapsed: %.1f s." % (time.time() - t))


        t = time.time()
        self.stdout.write("#5: Removing obsolete backups...")
        old = (datetime.date.today() - datetime.timedelta(days=KEEP_BACKUP)).strftime('%Y-%m-%dT00:00:00')

        list_mysql = subprocess.Popen("%s && drive list -q \"title contains 'DasLab' and (title contains '_mysql.gz' or title contains '_mysql_DEBUG.gz') and modifiedDate <= '%s'\"| awk '{ printf $1\" \"}'" % (gdrive_dir, old), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip().split()[1:]
        list_static = subprocess.Popen("%s && drive list -q \"title contains 'DasLab' and (title contains '_static.tgz' or title contains '_static_DEBUG.tgz') and modifiedDate <= '%s'\"| awk '{ printf $1\" \"}'" % (gdrive_dir, old), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip().split()[1:]
        list_apache = subprocess.Popen("%s && drive list -q \"title contains 'DasLab' and (title contains '_apache.tgz' or title contains '_apache_DEBUG.tgz') and modifiedDate <= '%s'\"| awk '{ printf $1\" \"}'" % (gdrive_dir, old), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip().split()[1:]
        list_config = subprocess.Popen("%s && drive list -q \"title contains 'DasLab' and (title contains '_config.tgz' or title contains '_config_DEBUG.tgz') and modifiedDate <= '%s'\"| awk '{ printf $1\" \"}'" % (gdrive_dir, old), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip().split()[1:]
        list_all = list_mysql + list_static + list_apache + list_config

        for id in list_all:
            try:
                subprocess.check_call('%s && drive info -i %s' % (gdrive_dir, id), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                print
                subprocess.check_call('%s && drive delete -i %s' % (gdrive_dir, id), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            except subprocess.CalledProcessError:
                self.stdout.write("    \033[41mERROR\033[0m: Failed to remove obsolete \033[94mbackup\033[0m files.")
                err = traceback.format_exc()
                ts = '%s\t\t%s %s\n' % (time.ctime(), sys.argv[0], sys.argv[1])
                open('%s/cache/log_alert_admin.log' % MEDIA_ROOT, 'a').write(ts)
                open('%s/cache/log_cron_gdrive.log' % MEDIA_ROOT, 'a').write('%s\n%s\n' % (ts, err))
                if IS_SLACK: send_notify_slack(SLACK['ADMIN_NAME'], '', [{"fallback":'ERROR', "mrkdwn_in": ["text"], "color":"danger", "text":'*`ERROR`*: *%s %s* @ _%s_\n>```%s```\n' % (sys.argv[0], sys.argv[1], time.ctime(), err)}])
                flag = True

        if not flag: self.stdout.write("    \033[92mSUCCESS\033[0m: \033[94m%s\033[0m obsolete backup files removed." % len(list_all))
        self.stdout.write("Time elapsed: %.1f s.\n" % (time.time() - t))

        if flag:
            self.stdout.write("Finished with errors!")
            self.stdout.write("Time elapsed: %.1f s." % (time.time() - t0))
            sys.exit(1)
        else:
            self.stdout.write("All done successfully!")
            self.stdout.write("Time elapsed: %.1f s." % (time.time() - t0))
            sys.exit(0)
