import * as fs from "node:fs";
import { dirname } from "path";
import { fileURLToPath } from "url";
import { sum } from "../math.js";
import { stringToNumberArray } from "../utils.js";

const __dirname = dirname(fileURLToPath(import.meta.url));

const isTest = false;

const fname = (isTest ? "test_" : "") + "input.dat";

const lines = fs.readFileSync(__dirname + "/" + fname).toString().split("\n");
lines.pop();

const digits = lines.map(line => stringToNumberArray(line));

function getNextInSequence(digits, getPrevious) {
	const deltas = [];
	for (let i = 0; i < digits.length - 1; i++) {
		deltas.push(digits[i+1] - digits[i]);
	}

	if (deltas.filter(d => d !== 0).length === 0) return digits[digits.length - 1];

	return getPrevious
		? (digits[0] - getNextInSequence(deltas, getPrevious))
		: (digits[digits.length - 1] + getNextInSequence(deltas, getPrevious));
}

function part1() {
	return sumNextDigitsInSequence(false);
}

function part2() {
	return sumNextDigitsInSequence(true);
}

function sumNextDigitsInSequence(getPrevious) {
	return sum(digits.map(d => getNextInSequence(d, getPrevious)));
}

function main() {
	console.log(`Part 1: ${part1()}`);
	console.log(`Part 2: ${part2()}`);
}

main();
