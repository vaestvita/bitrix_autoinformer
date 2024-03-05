<?php

if (true )
{

$user ="AMIuser";
$pass = "AMIpass";
$asterisk_ip = "localhost";

$phone_number = $_REQUEST['phone_number'];
$deal_date = $_REQUEST['deal_date'];
$deal_id = $_REQUEST['deal_id'];

$datetime_obj = DateTime::createFromFormat("d.m.Y H:i:s", $deal_date);
$unix_time = $datetime_obj->getTimestamp();

   
        if ( ! empty( $phone_number ) )
        {
		echo "Dialing $phone_number\r\n";
		$timeout = 10;
 
		$socket = fsockopen($asterisk_ip,"5038", $errno, $errstr, $timeout);
		fputs($socket, "Action: Login\r\n");
		fputs($socket, "UserName: $user\r\n");
		fputs($socket, "Secret: $pass\r\n\r\n");
 
		$wrets=fgets($socket,128);
		echo $wrets;
 
		fputs($socket, "Action: Originate\r\n" );
		fputs($socket, "Channel: Local/$phone_number@from-internal\r\n" );
		fputs($socket, "Variable: __deal_date=$unix_time\r\n" );
		fputs($socket, "Variable: __deal_id=$deal_id\r\n" );
		fputs($socket, "Priority: 1\r\n" );
		fputs($socket, "Context: autodialer\r\n" );
		fputs($socket, "Exten: autodialer\r\n" );
		fputs($socket, "Async: yes\r\n" );            
		fputs($socket, "Callerid: $phone_number\r\n\r\n" );
		fputs($socket, "Action: Logoff\r\n\r\n");
                
		while (!feof($socket)) {
  $wrets .= fread($socket, 8192);
}
fclose($socket);
echo <<<ASTERISKMANAGEREND
ASTERISK MANAGER OUTPUT:
$wrets
ASTERISKMANAGEREND;

				
        }
        else
        {
                echo "Unable to determine number from (" . $_REQUEST['phone_number'] . ")\r\n";
        }
}
else
{
echo "please enter number";
}

?>