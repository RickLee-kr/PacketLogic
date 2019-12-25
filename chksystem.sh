#!/bin/sh
clear
export LANG=C
LOGPATH="/tmp"
HOST=`/bin/hostname`
TODAY=`/bin/date +%Y%m%d`
DAY=`/bin/date +%d`

memorysinfo()
{
	echo "###################################################################" 
        echo "# 1. System Memory-Info                                            " 
        echo "###################################################################" 
        /bin/cat /proc/meminfo 
        echo "####################################################################" 
        memusage=`top -n 1 -b | grep "Mem"`
        MAXMEM=`echo $memusage | cut -d" " -f2 | awk '{print substr($0,1,length($0)-1)}'`
        USEDMEM=`echo $memusage | cut -d" " -f4 | awk '{print substr($0,1,length($0)-1)}'`
        USEDMEM1=`expr $USEDMEM \* 100`
        PERCENTAGE=`expr $USEDMEM1 / $MAXMEM`%
        echo "Total Memory: $MAXMEM KB, Used Memory: $USEDMEM KB, Used Memory Percentage: $PERCENTAGE" 
        echo "####################################################################" 
        echo "#SWAP Memory check and disk" 
        echo "####################################################################"
        /sbin/swapon -s
        echo "####################################################################" 

return 0
exit 0
}

memoryinfo()
{

  echo -e "\n"
        echo -e "\033[1;4;5mprocessing\033[1;4;0m"

        sleep 2
        echo -e "\n"
        echo " checked memory info OK "
        echo -ne " choice reporting method .. [\033[1;4;31mS\033[1;4;0mcreen/\033[1;4;31mF\033[1;4;0mile/\033[1;4;31mQ\033[1;4;0muit] "
        read choice
        case $choice in

                S|s )
                        echo -e "\n\n"
                        memorysinfo ;;

                F|f )
                        echo -e "\n"
        		tmp_file=$LOGPATH/$TODAY.memory.system.log
                        echo " write .. $tmp_file " 
        		echo -n > $tmp_file
        		echo "###################################################################" >> $tmp_file
       		        echo "# 1. System Memory-Info                                            " >> $tmp_file
        		echo "###################################################################" >> $tmp_file
        		/bin/cat /proc/meminfo  >> $tmp_file
        		echo "####################################################################" >> $tmp_file
        		memusage=`top -n 1 -b | grep "Mem"`
        		MAXMEM=`echo $memusage | cut -d" " -f2 | awk '{print substr($0,1,length($0)-1)}'`
        		USEDMEM=`echo $memusage | cut -d" " -f4 | awk '{print substr($0,1,length($0)-1)}'`
        		USEDMEM1=`expr $USEDMEM \* 100`
        		PERCENTAGE=`expr $USEDMEM1 / $MAXMEM`%
        		echo "Total Memory: $MAXMEM KB, Used Memory: $USEDMEM KB, Used Memory Percentage: $PERCENTAGE" >> $tmp_file
        		echo "####################################################################" >> $tmp_file
        		echo "#SWAP Memory check and disk" >> $tmp_file
        		echo "####################################################################" >> $tmp_file
        		/sbin/swapon -s >> $tmp_file
        		echo "####################################################################" >> $tmp_file ;;

                Q|q )
                        exit 0 ;;
        esac

        echo -e "\n"
        echo "------------- end report ------------ "
        echo -e "\n"
        echo -ne " return main menu ? [\033[1;4;31mR\033[1;4;0meturn/\033[1;4;31mQ\033[1;4;0muit] "
        read choice
        case $choice in

                Q|q )
                        exit 0 ;;

                R|r )
                        clear
                        return 0 ;;
        esac

}


diskscheck()
{
	echo "##################################################################" 
        echo "# 2. Disk Check and Mount info                                    "
        echo "##################################################################"
        /sbin/fdisk -l 
        echo "------------------------------------------------------------------" 
        /bin/cat /proc/partitions 
        echo "------------------------------------------------------------------" 
        /sbin/pvs 
        echo "------------------------------------------------------------------" 
        /sbin/vgs 
        echo "-----------------------------------------------------------------"
        /sbin/lvs 
        echo "-----------------------------------------------------------------"
        /sbin/lvs -v 
        echo "-----------------------------------------------------------------"
        /sbin/lvs -v --segments
        echo "-----------------------------------------------------------------"
        echo "/sbin/multipath -ll" 
        echo "-----------------------------------------------------------------" 
        echo "/bin/cat /etc/multipath.conf" 
        echo "####################################################################" 
        /bin/df -h     
        echo "-----------------------------------------------------------------" 
        /bin/df -i      
        echo "-----------------------------------------------------------------"
        /bin/mount     
        echo "####################################################################"


return 0

}

