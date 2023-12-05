import * as fs from "node:fs";
import { dirname } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));

const isTest = false;

const fname = (isTest ? `test_` : "") + "input.dat"

const lines = fs.readFileSync(__dirname + "/" + fname).toString().split("\n");
lines.pop()

const seeds = lines.shift().split(":")[1].trim().split(" ")
	.filter(v => v !== "").map(v => Number.parseInt(v));

const maps = [];
let map = {}

lines.forEach((line) => {
	if (line === '') {
		maps.push(map);
		map = {
			name: "",
			ranges: []
		};
	}
	else if (map.name === "") {
		map.name = line.split(" ")[0];
	}
	else {
		const values = line.split(" ").map(v => Number.parseInt(v));
		map.ranges.push({d: values[0], s: values[1], r: values[2]});
	}
});

// Add final map and remove initial empty map
maps.push(map);
maps.shift();

// console.log(seeds);
// console.log(JSON.stringify(maps));

function convertUsingMap(s, m) {
	// m.ranges.forEach(range => {
	// 	// console.log(JSON.stringify(range))
	// 	if (s >= range.s && s < (range.s + range.r)) {
	// 		s = range.d + (s - range.s);
	// 		// Return is no break, it is a continue, don't want to throw errors go with
	// 		// traditional for loop. Cleaner anyway.
	// 		return;
	// 	}
	// });

	for (const range of m.ranges) {
		if (s >= range.s && s < (range.s + range.r))
			return range.d + (s - range.s);
	}

	return s;
}

function getLowestSeed(seeds) {
	const locations = []
	seeds.forEach(seed => {
		let convertedSeedNumber = seed;
		// console.log("Seed: " + seed);
		maps.forEach(map => {
			convertedSeedNumber = convertUsingMap(convertedSeedNumber, map);
			// console.log(`After ${map.name}: ${convertedSeedNumber}`);
		});
		locations.push(convertedSeedNumber);
	});

	return locations.reduce((a, b) => (a < b ? a : b))
}

async function part1() {
	return getLowestSeed(seeds);

	// TODO: Whould this work?
	// return seeds.map(s => maps.forEach(m => {s = convertUsingMap(s, m)}))
	// 	.reduce((a, b) => (a < b ? a : b));
}

async function part2() {
	let lowestSeed = 1e99;

	// TODO: If this takes too long, we might need to mass ranges through the maps
	for (let i = 0; i < seeds.length / 2; i++) {
		console.log("Seed pair " + i);
		for (let j = 0; j < seeds[2*i + 1]; j++) {
			let convertedSeedNumber = seeds[2*i] + j
			maps.forEach(map => {
				convertedSeedNumber = convertUsingMap(convertedSeedNumber, map);
			});
			if (convertedSeedNumber < lowestSeed) lowestSeed = convertedSeedNumber;
		}
	}

	return getLowestSeed(newSeeds);
}

async function main() {
	console.log(`Part 1: ${await part1()}`);
	console.log(`Part 2: ${await part2()}`);
}

main().then().catch(
	err => console.error(err)
);
