import { readFileSync } from "node:fs";
import { dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { Grid2D } from "../map.js";

const __dirname = dirname(fileURLToPath(import.meta.url));

const isTest = false;
const testNumber = "";

const fname = (isTest ? `test${testNumber}_` : "") + "input.dat";

const lines = readFileSync(__dirname + "/" + fname).toString().split("\n");
lines.pop();

const instructions = [];

let DIRECTIONS = {
	"U": {x: 0, y: 1},
	"L": {x: -1, y: 0},
	"R": {x: 1, y: 0},
	"D": {x: 0, y: -1}
}

let totals = {}

for (const dir in DIRECTIONS) {
	totals[dir] = 0
}

lines.forEach(l => {
	const [p1, p2, p3] = l.split(" ");
	const instruction = {direction: p1, steps: Number.parseInt(p2), color: p3}
	instructions.push(instruction);
	totals[instruction.direction] += instruction.steps;
});

const digMap = new Grid2D(totals["L"] + totals["R"] + 2, totals["U"] + totals["D"] + 2, ".");
const pos = {x: digMap.width / 2, y: digMap.height / 2}
digMap.setValue(pos.x, pos.y, "#");

instructions.forEach(instruction => {
	for (let i = 0; i < instruction.steps; i++) {
		pos.x += DIRECTIONS[instruction.direction].x
		pos.y += DIRECTIONS[instruction.direction].y
		digMap.setValue(pos.x, pos.y, "#");
	}
});

function flood(map, start, value, digValue="#") {
	const floodStack = [];
	floodStack.push(start);

	while (floodStack.length) {
		const pos = floodStack.pop();

		if (map.getValue(pos.x, pos.y) === digValue)
			continue;

		map.setValue(pos.x, pos.y, value);

		for (const dir in DIRECTIONS) {
			const newPos = {x: pos.x + DIRECTIONS[dir].x, y: pos.y + DIRECTIONS[dir].y};
			if (!map.validCoords(newPos.x, newPos.y))
				continue;
			if (map.getValue(newPos.x, newPos.y) === value)
				continue;
			floodStack.push(newPos);
		}
	}
}

digMap.print();
flood(digMap, {x:0, y:0}, "O", "#");
const [x, y] = digMap.getCoords(digMap.values.indexOf("."))
flood(digMap, {x: x, y: y}, "#", "#");
flood(digMap, {x:0, y:0}, ".", "#");

function part1() {
	return digMap.values.filter(v => v === "#").length;
}

function part2() {
	return "Not doable with this solution :-)";
}

function main() {
	console.log(`Part 1: ${part1()}`);
	console.log(`Part 2: ${part2()}`);
}

main();
