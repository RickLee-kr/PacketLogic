#!/bin/bash

PATTERN=alert-email
FROM_PATTERN=site_name

RC=/opt/pang/mgmt/config/cluster_conf.xml


MAILTO=`grep $PATTERN $RC | grep -v \#  | cut -f2 -d\> | cut -f1 -d\<`
MAILFROM=`grep $FROM_PATTERN $RC | grep -v \#  | cut -f2 -d\> | cut -f1 -d\<`
rm 1 2>/dev/null

if [ A$MAILTO == A"" ];
then
      exit 1;
fi
echo ${MAILFROM} > 1

EXPR=`grep -E " |-" 1`
more_spaces=$EXPR

while [ -n "$more_spaces" ] 
do
    #echo "##########################"
    #echo "before"
    #cat 1      
    sed --in-place -e 's/-/_/'  --in-place  -e 's/ /_/' 1
    more_spaces=`grep -E " |-" 1`
    #echo "after"           
    #cat 1                      
done                        
# echo "string is null"      

MAILFROM=`cat 1`            
#echo $MAILFROM             


while read LOGLINE          
do 
  echo ${LOGLINE} | /usr/bin/mail -s 'UltraBand 5000 Alert' -r $MAILFROM ${MAILTO}
done   
