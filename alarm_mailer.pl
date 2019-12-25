#!/usr/bin/perl

my $alarm_file = "/var/log/peerapp/peerapp_system_alarm.log";
my ( $last_alarm, $current_alarm, $choped_alarm );
my $time_to_sleep = 5; 
my $mailer_script = "/home/padmin/mailer.sh";
my $first_time_flag = 1;
my @message_arr;

$last_alarm = `/usr/bin/tail -1 $alarm_file`;
chop($last_alarm);

while ( 1 )
{
	$current_alarm = `/usr/bin/tail -1 $alarm_file`;
	chop($current_alarm);
	#if ( "$current_alarm" eq "$last_alarm" )
	#{
	#		print "no change: current_alarm = $current_alarm, last_alarm = $last_alarm\n";
	#}
	#else
	if ("$current_alarm" ne "$last_alarm")
	{
		#print "change: current_alarm = $current_alarm, last_alarm = $last_alarm\n";
		@message_arr = split("\]\: ", $current_alarm);
		$choped_alarm = $message_arr[1];
		#print "choped_alarm = $choped_alarm\n";
		my $cmd = "echo \"$choped_alarm\" | $mailer_script";
		#print "cmd = $cmd\n";
		`$cmd`;
	}
	$last_alarm = $current_alarm;
	sleep ($time_to_sleep);
}