diskcheck()
{
	echo -e "\n"
        echo -e "\033[1;4;5mprocessing\033[1;4;0m"
        sleep 2

        echo -e "\n"
        echo " checked disk OK "
        echo -ne " choice reporting method .. [\033[1;4;31mS\033[1;4;0mcreen/\033[1;4;31mF\033[1;4;0mile/\033[1;4;31mQ\033[1;4;0muit] "
        read choice
        case $choice in

                S|s )
                        echo -e "\n\n"
                        diskscheck ;;
                F|f )
                        echo -e "\n"
			tmp_file=$LOGPATH/$TODAY.disk.system.log
                        echo " write .. $tmp_file " 
			# clear file
			echo -n > $tmp_file
			echo "##################################################################" >> $tmp_file
			echo "# 2. Disk Check and Mount info                                    " >> $tmp_file
			echo "##################################################################" >> $tmp_file
			/sbin/fdisk -l >> $tmp_file
			echo "------------------------------------------------------------------" >> $tmp_file
			/bin/cat /proc/partitions >> $tmp_file
			echo "------------------------------------------------------------------" >> $tmp_file
			/sbin/pvs >> $tmp_file
			echo "------------------------------------------------------------------" >> $tmp_file
			/sbin/vgs >> $tmp_file
			echo "-----------------------------------------------------------------" >> $tmp_file
			/sbin/lvs >> $tmp_file
			echo "-----------------------------------------------------------------" >> $tmp_file
			/sbin/lvs -v >> $tmp_file
			echo "-----------------------------------------------------------------" >> $tmp_file
			/sbin/lvs -v --segments >> $tmp_file
			echo "-----------------------------------------------------------------" >> $tmp_file
			/sbin/multipath -ll >> $tmp_file
			echo "-----------------------------------------------------------------" >> $tmp_file
			/bin/cat /etc/multipath.conf >> $tmp_file
			echo "####################################################################" >> $tmp_file
			/bin/df -h      >> $tmp_file
			echo "-----------------------------------------------------------------" >> $tmp_file
			/bin/df -i      >> $tmp_file
			echo "-----------------------------------------------------------------" >> $tmp_file
			/bin/mount      >> $tmp_file
			echo "####################################################################" >> $tmp_file ;;


                Q|q )
                        exit 0 ;;
        esac

        echo -e "\n"
        echo "------------- end report ------------ "
        echo -e "\n"
        echo -ne " return main menu ? [\033[1;4;31mR\033[1;4;0meturn/\033[1;4;31mQ\033[1;4;0muit] "
        read choice
        case $choice in

                R|r )
                        clear
                        return 0 ;;

        esac

}

networkscheck() 
{

	echo "##################################################################"
	echo "# 3. Network Check & Status                                         " 
	echo "##################################################################"
	/sbin/ifconfig -a 
	echo "#################################################################" 
	/sbin/ifconfig -a | grep addr
	echo "################################################################"
	/sbin/ip addr list
	echo "################################################################"
	cat /proc/net/bonding/bond0
	cat /proc/net/bonding/bond1
	cat /proc/net/bonding/bond2 
	cat /proc/net/bonding/bond3
	cat /proc/net/bonding/bond4 
	echo "###############################################################" 
	/sbin/ethtool eth0
	/sbin/ethtool eth1 
	/sbin/ethtool eth2 
	/sbin/ethtool eth3 
	/sbin/ethtool eth4 
	/sbin/ethtool eth5
	/sbin/ethtool eth6 
	/sbin/ethtool eth7 
	/sbin/ethtool eth8 
	/sbin/ethtool eth9 
	/sbin/ethtool eth10 
	echo "#############################################################" 
	/bin/cat /etc/sysconfig/network 
	/bin/cat /etc/sysconfig/network-scripts/ifcfg-*
	echo "------------------------------------------------------------" 
	echo " Network connectaion status" 
	echo "------------------------------------------------------------" 
	/bin/netstat -natpeu | grep ESTABLISHED 
	echo "------------------------------------------------------------" 
	/bin/netstat -natpeu | grep LISTEN      
	echo "------------------------------------------------------------" 
}


