import * as fs from "node:fs";
import { dirname } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));

const isTest = false;
const testNumber = "";

const fname = (isTest ? `test${testNumber}_` : "") + "input.dat";

const lines = fs.readFileSync(__dirname + "/" + fname).toString().split("\n");
lines.pop();

const galaxyMap = lines.map(l => Array.from(l));

const emptyRows = [];
galaxyMap.forEach((r, idx) => {
	if (!r.includes("#"))
		emptyRows.push(idx);
});

const emptyColumns = [];
for (let i = 0; i < galaxyMap[0].length; i++) {
	if (!galaxyMap.map(r => r[i]).includes("#"))
		emptyColumns.push(i);
}

const galaxies = [];
galaxyMap.forEach((r, i) => {
	r.forEach((c, j) => {
		if (c === "#")
			galaxies.push([i,j]);
	});
});

function getDistance(expansionRate) {
	let totalDistance = 0;
	for (let i = 0; i < galaxies.length; i++) {
		for (let j = i; j < galaxies.length; j++) {
			if (i == j) continue;
			let [i1, j1] = galaxies[i];
			let [i2, j2] = galaxies[j];
			if (i1 > i2) [i1, i2] = [i2, i1];
			if (j1 > j2) [j1, j2] = [j2, j1];
			const nEmptyRows = emptyRows.filter(v => (v>i1 && v<i2)).length;
			const nEmptyColumns = emptyColumns.filter(v => (v>j1 && v<j2)).length;
			i2 += (expansionRate - 1) * nEmptyRows;
			j2 += (expansionRate - 1) * nEmptyColumns;
			totalDistance += (i2 - i1) + (j2 - j1);
		}
	}
	return totalDistance;
}

function part1() {
	return getDistance(2);
}

function part2() {
	return getDistance(1000000);
}

function main() {
	console.log(`Part 1: ${part1()}`);
	console.log(`Part 2: ${part2()}`);
}

main();
