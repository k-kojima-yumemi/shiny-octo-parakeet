<?php

declare(strict_types=1);

require_once("vendor/autoload.php");

use JsonSchema\Constraints\Constraint;
use Symfony\Component\Console\Application;
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Input\InputOption;
use Symfony\Component\Console\Output\OutputInterface;
use Symfony\Component\Yaml\Yaml;

function getSchema(string $fileName, ?string $target): array
{
    if (str_ends_with($fileName, ".json") || str_ends_with($fileName, ".yaml")) {
        // YAML or JSON file
        $yamlArray = Yaml::parseFile($fileName);
        if (basename($fileName) === "openapi.yaml") {
            $content = $yamlArray["components"]["schemas"][$target];
        } else {
            $content = $yamlArray;
        }
    } else {
        throw new AssertionError();
    }
    return $content;
}

function validate(array $schema, object $json, string $fileName): array
{
    $validator = new JsonSchema\Validator();
    $validator->validate($json, schema: $schema, checkMode: Constraint::CHECK_MODE_TYPE_CAST);
    $error = $validator->getErrors();
    if (!empty($error)) {
        return [
            $fileName => $error
        ];
    } else {
        return [];
    }
}

function array_to_object($array)
{
    $json_str = json_encode($array);
    return json_decode($json_str);
}

function main(OutputInterface $output, string $schemaFileName, string $jsonFileName, ?string $target = null): int
{
    $output->writeln("Start main");
    $schema = getSchema($schemaFileName, $target);
    $json = json_decode(file_get_contents($jsonFileName));
    $error = validate($schema, $json, $jsonFileName);
    foreach ($error as $e) {
        $output->writeln(print_r($e, return: true));
    }
    $output->writeln("End main");
    return empty($error) ? 0 : 1;
}

$application = new Application();
$application
    ->register("lint")
    ->addArgument("schema_file", InputOption::VALUE_REQUIRED)
    ->addArgument("check_files", InputOption::VALUE_REQUIRED)
    ->addArgument("target_schema", InputOption::VALUE_OPTIONAL)
    ->setCode(function (InputInterface $input, OutputInterface $output): int {
        $target = $input->getArgument("target_schema");
        return main(
            output: $output,
            schemaFileName: $input->getArgument("schema_file"),
            jsonFileName: $input->getArgument("check_files"),
            target: empty($target) ? null : $target,
        );
    });

$application->run();