networkcheck()
{
        echo -e "\n"
        echo -e "\033[1;4;5mprocessing\033[1;4;0m"
        sleep 3

        echo -e "\n"
        echo " checked network info OK "
        echo -ne " choice reporting method .. [\033[1;4;31mS\033[1;4;0mcreen/\033[1;4;31mF\033[1;4;0mile/\033[1;4;31mQ\033[1;4;0muit] "
        read choice
        case $choice in 

                S|s ) 
                        echo -e "\n\n"
                        networkscheck ;;

                F|f ) 
			tmp_file=$LOGPATH/$TODAY.network.system.log
                        echo -e "\n"
                        echo " write .. $tmp_file " 
			echo -n > $tmp_file
			echo "##################################################################" >> $tmp_file
			echo "# 3. Network Check & Status                                       " >> $tmp_file
			echo "##################################################################" >> $tmp_file
			/sbin/ifconfig -a >> $tmp_file
			echo "#################################################################" >> $tmp_file
			/sbin/ifconfig -a | grep addr  >> $tmp_file
			echo "################################################################" >> $tmp_file
			/sbin/ip addr list  >> $tmp_file
			echo "################################################################" >> $tmp_file
			cat /proc/net/bonding/bond0 >> $tmp_file
			cat /proc/net/bonding/bond1 >> $tmp_file
			cat /proc/net/bonding/bond2 >> $tmp_file
			cat /proc/net/bonding/bond3 >> $tmp_file
			cat /proc/net/bonding/bond4 >> $tmp_file
			echo "###############################################################" >> $tmp_file
			/sbin/ethtool eth0 >> $tmp_file
			/sbin/ethtool eth1 >> $tmp_file
			/sbin/ethtool eth2 >> $tmp_file
			/sbin/ethtool eth3 >> $tmp_file
			/sbin/ethtool eth4 >> $tmp_file
			/sbin/ethtool eth5 >> $tmp_file
			/sbin/ethtool eth6 >> $tmp_file
			/sbin/ethtool eth7 >> $tmp_file
			/sbin/ethtool eth8 >> $tmp_file
			/sbin/ethtool eth9 >> $tmp_file
			/sbin/ethtool eth10 >> $tmp_file
			echo "#############################################################" >> $tmp_file
			/bin/cat /etc/sysconfig/network >> $tmp_file
			/bin/cat /etc/sysconfig/network-scripts/ifcfg-* >> $tmp_file
			echo "------------------------------------------------------------" >> $tmp_file
			echo " Network connectaion status" >>$tmp_file
			echo "------------------------------------------------------------" >> $tmp_file
			/bin/netstat -natpeu | grep ESTABLISHED >> $tmp_file
			echo "------------------------------------------------------------" >> $tmp_file
			/bin/netstat -natpeu | grep LISTEN      >> $tmp_file
			echo "------------------------------------------------------------" >> $tmp_file ;;

                Q|q ) 
                        exit 0 ;;
        esac

        echo -e "\n"
        echo "------------- end report ------------ "
        echo -e "\n"
        echo -ne " return main menu ? [\033[1;4;31mR\033[1;4;0meturn/\033[1;4;31mQ\033[1;4;0muit] "
        read choice
        case $choice in

                Q|q )
                        exit 0 ;;

                R|r )
                        clear
                        return 0 ;;

        esac

}


cpusinfo() 
{
	echo "############################################################"
        echo "# 4. CPU Model              "                                   
        echo "############################################################" 
        /bin/cat /proc/cpuinfo | grep name 
        echo "############################################################" 
        echo "############################################################"
        echo "#CPU load System(%), User(%)" 
        echo "############################################################" 
        top -b -n 1 | sed -ne '/Cpu/ s/.* \([0-9]*\.[0-9]*\)%us.* \([0-9]*\.[0-9]*\)%sy.*/User: \1%, System: \2%/p' 
        echo "############################################################" 

return 0 
}

