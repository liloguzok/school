<?php 
	session_start();
if (!isset($_SESSION['user'])){
	header("Location: /");
} 
?>

<!doctype html>
<html lang = "en">
<head>
	<meta charset="utf-8">
	<title>Авторизация и регистрация</title>
	<link rel="stylesheet" href="assets/css/main.css">
</head>
<body>
	
	<form action="vendor/signin.php" method="post">
		<img src = "<?= $_SESSION['user']['avatar']?>" width= "100" alt = "">
		<h2><?= $_SESSION['user']['full_name']?></h2>
		<a href="#"><?= $_SESSION['user']['email']?></a>
		<a href="vendor/logout.php" class = "logout">Выход</a>
	</form>
</body>
</html>