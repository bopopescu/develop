#!/bin/bash
LOOKDIR='/home/goland/zzz/POS'
#LOOKDIR=$1
DIRLIST=`ls $LOOKDIR`
DIR=$DIRLIST
ip='10.10.2.64'
username='goland'
password='123456'

#for i in `seq 0 $((${#DIR[@]}-1))`
#do
#expect -c " 
#spawn ssh $username@$ip "cd ${DIR[i]};git pull;cd .."
#       expect {
  #            \"*yes/no*\" {send \"yes\r\"; exp_continue} 
 #             \"*password*\" {send \"$password\r\"; exp_continue} 
   #           }
#"
#done
expect -c "
spawn ssh $username@$ip "cd /tmp;ls"
    expect {
 #             \"*yes/no*\" {send \"yes\r\"; exp_continue} 
              \"*password*\" {send \"$password\r\"; exp_continue} 
              }
"
    