cpuinfo()
{

  echo -e "\n"
        echo -e "\033[1;4;5mprocessing\033[1;4;0m"
        sleep 2

        echo -e "\n"
        echo " checked cpu info OK "
        echo -ne " choice reporting method .. [\033[1;4;31mS\033[1;4;0mcreen/\033[1;4;31mF\033[1;4;0mile/\033[1;4;31mQ\033[1;4;0muit] "
        read choice
        case $choice in

                S|s )
                        echo -e "\n\n"
                        cpusinfo ;;

                F|f )
                        echo -e "\n"
			tmp_file=$LOGPATH/$TODAY.cpu.system.log
                        echo " write .. $tmp_file " 
			echo -n > $tmp_file
			echo "############################################################" >> $tmp_file
			echo "# 4. CPU Model              "                                   >> $tmp_file
			echo "############################################################" >> $tmp_file
			/bin/cat /proc/cpuinfo | grep name >> $tmp_file
			echo "############################################################" >> $tmp_file
			echo "############################################################" >> $tmp_file
			echo "#CPU load System(%), User(%)" >> $tmp_file
			echo "############################################################" >> $tmp_file
			top -b -n 1 | sed -ne '/Cpu/ s/.* \([0-9]*\.[0-9]*\)%us.* \([0-9]*\.[0-9]*\)%sy.*/User: \1%, System: \2%/p' >> $tmp_file
			echo "############################################################" >> $tmp_file ;;

                Q|q )
                        exit 0 ;;
        esac

        echo -e "\n"
        echo "------------- end report ------------ "
        echo -e "\n"
        echo -ne " return main menu ? [\033[1;4;31mR\033[1;4;0meturn/\033[1;4;31mQ\033[1;4;0muit] "
        read choice
        case $choice in

                Q|q )
                        exit 0 ;;

                R|r )
                        clear
                        return 0 ;;

        esac


}

sysloadsavg()
{

	echo "##################################################################"
        echo "# 5. System Load Avg" >> $tmp_file
        echo "##################################################################"
        loadavg1=`uptime | awk '{print $10}'`
        loadavg2=`echo $loadavg1|awk -F \. '{print $1}'`
        if [ "$loadavg2" -ge "2" ]; then
                echo "Busy - Load Average $loadavg1 ($loadavg2) "
                top -bn 1
                echo "##################################################################"
                else
                echo "#Normal - Load Average $loadavg1 ($loadavg2) "
                echo "##################################################################"
        fi

return 0

}

sysloadavg()
{
       
        echo -e "\n"
        echo -e "\033[1;4;5mprocessing\033[1;4;0m"
        sleep 3

        echo -e "\n"
        echo " checked sysloadavg OK "
        echo -ne " choice reporting method .. [\033[1;4;31mS\033[1;4;0mcreen/\033[1;4;31mF\033[1;4;0mile/\033[1;4;31mQ\033[1;4;0muit] "
        read choice
        case $choice in

                S|s )
                        echo -e "\n\n"
                        sysloadsavg ;;

                F|f )
                        echo -e "\n"
			tmp_file=$LOGPATH/$TODAY.sysloadavg.system.log
                        echo " write .. $tmp_file " 
			echo -n > $tmp_file

			echo "##################################################################" >> $tmp_file
			echo "# 5. System Load Avg" >> $tmp_file
			echo "##################################################################" >> $tmp_file
			loadavg1=`uptime | awk '{print $10}'`
			loadavg2=`echo $loadavg1|awk -F \. '{print $1}'`
			if [ "$loadavg2" -ge "2" ]; then
				echo "Busy - Load Average $loadavg1 ($loadavg2) " >> $tmp_file
				top -bn 1 >> $tmp_file
				echo "##################################################################" >> $tmp_file
				else
				echo "#Normal - Load Average $loadavg1 ($loadavg2) " >> $tmp_file
				echo "##################################################################" >> $tmp_file 
			fi ;;

                Q|q )
                        exit 0 ;;
        esac

        echo -e "\n"
        echo "------------- end report ------------ "
        echo -e "\n"
        echo -ne " return main menu ? [\033[1;4;31mR\033[1;4;0meturn/\033[1;4;31mQ\033[1;4;0muit] "
        read choice
        case $choice in

                Q|q )
                        exit 0 ;;

                R|r )
                        clear
                        return 0 ;;

        esac
}



kdumpscheck()
{
        echo "##################################################################"
        echo "# 6. Kdump Check"
        echo "##################################################################"
        /sbin/chkconfig --list | grep kdump
        echo "-----------------------------------------------------------------"
        /etc/init.d/kdump status
        echo "-----------------------------------------------------------------"

return 0 

}


