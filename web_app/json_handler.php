<!DOCTYPE Html>
<meta charset = 'utf-8'>

<?php 
$obj = json_decode(file_get_contents('test.json'));
print_r ($obj->{'66b55a8defe217ce5bddd6dea5639947'}->{'content'});
echo '<br><br>';
foreach ($obj as $x) {
	print_r($x->{'title'});
	echo '<br>';
}

?>