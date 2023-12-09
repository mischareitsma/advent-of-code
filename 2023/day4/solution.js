import * as fs from "node:fs";
import { dirname } from "path";
import { fileURLToPath } from "url";
import { stringToNumberArray } from "../utils.js";
import { sum } from "../math.js";

const __dirname = dirname(fileURLToPath(import.meta.url));

const isTest = false;

const fname = (isTest ? "test_" : "") + "input.dat"

const lines = fs.readFileSync(__dirname + "/" + fname).toString().split("\n");
lines.pop();

const cards = [];

lines.forEach(line => {
	const cardID = Number.parseInt(line.split(":")[0].split(" ")[1]);
	const winningNumbers = stringToNumberArray(line.split(":")[1].split("|")[0]);
	const cardNumbers = stringToNumberArray(line.split(":")[1].split("|")[1]);

	const matches = winningNumbers.filter(v => cardNumbers.includes(v)).length;

	cards.push({
		cardID: cardID,
		winningNumbers: winningNumbers,
		cardNumbers: cardNumbers,
		matches: matches,
		value: matches ? 2 ** (matches - 1) : 0
	});
	
});

function part1() {
	return sum(cards.map(v => v.value));
}

function part2() {
	const totalCards = new Array(cards.length).fill(1);
	cards.forEach((card, i) => {
		for (let j = 0; j < card.matches; j++) {
			totalCards[i + j + 1] += totalCards[i];
		}
	});
	return sum(totalCards);
}

function main() {
	console.log(`Part 1: ${part1()}`);
	console.log(`Part 2: ${part2()}`);
}

main();