kdumpcheck()
{
        echo -e "\n"
        echo -e "\033[1;4;5mprocessing\033[1;4;0m"
        sleep 2

        echo -e "\n"
        echo " checked dump OK "
        echo -ne " choice reporting method .. [\033[1;4;31mS\033[1;4;0mcreen/\033[1;4;31mF\033[1;4;0mile/\033[1;4;31mQ\033[1;4;0muit] "
        read choice
        case $choice in

                S|s )
                        echo -e "\n\n"
                        kdumpscheck ;;

                F|f )
                        echo -e "\n"
			tmp_file=$LOGPATH/$TODAY.dump.system.log
                        echo " write .. $tmp_file " 
			echo -n > $tmp_file
			echo "##################################################################" >> $tmp_file
			echo "# 6. Kdump Check" >> $tmp_file
			echo "##################################################################" >> $tmp_file
			/sbin/chkconfig --list | grep kdump >> $tmp_file
			echo "-----------------------------------------------------------------" >> $tmp_file
			/etc/init.d/kdump status >> $tmp_file
			echo "-----------------------------------------------------------------" >> $tmp_file ;; 
               Q|q) 
			exit 0 ;;
	 	esac
			 echo -e "\n"
			 echo "------------- end report ------------ "
			 echo -e "\n"
			 echo -ne " return main menu ? [\033[1;4;31mR\033[1;4;0meturn/\033[1;4;31mQ\033[1;4;0muit] "
		        read choice
			case $choice in

				Q|q )
					exit 0 ;;

				R|r )
					clear
					return 0 ;;

				Q|q )
					exit 0 ;;
		esac	
}


checksfilesystem()
{
        echo "##################################################################" 
        echo "# 7. Check Filsystem status " 
        echo "##################################################################"
        echo " #  8. tune2fs -l                                                   " 
        for i in $(df -h | grep /dev | awk {'print $1'} | grep -v tmpfs) ;
        do echo $i; tune2fs -l $i; done
        echo "##################################################################"
return 0 

}

checkfilesystem()
{
	 echo -e "\n"
        echo -e "\033[1;4;5mprocessing\033[1;4;0m"
        sleep 2

        echo -e "\n"
        echo " checked dump OK "
        echo -ne " choice reporting method .. [\033[1;4;31mS\033[1;4;0mcreen/\033[1;4;31mF\033[1;4;0mile/\033[1;4;31mQ\033[1;4;0muit] "
        read choice
        case $choice in

                S|s )
                        echo -e "\n\n"
                        checksfilesystem ;;

                F|f )
                        echo -e "\n"
			tmp_file=$LOGPATH/$TODAY.filesystem.system.log
                        echo " write .. $tmp_file "  
			# clear file
			echo -n > $tmp_file
			echo "##################################################################" >> $tmp_file
			echo "# 7. Check Filsystem status " >> $tmp_file
			echo "##################################################################" >> $tmp_file
			echo " #  8. tune2fs -l                                                   " >> $tmp_file
			for i in $(df -h | grep /dev | awk {'print $1'} | grep -v tmpfs) ;
			do echo $i; tune2fs -l $i; done >> $tmp_file
			echo "##################################################################" >> $tmp_file ;;

                Q|q )
                        exit 0 ;;
        esac

        echo -e "\n"
        echo "------------- end report ------------ "
        echo -e "\n"
        echo -ne " return main menu ? [\033[1;4;31mR\033[1;4;0meturn/\033[1;4;31mQ\033[1;4;0muit] "
        read choice
        case $choice in

                Q|q )
                        exit 0 ;;

                R|r )
                        clear
                        return 0 ;;
esac

}



spcheckdeamon()
{

	echo "##################################################################" 
        echo "# 8. Check System Deamon & Process"
        echo "##################################################################"
        /sbin/chkconfig --list | grep 3:on
        echo "-----------------------------------------------------------------" 
        /usr/bin/pstree -a -n -p 
        echo "##################################################################"
         
return 0 
}

checksysdeamon()
{
        echo -e "\n"
        echo -e "\033[1;4;5mprocessing\033[1;4;0m"
        sleep 2

        echo -e "\n"
        echo " checked dump OK "
        echo -ne " choice reporting method .. [\033[1;4;31mS\033[1;4;0mcreen/\033[1;4;31mF\033[1;4;0mile/\033[1;4;31mQ\033[1;4;0muit] "
        read choice
        case $choice in

                S|s )
                        echo -e "\n\n"
                        spcheckdeamon ;;

                F|f )
                        echo -e "\n"
			tmp_file=$LOGPATH/$TODAY.deamon.system.log
                        echo " write .. $tmp_file " 
			echo -n > $tmp_file
			echo "##################################################################" >> $tmp_file
			echo "# 8. Check System Deamon & Process" >> $tmp_file
			echo "##################################################################" >> $tmp_file
			/sbin/chkconfig --list | grep 3:on >> $tmp_file
			echo "-----------------------------------------------------------------" >> $tmp_file
			/usr/bin/pstree -a -n -p  >> $tmp_file
			echo "##################################################################" >> $tmp_file ;;

                Q|q )
                        exit 0 ;;
        	esac

			echo -e "\n"
			echo "------------- end report ------------ "
			echo -e "\n"
			echo -ne " return main menu ? [\033[1;4;31mR\033[1;4;0meturn/\033[1;4;31mQ\033[1;4;0muit] "
			read choice
			case $choice in

                Q|q )
                        exit 0 ;;

                R|r )
                        clear
                        return 0 ;;
