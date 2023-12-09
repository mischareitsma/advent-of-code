import * as fs from "node:fs";
import { dirname } from "path";
import { fileURLToPath } from "url";
import { stringToNumberArray } from "../utils.js";
import { mult } from "../math.js";

const __dirname = dirname(fileURLToPath(import.meta.url));

const isTest = false;

const fname = (isTest ? "test_" : "") + "input.dat";

const lines = fs.readFileSync(__dirname + "/" + fname).toString().split("\n");
lines.pop();

const times = stringToNumberArray(lines[0].split(":")[1]);
const distances = stringToNumberArray(lines[1].split(":")[1]);

const time = Number.parseInt(lines[0].split(":")[1].replace(/\s/g,""));
const distance = Number.parseInt(lines[1].split(":")[1].replace(/\s/g,""));

function getPossibilitiesToWin(time, distance) {
	let won = 0;
	for (let v = 0; v < time; v++) {
		if (v * (time - v) > distance) won++;
	}

	return won;
}

function part1() {
	return mult(times.map((t, idx) => getPossibilitiesToWin(t, distances[idx])));
		
}

function part2() {
	return getPossibilitiesToWin(time, distance);
}

function main() {
	console.log(`Part 1: ${part1()}`);
	console.log(`Part 2: ${part2()}`);
}

main();
