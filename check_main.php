<?php

declare(strict_types=1);

require_once("vendor/autoload.php");

use Symfony\Component\Yaml\Yaml;

function getSchema(string $fileName, ?string $target = null)
{
    if (str_ends_with($fileName, ".json") || str_ends_with($fileName, ".yaml")) {
        // YAML or JSON file
        $yamlArray = Yaml::parseFile($fileName);
        if (basename($fileName) === "openapi.yaml") {
            $content = array_to_object($yamlArray["components"]["schemas"][$target]);
        } else {
            $content = array_to_object($yamlArray);
        }
    } else {
        throw new AssertionError();
    }

    $validator = new JsonSchema\Validator();
    $json = json_decode(file_get_contents("resources/json/test-region-no-area.json"));

    $exitCode = $validator->validate($json, schema: $content);
    $error = $validator->getErrors();
    print_r($error);
    exit($exitCode);
}

function array_to_object($array)
{
    $json_str = json_encode($array);
    return json_decode($json_str);
}

getSchema("resources/json-schema/regions.json");
