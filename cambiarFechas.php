<?php

if (count($argv) == 1) {
	fixDatetime();
} 
else {
	fixDatetime($argv[1]);
}

function fixDatetime($path = __DIR__) {
	// Usar RecursiveIterator
	$extensions = array('gif', 'png', 'jpg', 'jpeg', 'tiff', 'mp4', 'avi', 'mov', 'flv');

	$files = array();
	$iterator = new RecursiveIteratorIterator(new RecursiveDirectoryIterator($path));
	foreach ($iterator as $file) {
		if ($file->isFile() && in_array(pathinfo($file, PATHINFO_EXTENSION), $extensions)) {
			$files[] = $file->getPathname();
		}
	}

	foreach ($files as $file) {
		$filePath = pathinfo($file, PATHINFO_DIRNAME);
		$fileName = pathinfo($file, PATHINFO_FILENAME);
		$extension = pathinfo($file, PATHINFO_EXTENSION);

		if (substr($fileName, -1) == ')') {
			$indice = substr($fileName, -3);

			if ($indice == '(0)') {
				$indice = '';
			}
		}
		else {
			$indice = '';
		}

		$jsonFile = str_replace($indice, '', $fileName);
		$jsonFile = str_replace('-editado', '', $jsonFile);
		
		$jsonFilePath = $filePath . DIRECTORY_SEPARATOR . substr($jsonFile . '.' . $extension . $indice, 0, 46) . '.json';

		if (file_exists($jsonFilePath)) {
			$jsonData = file_get_contents($jsonFilePath);
			$jsonData = json_decode($jsonData, true);

			if (isset($jsonData['photoTakenTime']['timestamp'])) {
				$new_time = date('U', $jsonData['photoTakenTime']['timestamp']);

				if (!touch($file, $new_time)) {
					echo "Failed to update modified time to {$file}.";
				}
			}
		}
		else {
			echo 'File not found: ' . $jsonFilePath . "\n";
			continue;
		}
	}
}