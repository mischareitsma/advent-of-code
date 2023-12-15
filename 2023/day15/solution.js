import * as fs from "node:fs";
import { dirname } from "path";
import { fileURLToPath } from "url";
import { sum } from "../math.js";

const __dirname = dirname(fileURLToPath(import.meta.url));

const isTest = false;
const testNumber = "";

const fname = (isTest ? `test${testNumber}_` : "") + "input.dat";

const lines = fs.readFileSync(__dirname + "/" + fname).toString().split("\n");
lines.pop();

function hashAlgorithm(char, current) {
	return ((current + char.charCodeAt(0)) * 17) % 256;
}

const lookup = {}
const boxLookup = new Array(256);
const boxContent = new Array(256)

for (let i = 0; i < 256; i++) {
	boxContent[i] = [];
}

lines.forEach(line => {
	for (const char of line) {
		if (char in lookup)
			continue;

		lookup[char] = new Array(256);
		for (let i = 0; i < 256; i++) {
			lookup[char][i] = hashAlgorithm(char, i);
		}
	}
});

function getBoxNumber(label) {
	if (!(label in boxLookup)) {
		let hash = 0;
		for (const char of label) {
			hash = lookup[char][hash];
		}
	
		boxLookup[label] = hash;
	}

	return boxLookup[label];
}

function getLensIndex(boxNumber, label) {
	const box = boxContent[boxNumber];
	for (let i = 0; i < box.length; i++) {
		if (box[i][0] === label)
			return i;
	}
	return -1;
}

function deconstructSequence(sequence) {
	const addIndex = sequence.indexOf("=");
	const removeIndex = sequence.indexOf("-");

	const operation = addIndex !== -1 ? "=" : "-";

	const label = sequence.slice(0, operation === "=" ? addIndex : removeIndex);

	return [
		label,
		operation,
		operation === "=" ? Number.parseInt(sequence.split("=")[1]) : -1
	]
}

lines[0].split(",").forEach(sequence => {
	const [label, operation, focal] = deconstructSequence(sequence);

	const boxNumber = getBoxNumber(label);

	const index = getLensIndex(boxNumber, label);

	if (operation === "=") {
		if (index === -1)
			boxContent[boxNumber].push([label, focal]);
		else
			boxContent[boxNumber][index][1] = focal;
	}
	else {
		if (index > -1)
			boxContent[boxNumber].splice(index, 1);
	}
});

function part1() {
	const hashValues = [];

	lines[0].split(",").forEach((sequence => {
		let hashValue = 0;
		for (const char of sequence) {
			hashValue = lookup[char][hashValue];
		}
		hashValues.push(hashValue);
	}));
	return sum(hashValues);
}

function part2() {
	let focusPower = 0;
	boxContent.forEach((box, boxIdx) => {
		box.forEach((lens, lensIdx) => {
			focusPower += ((boxIdx + 1) * (lensIdx + 1) * lens[1]);
		});
	});
	return focusPower;
}

function main() {
	console.log(`Part 1: ${part1()}`);
	console.log(`Part 2: ${part2()}`);
}

main();