esac

}



spchecksystemlog()
{
	echo "##################################################################"
	echo "# 9. Check SystemLog info"
	echo "##################################################################"
	echo "# dmesg Log info"
	echo "##################################################################"
	/bin/dmesg | egrep -i -e error -e warning -e fail
	echo "##################################################################"
	echo "# Messages Log info"
	echo "##################################################################"
	/bin/cat /var/log/messages | egrep -i -e error -e warning -e fail
	echo "##################################################################"
	echo "# Crond Log info"
	echo "##################################################################"
	/bin/cat /var/log/cron | egrep -i -e error -e warning -e fail
	echo "##################################################################"

return 0 
}


checksystemlog()
{

echo -e "\n"
        echo -e "\033[1;4;5mprocessing\033[1;4;0m"
        sleep 2

        echo -e "\n"
        echo " checked Systemlog OK "
        echo -ne " choice reporting method .. [\033[1;4;31mS\033[1;4;0mcreen/\033[1;4;31mF\033[1;4;0mile/\033[1;4;31mQ\033[1;4;0muit] "
        read choice
        case $choice in

                S|s )
                        echo -e "\n\n"
                        spchecksystemlog ;;

                F|f )
                        echo -e "\n"
			tmp_file=$LOGPATH/$TODAY.dmesg.system.log
                        echo " write .. $tmp_file " 
			echo -n > $tmp_file
			echo "##################################################################" >> $tmp_file
			echo "# 9. Check SystemLog info" >> $tmp_file
			echo "##################################################################" >> $tmp_file
			echo "# dmesg Log info" >> $tmp_file
			echo "##################################################################" >> $tmp_file
			/bin/dmesg | egrep -i -e error -e warning -e fail >> $tmp_file
			echo "##################################################################" >> $tmp_file
			echo "# Messages Log info" >> $tmp_file
			echo "##################################################################" >> $tmp_file
			/bin/cat /var/log/messages | egrep -i -e error -e warning -e fail >> $tmp_file
			echo "##################################################################" >> $tmp_file
			echo "# Crond Log info" >> $tmp_file
			echo "##################################################################" >> $tmp_file
			/bin/cat /var/log/crond | egrep -i -e error -e warning -e fail >> $tmp_file
			echo "##################################################################" >> $tmp_file;;

                Q|q )
                        exit 0 ;;
        esac

			echo -e "\n"
			echo "------------- end report ------------ "
			echo -e "\n"
			echo -ne " return main menu ? [\033[1;4;31mR\033[1;4;0meturn/\033[1;4;31mQ\033[1;4;0muit] "
			read choice
			case $choice in

				Q|q )
					exit 0 ;;

				R|r )
					clear
					return 0 ;;
esac 
}


