import * as fs from "node:fs";
import { dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));

const isTest = false;

const fname = (isTest ? `test_` : '') + 'input.dat'

const lines = fs.readFileSync(__dirname + "/" + fname).toString().split('\n');
lines.pop()

const cards = [];

lines.forEach(line => {
	const cardID = Number.parseInt(line.split(":")[0].split(" ")[1]);
	const winningNumbers = line.split(":")[1].split("|")[0].split(" ")
		.filter(e => e !== "")
		.map(v => Number.parseInt(v));
	const cardNumbers = line.split(":")[1].split("|")[1].split(" ")
		.filter(e => e !== "")
		.map(v => Number.parseInt(v));

	const matches = winningNumbers.filter(v => cardNumbers.includes(v)).length;

	cards.push({
		cardID: cardID,
		winningNumbers: winningNumbers,
		cardNumbers: cardNumbers,
		matches: matches,
		value: matches ? 2 ** (matches - 1) : 0
	});
	
});

async function part1() {
	return cards.map(v => v.value).reduce((a, b) => a + b);
}

async function part2() {
	const totalCards = new Array(cards.length).fill(1);
	cards.forEach((card, i) => {
		for (let j = 0; j < card.matches; j++) {
			totalCards[i + j + 1] += totalCards[i];
		}
	});
	// TODO: sum, mult, max, min need to be in some util
	return totalCards.reduce((a, b) => a + b);
}

async function main() {
	console.log(`Part 1: ${await part1()}`);
	console.log(`Part 2: ${await part2()}`);
}

main().then().catch(
	err => console.error(err)
);
