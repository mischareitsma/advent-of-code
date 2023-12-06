import * as fs from "node:fs";
import { dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));

const isTest = false;

const fname = (isTest ? `test_` : '') + 'input.dat'

const lines = fs.readFileSync(__dirname + "/" + fname).toString().split('\n');
lines.pop()

function getListOfNumbers(line) {
	return line.split(":")[1]
		.trim()
		.split(" ")
		.filter(v => v !== "")
		.map(v => Number.parseInt(v));
}

const times = getListOfNumbers(lines[0])
const distances = getListOfNumbers(lines[1]);

const time = Number.parseInt(lines[0].split(":")[1].replace(/\s/g,""));
const distance = Number.parseInt(lines[1].split(":")[1].replace(/\s/g,""));

function getPossibilitiesToWin(time, distance) {
	let won = 0;
	for (let v = 0; v < time; v++) {
		if (v * (time - v) > distance) won++;
	}

	return won;
}

async function part1() {
	return times.map((t, idx) => getPossibilitiesToWin(t, distances[idx]))
		.reduce((a, b) => a*b);
}

async function part2() {
	return getPossibilitiesToWin(time, distance);
}

async function main() {
	console.log(`Part 1: ${await part1()}`);
	console.log(`Part 2: ${await part2()}`);
}

main().then().catch(
	err => console.error(err)
);
