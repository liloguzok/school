<?php

	$connect = mysqli_connect(hostname: "localhost", username: "root",password:'12345', database:'php_auth');

	if (!$connect){
		die("Error connect to database");
	}