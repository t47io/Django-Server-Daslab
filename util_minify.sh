sudo rm media/js/admin/min/*.min.js
java -jar ../yuicompressor.jar -o '.js$:.min.js' media/js/admin/*.js
mv media/js/admin/*.min.js media/js/admin/min/

sudo rm media/js/group/min/*.min.js
java -jar ../yuicompressor.jar -o '.js$:.min.js' media/js/group/*.js
mv media/js/group/*.min.js media/js/group/min/

sudo rm media/js/suit/min/*.min.js
java -jar ../yuicompressor.jar -o '.js$:.min.js' media/js/suit/*.js
mv media/js/suit/*.min.js media/js/suit/min/

sudo rm media/css/min/*.min.css
java -jar ../yuicompressor.jar -o '.css$:.min.css' media/css/*.css
rm media/css/*.min.min.css
mv media/css/*.min.css media/css/min/
mv media/css/min/bootstrap.min.css media/css/
mv media/css/min/fullcalendar.min.css media/css/


cat media/js/group/min/menu.min.js media/js/group/min/email.min.js > media/js/group/min/menu.js
rm media/js/group/min/menu.min.js media/js/group/min/email.min.js
mv media/js/group/min/menu.js media/js/group/min/menu.min.js

cat media/js/group/min/home.min.js media/js/group/min/clock.min.js > media/js/group/min/home.js
rm media/js/group/min/home.min.js media/js/group/min/clock.min.js
mv media/js/group/min/home.js media/js/group/min/home.min.js

cat media/js/suit/min/core.min.js media/js/suit/min/RelatedObjectLookups.min.js media/js/suit/min/jquery.init.min.js media/js/suit/min/actions.min.js media/js/suit/min/jquery.formset.min.js media/js/suit/min/DateTimeShortcuts.min.js > media/js/suit/min/core.js
rm media/js/suit/min/core.min.js media/js/suit/min/RelatedObjectLookups.min.js media/js/suit/min/jquery.init.min.js media/js/suit/min/actions.min.js media/js/suit/min/jquery.formset.min.js media/js/suit/min/DateTimeShortcuts.min.js
mv media/js/suit/min/core.js media/js/suit/min/core.min.js

cat media/js/admin/min/_suit.min.js media/js/admin/min/table.min.js media/js/admin/min/clock.min.js media/js/admin/min/menu.min.js > media/js/admin/min/menu.js
rm media/js/admin/min/_suit.min.js media/js/admin/min/table.min.js media/js/admin/min/clock.min.js media/js/admin/min/menu.min.js
mv media/js/admin/min/menu.js media/js/admin/min/menu.min.js

cat media/css/min/theme.min.css media/css/min/palette.min.css > media/css/min/theme.css
rm media/css/min/theme.min.css media/css/min/palette.min.css
mv media/css/min/theme.css media/css/min/theme.min.css