systemfullog() {

# clear file
tmp_file=$LOGPATH/$TODAY.$HOST.system_full.log
echo "###################################################################" >> $tmp_file
echo "# 1. System Memory-Info                                            " >> $tmp_file
echo "###################################################################" >> $tmp_file
/bin/cat /proc/meminfo  >> $tmp_file
echo "####################################################################" >> $tmp_file
memusage=`top -n 1 -b | grep "Mem"`
MAXMEM=`echo $memusage | cut -d" " -f2 | awk '{print substr($0,1,length($0)-1)}'`
USEDMEM=`echo $memusage | cut -d" " -f4 | awk '{print substr($0,1,length($0)-1)}'`
USEDMEM1=`expr $USEDMEM \* 100`
PERCENTAGE=`expr $USEDMEM1 / $MAXMEM`%
echo "Total Memory: $MAXMEM KB, Used Memory: $USEDMEM KB, Used Memory Percentage: $PERCENTAGE" >> $tmp_file
echo "####################################################################" >> $tmp_file
echo "#SWAP Memory check and disk" >> $tmp_file
echo "####################################################################" >> $tmp_file
/sbin/swapon -s >> $tmp_file
echo "####################################################################" >> $tmp_file
echo "									  " >> $tmp_file
echo "									  " >> $tmp_file
echo "##################################################################" >> $tmp_file
echo "# 2. Disk Check and Mount info                                    " >> $tmp_file
echo "##################################################################" >> $tmp_file
/sbin/fdisk -l >> $tmp_file
echo "------------------------------------------------------------------" >> $tmp_file
/bin/cat /proc/partitions >> $tmp_file
echo "------------------------------------------------------------------" >> $tmp_file
/sbin/pvs >> $tmp_file
echo "------------------------------------------------------------------" >> $tmp_file
/sbin/vgs >> $tmp_file
echo "-----------------------------------------------------------------" >> $tmp_file
/sbin/lvs >> $tmp_file
echo "-----------------------------------------------------------------" >> $tmp_file
/sbin/lvs -v >> $tmp_file
echo "-----------------------------------------------------------------" >> $tmp_file
/sbin/lvs -v --segments >> $tmp_file
echo "-----------------------------------------------------------------" >> $tmp_file
/sbin/multipath -ll >> $tmp_file
echo "-----------------------------------------------------------------" >> $tmp_file
/bin/cat /etc/multipath.conf >> $tmp_file
echo "####################################################################" >> $tmp_file
/bin/df -h      >> $tmp_file
echo "-----------------------------------------------------------------" >> $tmp_file
/bin/df -i      >> $tmp_file
echo "-----------------------------------------------------------------" >> $tmp_file
/bin/mount      >> $tmp_file
echo "####################################################################" >> $tmp_file
echo "									  " >> $tmp_file
echo "									  " >> $tmp_file
echo "##################################################################" >> $tmp_file
echo "# 3. Network Check & Status                                         " >> $tmp_file
echo "##################################################################" >> $tmp_file
/sbin/ifconfig -a >> $tmp_file
echo "#################################################################" >> $tmp_file
/sbin/ifconfig -a | grep addr  >> $tmp_file
echo "################################################################" >> $tmp_file
/sbin/ip addr list  >> $tmp_file
echo "################################################################" >> $tmp_file
cat /proc/net/bonding/bond0 >> $tmp_file
cat /proc/net/bonding/bond1 >> $tmp_file
cat /proc/net/bonding/bond2 >> $tmp_file
cat /proc/net/bonding/bond3 >> $tmp_file
cat /proc/net/bonding/bond4 >> $tmp_file
echo "###############################################################" >> $tmp_file
/sbin/ethtool eth0 >> $tmp_file
/sbin/ethtool eth1 >> $tmp_file
/sbin/ethtool eth2 >> $tmp_file
/sbin/ethtool eth3 >> $tmp_file
/sbin/ethtool eth4 >> $tmp_file
/sbin/ethtool eth5 >> $tmp_file
/sbin/ethtool eth6 >> $tmp_file
/sbin/ethtool eth7 >> $tmp_file
/sbin/ethtool eth8 >> $tmp_file
/sbin/ethtool eth9 >> $tmp_file
/sbin/ethtool eth10 >> $tmp_file
echo "#############################################################" >> $tmp_file
/bin/cat /etc/sysconfig/network >> $tmp_file
/bin/cat /etc/sysconfig/network-scripts/ifcfg-* >> $tmp_file
echo "------------------------------------------------------------" >> $tmp_file
echo " Network connectaion status" >>$tmp_file
echo "------------------------------------------------------------" >> $tmp_file
/bin/netstat -natpeu | grep ESTABLISHED >> $tmp_file
echo "------------------------------------------------------------" >> $tmp_file
/bin/netstat -natpeu | grep LISTEN      >> $tmp_file
echo "------------------------------------------------------------" >> $tmp_file
echo "									  " >> $tmp_file
echo "									  " >> $tmp_file
echo "############################################################" >> $tmp_file
echo "# 4. CPU Model              "                                   >> $tmp_file
echo "############################################################" >> $tmp_file
/bin/cat /proc/cpuinfo | grep name >> $tmp_file
echo "############################################################" >> $tmp_file
echo "############################################################" >> $tmp_file
echo "#CPU load System(%), User(%)" >> $tmp_file
echo "############################################################" >> $tmp_file
top -b -n 1 | sed -ne '/Cpu/ s/.* \([0-9]*\.[0-9]*\)%us.* \([0-9]*\.[0-9]*\)%sy.*/User: \1%, System: \2%/p' >> $tmp_file
echo "############################################################" >> $tmp_file
echo "									  " >> $tmp_file
echo "									  " >> $tmp_file
echo "##################################################################" >> $tmp_file
echo "# 5. System Load Avg" >> $tmp_file
echo "##################################################################" >> $tmp_file
loadavg1=`uptime | awk '{print $10}'`
loadavg2=`echo $loadavg1|awk -F \. '{print $1}'`
if [ "$loadavg2" -ge "2" ]; then
        echo "Busy - Load Average $loadavg1 ($loadavg2) " >> $tmp_file
        top -bn 1 >> $tmp_file
        echo "##################################################################" >> $tmp_file
        else
        echo "#Normal - Load Average $loadavg1 ($loadavg2) " >> $tmp_file
        echo "##################################################################" >> $tmp_file
fi
echo "									  " >> $tmp_file
echo "									  " >> $tmp_file
echo "##################################################################" >> $tmp_file
echo "# 6. Kdump Check" >> $tmp_file
echo "##################################################################" >> $tmp_file
/sbin/chkconfig --list | grep kdump >> $tmp_file
echo "-----------------------------------------------------------------" >> $tmp_file
/etc/init.d/kdump status >> $tmp_file
echo "-----------------------------------------------------------------" >> $tmp_file
echo "									  " >> $tmp_file
echo "									  " >> $tmp_file
echo "##################################################################" >> $tmp_file
echo "# 7. Check Filsystem status " >> $tmp_file
echo "##################################################################" >> $tmp_file
echo " #  8. tune2fs -l                                                   " >> $tmp_file
for i in $(df -h | grep /dev | awk {'print $1'} | grep -v tmpfs) ;
do echo $i; tune2fs -l $i; done >> $tmp_file
echo "##################################################################" >> $tmp_file
echo "									  " >> $tmp_file
echo "									  " >> $tmp_file
echo "##################################################################" >> $tmp_file
echo "# 8. Check System Deamon & Process" >> $tmp_file
echo "##################################################################" >> $tmp_file
/sbin/chkconfig --list | grep 3:on >> $tmp_file
echo "-----------------------------------------------------------------" >> $tmp_file
/usr/bin/pstree -a -n -p  >> $tmp_file
echo "##################################################################" >> $tmp_file
echo "									  " >> $tmp_file
echo "									  " >> $tmp_file
echo "##################################################################" >> $tmp_file
echo "# 9. Check SystemLog info" >> $tmp_file
echo "##################################################################" >> $tmp_file
echo "# dmesg Log info" >> $tmp_file
echo "##################################################################" >> $tmp_file
/bin/dmesg | egrep -i -e error -e warning -e fail >> $tmp_file
echo "##################################################################" >> $tmp_file
echo "# Messages Log info" >> $tmp_file
echo "##################################################################" >> $tmp_file
/bin/cat /var/log/messages | egrep -i -e error -e warning -e fail >> $tmp_file
echo "##################################################################" >> $tmp_file
echo "# Crond Log info" >> $tmp_file
echo "##################################################################" >> $tmp_file
/bin/cat /var/log/crond | egrep -i -e error -e warning -e fail >> $tmp_file
echo "##################################################################" >> $tmp_file

return 0 

}

