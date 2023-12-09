import * as fs from "node:fs";
import { dirname } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));

const isTest = false;
const testNumber = 2;

const fname = (isTest ? `test${testNumber}_` : "") + "input.dat";

const lines = fs.readFileSync(__dirname + "/" + fname).toString().split("\n");
lines.pop();

function part1() {
	let sum = 0;

	lines.forEach(line => {
		let firstDigit = -1, lastDigit = -1;
		for (let i = 0; firstDigit === -1; i++) {
			const char = line.charAt(i);
			const n = Number.parseInt(char);
			if (n || n === 0) firstDigit = n;
		}
		for (let i = line.length - 1; lastDigit === -1; i--) {
			const char = line.charAt(i);
			const n = Number.parseInt(char);
			if (n || n === 0) lastDigit = n;
		}
		sum += firstDigit * 10 + lastDigit;
	});
	return sum;
}

function part2() {
	const digits = [
		"zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
		"0", "1" ,"2", "3", "4", "5", "6", "7", "8", "9"
	];

	let sum = 0;

	lines.forEach((line, ln) => {
		let firstIdx = line.length;
		let firstDigit = 0;
		let lastIdx = -1;
		let lastDigit = 0;
		digits.forEach((v, i) => {
			let firstIdxForDigit = line.indexOf(v);
			let lastIdxForDigit = line.lastIndexOf(v);
			if (firstIdxForDigit === -1 && lastIdxForDigit === -1 ) return;
			if (firstIdxForDigit < firstIdx) {
				firstIdx = firstIdxForDigit;
				firstDigit = i % 10;
			}
			if (lastIdxForDigit > lastIdx) {
				lastIdx = lastIdxForDigit;
				lastDigit = i % 10;
			}
		});

		sum += firstDigit * 10 + lastDigit;
	});

	return sum;
}


function main() {
	console.log(`Part 1: ${part1()}`);
	console.log(`Part 2: ${part2()}`);
}

main();
