import * as process from "node:process";
import * as fs from "node:fs";
import * as path from 'path';
import * as url from 'url';

const __dirname = path.dirname(url.fileURLToPath(import.meta.url));

const data = {
	operation: "", // Operation to run. Allowed values in ALLOWED_OPERATIONS
	day: 0, // Day for which to run the operation
	part: 0, // Part to run
	input: '', // Input file name
	test: false, // Flag determines if the current run is a test
	verbose: false, // Verbose flag, prints stuff to terminal
	lines: [], // Lines loaded from the input file
	solutions: [undefined, undefined], // Solutions for the parts.
}

function getInputFilePath() {
	return path.join(__dirname, `day${data.day}`, data.input)
}

const ALLOWED_OPERATIONS = ["create", "run"];

/**
 * Parse command line arguments.
 * 
 * The command line call has the following pattern:
 * node ./aoc.js <operation> [additional flags and options]
 * 
 * Allowed operations are in the {@link ALLOWED_OPERATIONS} array. The additional flags are in the
 * form `-f [<value>]` or `--option [<value>]`, where the value is optional. The supported flags
 * and/or options are:
 * 
 * - `-v` / `--verbose`: Prints all log statements.
 * - `-d` / `--day`: Which day to run, requires integer value as input
 * - `-p` / `--part`: Which part to run, requires integer value as input.
 * - `-i` / `--input`: Which input file to use.
 * - `-t` / `--test`: Run as test.
 * 
 * For the operation "create", the day is required input, the rest is ignored. For the operation
 * run, the day is required. If the part is not passed, try to run both parts. If the input is not
 * passed, guess the input name (input.dat is default).
 * 
 * This function will throw errors if anything is not conform these rules. Error message might be
 * "interesting" if required values are omitted, like: `node ./aoc.js run --input --day 1` will
 * give the error "Invalid option '1'", as `--day` is treated as the input file name.
 */
function parseInput() {

	if (process.argv.length < 3)
		throw new Error("Invalid number of arguments, check parseInput() method doc.");

	data.operation = process.argv[2];
	if (!ALLOWED_OPERATIONS.includes(data.operation))
		throw new Error(
			`Invalid operation '${data.operation}', ` +
			`allowed values: ${ALLOWED_OPERATIONS.toString()}`
		)

	for (let i = 3; i < process.argv.length; i++) {
		const option = process.argv[i];
		switch (option) {
			case '-v':
			case '--verbose':
				data.verbose = true;
				break;
			case '-d':
			case '--day':
				data.day = Number.parseInt(process.argv[++i]);
				if (Number.isNaN(data.day))
					throw new Error(
						"Invalid integer format for day: " + process.argv[i]
					);
				break;
			case '-p':
			case '--part':
				data.part = Number.parseInt(process.argv[++i]);
				if (Number.isNaN(data.part))
					throw new Error(
						"Invalid integer format for part: " +
						process.argv[i]
					);
				break
			case '-i':
			case '--input':
				data.input = process.argv[++i];
				break;
			case '-t':
			case '--test':
				data.test = true;
				break;
			default:
				throw new Error(`Invalid option '${option}'`)
		}
	}

	// Only required option so far doesn't care about the command, so if day is missing,
	// the options were not complete. Might actually make the day a second positional.
	if (data.day === 0)
		throw new Error("Missing required option '-d' / '--day'");

	// Load some sensible defaults
	if (data.input.includes('test')) data.test = true;
	if (data.input === '') data.input = (data.test ? 'test_' : '') + 'input.dat';

	log("Done parsing input");
}

function createDirs() {
	log(`Creating directory and template files for day ${data.day}`);
}

function run() {
	log(`Running day ${data.day} and part ${data.part} (0 = part 1 and 2)`);
	loadFile();
	runSolutions();
	if (data.part === 0 || data.part === 1)
		console.log(`Solution day ${data.day} part 1: ${data.solutions[0]}`)
	if (data.part === 0 || data.part === 2)
		console.log(`Solution day ${data.day} part 2: ${data.solutions[1]}`)

}

function loadFile() {
	data.lines = fs.readFileSync(getInputFilePath()).toString().split('\n');
	data.lines.pop();
}

function runSolutions() {
	const solutions = require(`./day${data.day}/solution`);
	solutions.
	if (data.part === 0 || data.part === 1)
		data.solutions[0] = solutions.part1();
	if (data.part === 0 || data.part === 2)
		data.solutions[0] = solutions.part2();
}

function log(message) {
	if (data.verbose) console.log(message)
}

async function main() {
	parseInput();
	prepData();
	log(`data = ${JSON.stringify(data)}`);
	if (data.operation === "create") {
		createDirs();
	}
	else if (data.operation === "run") {
		run();
	}
	else {
		// Should never get here, parseInput() should handle this.
		throw new Error("Invalid operation " + data.operation)
	}
}

main().then().catch(
	err => console.error(`Error while running aoc.js: ${err}`)
);