# 2013-05-06 Write by Yi HO Sung ##### 
while ( true ) ; do
  echo "                                            "
  echo "============================================"
  echo " OpenSource Consulting system health script"
  echo " Hostname is" $HOST
  echo "============================================"
  echo "                                            "
  echo "                     Write by HoSung Yi RHCE"
  echo "
   Menu's
   ------------------------------------------
    1.  System Memory Info. (80%)
    2.  Disk Check & Mount info
    3.  Network Check & Status
    4.  CPU Model & Usage
    5.  System Load Check 
    6.  Kdump Check
    7.  Filesystem Check
    8.  Check System Deamon & Process
    9.  System Log Check
    10. Print All System log
    q.  Quit

============================================"
  echo -n "                            Select Number : "
  read no

  case $no in 

    "1" ) 
        memoryinfo ;;

    "2" )
        diskcheck ;;

    "3" )     
        cpuinfo ;;

    "4" )
        networkcheck ;;

    "5" ) 
        sysloadavg ;;

    "6" )
        kdumpcheck ;;
    
    "7" )
        checkfilesystem ;;

    "8" )
        checksysdeamon ;;
 
    "9" )
        checksystemlog ;;
     
    "10" )
        systemfullog ;;

    "q" ) 
        exit 0 ;;
   esac
done
