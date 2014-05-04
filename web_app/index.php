<!DOCTYPE Html>
<meta charset = 'utf-8'>

<?php 
echo "Welcome to Here!!";
$json = file_get_contents("php://input", true);
if(!empty($json)):
	$file = 'test.json';
	$file_content = file_get_contents($file);
	$file_content.= print_r($json, true);
	file_put_contents($file, $file_content);
endif;

?>
