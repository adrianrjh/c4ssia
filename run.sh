#!/bin/bash
set -e

mypgid=`ps -o pgid $$ | tail -1 | sed 's/ //g'`
echo "started mypgid: ${mypgid}"
# setup ros2 environment
trap "kill -9 -$mypgid; exit"  INT
#cd /home/adrian/ws/wave/cassia/apps/ && wave run login  &
#P1=$!
#sleep 1
#cd /home/adrian/ws/wave/cassia/apps/ && wave run signin  &
#P2=$!
#sleep 1
#cd /home/adrian/ws/wave/cassia/apps/ && wave run home  &
#P3=$!
#sleep 1
#cd /home/adrian/ws/wave/cassia/apps/ && wave run users  &
#P4=$!
#sleep 1
#cd /home/adrian/ws/wave/cassia/apps/settings && wave run mydevices  &
#P6=$!
#sleep 1
#cd /home/adrian/ws/wave/cassia/apps/settings && wave run home_settings  &
#P7=$!
#sleep 1
#cd /home/adrian/ws/wave/cassia/apps/settings && wave run devices  &
#P8=$!
#sleep 1
#cd /home/adrian/ws/wave/cassia/apps/settings && wave run connections &
#P9=$!
#sleep 1
#cd /home/adrian/ws/wave/cassia/apps/settings && wave run myprs &
#P10=$!
#sleep 1
#cd /home/adrian/ws/wave/cassia/apps/settings && wave run mytickets &
#P11=$!
#sleep 1
#cd /home/adrian/ws/wave/cassia/apps/ && wave run rtm &
#P12=$!
#sleep 1
#cd /home/adrian/ws/wave/cassia/apps/ && wave run maps &
#P13=$!
#sleep 1
#cd /home/adrian/ws/wave/cassia/apps/ && wave run a-vsty &
#P14=$!
#sleep 1
#cd /home/adrian/ws/wave/cassia/apps/prs/ && wave run home_prs &
#P15=$!
#sleep 1
#cd /home/adrian/ws/wave/cassia/apps/prs/ && wave run prs &
#P16=$!
#sleep 1
#cd /home/adrian/ws/wave/cassia/apps/prs/ && wave run addMats &
#P17=$!
#sleep 1
#cd /home/adrian/ws/wave/cassia/apps/prs/ && wave run addDevs &
#P18=$!
#sleep 1
#cd /home/adrian/ws/wave/cassia/apps/pap && wave run home_pap &
#P19=$!
#sleep 1
#cd /home/adrian/ws/wave/cassia/apps/pap && wave run pap_projects &
#P20=$!
#sleep 1
#cd /home/adrian/ws/wave/cassia/apps/pap && wave run pap_obra &
#P21=$!
#sleep 1
#cd /home/adrian/ws/wave/cassia/apps/pap && wave run pap_tickets &
#P22=$!
#sleep 1
#cd /home/adrian/ws/wave/cassia/apps/pap && wave run pap_manage &
#P23=$!
#sleep 1
#cd /home/adrian/ws/wave/cassia/apps/pap && wave run pap_converter &
#P24=$!
#sleep 1
#cd /home/adrian/ws/wave/cassia/apps/pap && wave run pap_poles &
#P25=$!
#sleep 1
#cd /home/adrian/ws/wave/cassia/apps/pap && wave run pap_density &
#P26=$!
#sleep 1
#cd /home/adrian/ws/wave/cassia/apps/pap && wave run pap_monitor &
#P27=$!
#sleep 1
#cd /home/adrian/ws/wave/cassia/apps/inventory && wave run home_sims &
#P28=$!
#sleep 1
#cd /home/adrian/ws/wave/cassia/apps/inventory && wave run sims_cotejo &
#P29=$!
#sleep 1
#cd /home/adrian/ws/wave/cassia/apps/inventory && wave run sims_recepcion &
#P30=$!
#sleep 1
#cd /home/adrian/ws/wave/cassia/apps/inventory && wave run sims_asignacion &
#P31=$!
#sleep 1
#cd /home/adrian/ws/wave/cassia/apps/inventory && wave run sims_devolucion &
#P32=$!
#sleep 1
#cd /home/adrian/ws/wave/cassia/apps/inventory && wave run sims_scrap &
#P33=$!
#sleep 1
#cd /home/adrian/ws/wave/cassia/apps/inventory && wave run sims_stocksEN &
#P34=$!
#sleep 1
#cd /home/adrian/ws/wave/cassia/apps/inventory && wave run sims_stocksEU &
#P35=$!
#sleep 1
#cd /home/adrian/ws/wave/cassia/apps/inventory && wave run sims_stocksMC &
#P36=$!
#sleep 1
#cd /home/adrian/ws/wave/cassia/apps/inventory && wave run sims_altaEU &
#P37=$!
#sleep 1
#cd /home/adrian/ws/wave/cassia/apps/inventory && wave run sims_altaEN &
#P38=$!
#sleep 1
#cd /home/adrian/ws/wave/cassia/apps/inventory && wave run sims_altaMC &
#P39=$!
#sleep 1
#cd /home/adrian/ws/wave/cassia/apps/tickets && wave run home_tickets &
#P40=$!
#sleep 1
#cd /home/adrian/ws/wave/cassia/apps/tickets && wave run tickets_add &
#P41=$!
#sleep 1
#cd /home/adrian/ws/wave/cassia/apps/tickets && wave run tickets_active &
#P42=$!
#sleep 1
#cd /home/adrian/ws/wave/cassia/apps/tickets && wave run tickets_fiber &
#P43=$!
#sleep 1
#cd /home/adrian/ws/wave/cassia/apps/tickets && wave run tickets_wireless &
#P44=$!
#sleep 1
#cd /home/adrian/ws/wave/cassia/apps/tickets && wave run tickets_public &
#P45=$!
#sleep 1
#cd /home/adrian/ws/wave/cassia/apps/tickets && wave run tickets_done &
#P46=$!
#sleep 1
#cd /home/adrian/ws/wave/cassia/apps/tickets && wave run tickets_exception &
#P47=$!
#sleep 1
#cd /home/adrian/ws/wave/cassia/apps/iis && wave run home_iis &
#P48=$!
#sleep 1
cd /home/adrian/ws/wave/cassia/apps/iis && wave run iis_create &
P49=$!
sleep 1
cd /home/adrian/ws/wave/cassia/apps/iis && wave run iis_dashboard &
P50=$!
sleep 1
cd /home/adrian/ws/wave/cassia/apps/iis && wave run iis_workers &
P51=$!
sleep 1
wait $P51 $P50 $P49 #$P4 $P5 $P6 $P7 $P8 $P9 $P10 $P11 $P12 $P13 $P14 $P15 $P16 $P17 $P18 $P19 $P20 $P21 $P22 $P23 $P24 $P25 $P26 $P27 $P28 $P29 $P30 $P31 $P32 $P33 $P34 $P35 $P36 $P37 $P38 $P39 $P40 $P41 $P42 $P43 $P44 $P45 $P46 $P47 $P48 $P49 $P50
exec "$@"