import * as fs from "node:fs";
import { dirname } from "path";
import { fileURLToPath } from "url";
import { sum, mult } from "../math.js";

const __dirname = dirname(fileURLToPath(import.meta.url));

const isTest = false;

const fname = (isTest ? "test_" : "") + "input.dat"

const lines = fs.readFileSync(__dirname + "/" + fname).toString().split("\n");
lines.pop();

class NumberedPart {
	digits = [];
	isEnginePart = false;

	hasPrinted = false;

	getDigit() {
		return this.digits.reduce((a, b) => a * 10 + b);
	}

	print() {
		if (this.hasPrinted) return;
		this.hasPrinted = true;

		if (this.isEnginePart)
			process.stdout.write(`\x1b[31m${this.getDigit()}\x1b[0m`);
		else
			process.stdout.write(this.getDigit().toString());
	}
}

const engineMap = [];
const symbolLocations = [];

lines.forEach((line, j) => {
	const currentLine = [];
	let numberedPart = new NumberedPart();
	for (let i = 0; i < line.length; i++) {
		const char = line[i];
		const digit = Number.parseInt(char);
		if (digit || digit === 0) {
			numberedPart.digits.push(digit);
			currentLine.push(numberedPart);
			continue;
		}
		else if (numberedPart.digits) {
			numberedPart = new NumberedPart();
		}

		if (!digit && char !== ".") {
			symbolLocations.push([i, j]);
		}
		currentLine.push(char);
	}
	engineMap.push(currentLine);
});

const engineParts = new Set();

const x_max = engineMap[0].length - 1;
const y_max = engineMap.length - 1;

const delta = [-1, 0, 1];

const gearRatios = [];

symbolLocations.forEach((v) => {
	const xc = v[0];
	const yc = v[1];
	const possibleGear = (engineMap[yc][xc] === "*");
	const tempSet = new Set();
	delta.forEach(dx => {
		const x = xc + dx;
		if (x > x_max || x < 0) return;
		delta.forEach(dy => {
			const y = yc + dy;
			if (y > y_max || y < 0) return;
			const possiblePart = engineMap[y][x];
			if (typeof possiblePart === "object") {
				engineParts.add(possiblePart);
				tempSet.add(possiblePart);
				possiblePart.isEnginePart = true;
			}
		});
	});

	if (possibleGear && [...tempSet].length === 2)
		gearRatios.push(mult([...tempSet].map(v => v.getDigit())));
});

function part1() {
	return sum([...engineParts].map((v) => v.getDigit()));
}

function part2() {
	return sum(gearRatios);
}

function main() {
	console.log(`Part 1: ${part1()}`);
	console.log(`Part 2: ${part2()}`);
}

main();
