import * as fs from "node:fs";
import { dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));

const isTest = false;

const fname = (isTest ? `test_` : '') + 'input.dat'

const lines = fs.readFileSync(__dirname + "/" + fname).toString().split('\n');
lines.pop()

const max = {red: 12, green: 13, blue: 14}

let sumValidGames = 0;
let power = 0;

function getCountsFromCubeList(cubeList) {
	const c = {red: 0, green: 0, blue: 0};
	cubeList.split(", ").forEach(cube => {
		c[cube.split(" ")[1]] = Number.parseInt(cube.split(" ")[0])
	});
	return c
}

lines.forEach(line => {
	const id = Number.parseInt(line.split(":")[0].split(" ")[1]);
	let isValid = true;
	const least = {red: 0, green: 0, blue: 0}
	line.split(": ")[1].split("; ").map(getCountsFromCubeList).forEach( counts => {
		for (const color in counts) {
			if (counts[color] > max[color])
				isValid = false;
			if (counts[color] > least[color])
				least[color] = counts[color];
		}
	});

	if (isValid)
		sumValidGames += id;
	power += least.red * least.green * least.blue;

});

async function part1() {
	return sumValidGames;
}

async function part2() {
	return power;
}

async function main() {
	console.log(`Part 1: ${await part1()}`);
	console.log(`Part 2: ${await part2()}`);
}

main().then().catch(
	err => console.error(err)
);
