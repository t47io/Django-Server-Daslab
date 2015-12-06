import subprocess
import sys
import time
import traceback

from django.core.management.base import BaseCommand

from src.settings import *
from src.console import get_date_time, get_backup_stat, send_notify_slack


class Command(BaseCommand):
    help = 'Backups MySQL database, static files, Apache2 settings and config settings to local backup/ folder. Existing backup files will be overwritten.'

    def handle(self, *args, **options):
        t0 = time.time()
        self.stdout.write('%s:\t%s' % (time.ctime(), ' '.join(sys.argv)))
         
        flag = False
        t = time.time()
        self.stdout.write("#1: Backing up MySQL database...")
        try:
            subprocess.check_call('mysqldump --quick %s -u %s -p%s > %s/backup/backup_mysql' % (env.db()['NAME'], env.db()['USER'], env.db()['PASSWORD'], MEDIA_ROOT), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            subprocess.check_call('gzip -f %s/backup/backup_mysql' % MEDIA_ROOT, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError:
            self.stdout.write("    \033[41mERROR\033[0m: Failed to dump \033[94mMySQL\033[0m database.")
            err = traceback.format_exc()
            ts = '%s\t\t%s\n' % (time.ctime(), ' '.join(sys.argv))
            open('%s/cache/log_alert_admin.log' % MEDIA_ROOT, 'a').write(ts)
            open('%s/cache/log_cron_backup.log' % MEDIA_ROOT, 'a').write('%s\n%s\n' % (ts, err))
            if IS_SLACK: send_notify_slack(SLACK['ADMIN_NAME'], '', [{"fallback":'ERROR', "mrkdwn_in": ["text"], "color":"danger", "text":'*`ERROR`*: *%s* @ _%s_\n>```%s```\n' % (' '.join(sys.argv), time.ctime(), err)}])
            flag = True
        else:
            self.stdout.write("    \033[92mSUCCESS\033[0m: \033[94mMySQL\033[0m database dumped.")
        self.stdout.write("Time elapsed: %.1f s." % (time.time() - t))

        t = time.time()
        self.stdout.write("#2: Backing up static files...")
        try:
            subprocess.check_call('cd %s && tar zcf backup/backup_static.tgz data/' % MEDIA_ROOT, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError:
            self.stdout.write("    \033[41mERROR\033[0m: Failed to archive \033[94mstatic\033[0m files.")
            err = traceback.format_exc()
            ts = '%s\t\t%s\n' % (time.ctime(), ' '.join(sys.argv))
            open('%s/cache/log_alert_admin.log' % MEDIA_ROOT, 'a').write(ts)
            open('%s/cache/log_cron_backup.log' % MEDIA_ROOT, 'a').write('%s\n%s\n' % (ts, err))
            if IS_SLACK: send_notify_slack(SLACK['ADMIN_NAME'], '', [{"fallback":'ERROR', "mrkdwn_in": ["text"], "color":"danger", "text":'*`ERROR`*: *%s* @ _%s_\n>```%s```\n' % (' '.join(sys.argv), time.ctime(), err)}])
            flag = True
        else:
            self.stdout.write("    \033[92mSUCCESS\033[0m: \033[94mstatic\033[0m files synced.")
        self.stdout.write("Time elapsed: %.1f s." % (time.time() - t))

        t = time.time()
        self.stdout.write("#3: Backing up apache2 settings...")
        try:
            subprocess.check_call('cp -r /etc/apache2 %s/backup' % MEDIA_ROOT, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            subprocess.check_call('cd %s/backup && tar zcf backup_apache.tgz apache2/' % MEDIA_ROOT, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            subprocess.check_call('rm -rf %s/backup/apache2' % MEDIA_ROOT, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError:
            self.stdout.write("    \033[41mERROR\033[0m: Failed to archive \033[94mapache2\033[0m settings.")
            err = traceback.format_exc()
            ts = '%s\t\t%s\n' % (time.ctime(), ' '.join(sys.argv))
            open('%s/cache/log_alert_admin.log' % MEDIA_ROOT, 'a').write(ts)
            open('%s/cache/log_cron_backup.log' % MEDIA_ROOT, 'a').write('%s\n%s\n' % (ts, err))
            if IS_SLACK: send_notify_slack(SLACK['ADMIN_NAME'], '', [{"fallback":'ERROR', "mrkdwn_in": ["text"], "color":"danger", "text":'*`ERROR`*: *%s* @ _%s_\n>```%s```\n' % (' '.join(sys.argv), time.ctime(), err)}])
            flag = True
        else:
            self.stdout.write("    \033[92mSUCCESS\033[0m: \033[94mapache2\033[0m settings saved.")
        self.stdout.write("Time elapsed: %.1f s." % (time.time() - t))

        t = time.time()
        self.stdout.write("#4: Backing up config settings...")
        try:
            subprocess.check_call('cd %s && tar zcf backup/backup_config.tgz config/' % MEDIA_ROOT, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError:
            self.stdout.write("    \033[41mERROR\033[0m: Failed to archive \033[94mconfig\033[0m settings.")
            err = traceback.format_exc()
            ts = '%s\t\t%s\n' % (time.ctime(), ' '.join(sys.argv))
            open('%s/cache/log_alert_admin.log' % MEDIA_ROOT, 'a').write(ts)
            open('%s/cache/log_cron_backup.log' % MEDIA_ROOT, 'a').write('%s\n%s\n' % (ts, err))
            if IS_SLACK: send_notify_slack(SLACK['ADMIN_NAME'], '', [{"fallback":'ERROR', "mrkdwn_in": ["text"], "color":"danger", "text":'*`ERROR`*: *%s* @ _%s_\n>```%s```\n' % (' '.join(sys.argv), time.ctime(), err)}])
            flag = True
        else:
            self.stdout.write("    \033[92mSUCCESS\033[0m: \033[94mconfig\033[0m settings saved.")
        self.stdout.write("Time elapsed: %.1f s.\n" % (time.time() - t))

        if flag:
            self.stdout.write("Finished with errors!")
            self.stdout.write("Time elapsed: %.1f s." % (time.time() - t0))
            sys.exit(1)
        else:
            if DEBUG:
                self.stdout.write("\033[94m Backed up locally. \033[0m")
            else:
                (t_cron, d_cron, t_now) = get_date_time('backup')
                local_list = subprocess.Popen('ls -gh %s/backup/*.*gz' % MEDIA_ROOT, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].strip().split()
                html = 'File\t\t\t\tTime\t\t\t\tSize\n\n'
                for i in range(0, len(local_list), 8):
                    html += '%s\t\t%s %s, %s\t\t%s\n' % (local_list[i+7], local_list[i+4], local_list[i+5], local_list[i+6], local_list[i+3])

                if IS_SLACK: 
                    send_notify_slack(SLACK['ADMIN_NAME'], '', [{"fallback":'SUCCESS', "mrkdwn_in": ["text"], "color":"good", "text":'*SUCCESS*: Scheduled weekly *backup* finished @ _%s_\n' % time.ctime()}])
                    send_notify_slack(SLACK['ADMIN_NAME'], '>```%s```\n' % html, '')
                else:
                    send_notify_emails('[System] {%s} Weekly Backup Notice' % env('SSL_HOST'), 'This is an automatic email notification for the success of scheduled weekly backup of the DasLab Website database and static contents.\n\nThe crontab job is scheduled at %s (UTC) on every %sday.\n\nThe last system backup was performed at %s (PDT).\n\n%s\n\nDasLab Website Admin\n' % (t_cron, d_cron, t_now, html))
                    self.stdout.write("Admin email (Weekly Backup Notice) sent.")
            get_backup_stat()
            self.stdout.write("Admin Backup Statistics refreshed.")

            self.stdout.write("All done successfully!")
            self.stdout.write("Time elapsed: %.1f s." % (time.time() - t0))
            