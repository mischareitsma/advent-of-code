import { readFileSync } from "node:fs";
import { dirname } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));

const isTest = true;
const testNumber = "";

const fname = (isTest ? `test${testNumber}_` : "") + "input.dat";

const lines = readFileSync(__dirname + "/" + fname).toString().split("\n");
lines.pop();

function part1() {
	return "";
}

function part2() {
	return "";
}

function main() {
	const answerPart1 = part1();
	const testPart1 = 0
	console.log(`Part 1: ${answerPart1} (test${!isTest ? "" : testPart1 === answerPart1 ? " OK" : " NOK"}: ${testPart1})`);

	const answerPart2 = part2();
	const testPart2 = 0;
	console.log(`Part 2: ${answerPart2} (test${!isTest ? "" : testPart2 === answerPart2 ? " OK" : " NOK"}: ${testPart2})`);
}

main();
