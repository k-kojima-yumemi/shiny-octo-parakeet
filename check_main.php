<?php

declare(strict_types=1);

require_once("vendor/autoload.php");

use JsonSchema\Constraints\Constraint;
use Symfony\Component\Console\Application;
use Symfony\Component\Console\Input\InputArgument;
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
            if (empty($target)) {
                throw new InvalidArgumentException("target_schema must not be empty if you use openapi");
            }
            if (!isset($yamlArray["components"]["schemas"][$target])) {
                throw new InvalidArgumentException("This schema doesn't have the target '$target'");
            }
            $content = $yamlArray["components"]["schemas"][$target];
        } else {
            $content = $yamlArray;
        }
    } else {
        throw new InvalidArgumentException("The file type '$fileName' is not supported");
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

function main(OutputInterface $output, string $schemaFileName, array $jsonFileNames, ?string $target = null): int
{
    $output->writeln(["Start main",]);
    $schema = getSchema($schemaFileName, $target);
    $errors = [];
    foreach ($jsonFileNames as $jsonFileName) {
        $output->writeln(["Loading " . $jsonFileName]);
        $json = json_decode(file_get_contents($jsonFileName));
        $errors = array_merge($errors, validate($schema, $json, $jsonFileName));
    }
    $output->writeln([str_repeat("=", 20)]);
    foreach ($errors as $name => $e) {
        $output->writeln([
            $name,
            print_r($e, return: true),
            str_repeat("=", 20),
        ]);
    }
    $output->writeln("End main");
    return empty($errors) ? 0 : 1;
}

$application = new Application();
$application
    ->register("lint")
    ->addArgument("schema_file", InputArgument::REQUIRED, "Location of schema JSON/yaml")
    ->addArgument("check_files", InputArgument::REQUIRED | InputArgument::IS_ARRAY, "Space separated files")
    ->addOption("target_schema", "t", InputOption::VALUE_OPTIONAL, "target schema in openapi.yaml", null)
    ->setCode(function (InputInterface $input, OutputInterface $output): int {
        $target = $input->getOption("target_schema");
        return main(
            output: $output,
            schemaFileName: $input->getArgument("schema_file"),
            jsonFileNames: $input->getArgument("check_files"),
            target: empty($target) ? null : $target,
        );
    });

$application->run();
