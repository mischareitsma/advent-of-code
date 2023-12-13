import * as fs from "node:fs";
import { dirname } from "path";
import { fileURLToPath } from "url";
import { min } from "../math.js"

const __dirname = dirname(fileURLToPath(import.meta.url));

const isTest = false;

const fname = (isTest ? "test_" : "") + "input.dat"

const lines = fs.readFileSync(__dirname + "/" + fname).toString().split("\n");
lines.pop();

const seeds = lines.shift().split(":")[1].trim().split(" ")
	.filter(v => v !== "").map(v => Number.parseInt(v));

const maps = [];
let map = {};

lines.forEach((line) => {
	if (line === "") {
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

function convertUsingMap(s, m) {
	for (const range of m.ranges) {
		if (s >= range.s && s < (range.s + range.r))
			return range.d + (s - range.s);
	}

	return s;
}

function getLowestSeed(seeds) {
	const locations = [];
	seeds.forEach(seed => {
		let convertedSeedNumber = seed;
		maps.forEach(map => {
			convertedSeedNumber = convertUsingMap(convertedSeedNumber, map);
		});
		locations.push(convertedSeedNumber);
	});

	return Math.min(...locations);
}

function part1() {
	return getLowestSeed(seeds);
}

function part2() {
	let seedRanges = [];
	for (let i = 0; i < seeds.length / 2; i++) {
		seedRanges.push({s: seeds[2*i], r: seeds[2*i + 1]});
	}

	// TODO: Range mechanics come around every year, should make a lib out of it!
	// Include range arithmetics like r1 - r2 giving you back a list of ranges
	const getOverlap = (r1, r2) => {
		// r1 = source map range, r2 is seed range. remainder is what is left of r2.

		// Few conditions:
		// - r1 is of left of r2, there is overlap, r1.s <= r2.s < r1.s + r1.r
		// - r1 is of right of r2, there is overlap, r1.s <= r2.s + r2.r - 1 < r1.s + r1.r
		// - r1 is embedded in r2: r2.s <= r1.s < r2.s + r2.r && r2.s <= r1.s + r1.r - 1 < r2.s + r2.r
		// - r2 is embedded in r1: prev but r1 <=> r2

		const result = {
			overlappingRange: null,
			remainders: []
		};

		if (r1.s <= r2.s && r2.s < r1.s + r1.r) {
			if (r1.s <= r2.s + r2.r - 1 && r2.s + r2.r - 1 < r1.s + r1.r) {
				// r2 fully embedded in r1
				result.overlappingRange = r2;
				// No remainder, r2 is fully in r1
				return result;
			}
			else {
				// r1 left of r2
				result.overlappingRange = {s: r2.s, r: r1.s + r1.r - r2.s};
				result.remainders.push({
					s: r1.s + r1.r,
					r: (r2.s + r2.r) - (r1.s + r1.r)
				});
			}
		}

		if (r2.s <= r1.s && r1.s < r2.s + r2.r) {
			if (r2.s <= r1.s + r1.r - 1 && r1.s + r1.r - 1 < r2.s + r2.r) {
				// r1 fully embedded in r2
				result.overlappingRange = r1;
				result.remainders.push({
					s: r2.s,
					r: r1.s - r2.s

				});
				result.remainders.push({
					s: r1.s + r1.r,
					r: (r2.s + r2.r) - (r1.s + r1.r)
				});
			}
			else {
				// r2 left of r1
				result.overlappingRange = {s: r1.s, r: r2.s + r2.r - r1.s};
				result.remainders.push({
					s: r2.s,
					r: r1.s - r2.s
				});
			}
		}

		return result;
	}

	for (const map of maps) {
		const newSeedRanges = [];
		let processRanges = seedRanges;
		for (const {d, s, r} of map.ranges) {
			let newProcessRanges = [];
			for (const seedRange of processRanges) {
				if (seedRange.skip) continue;
				const {overlappingRange, remainders} =
					getOverlap({s, r}, seedRange);

				if (overlappingRange) {
					newSeedRanges.push({
						s: overlappingRange.s - s + d,
						r: overlappingRange.r
					});
					remainders.forEach(rm => processRanges.push(rm));
				}
				else {
					newProcessRanges.push(seedRange);
				}
			}
			processRanges = newProcessRanges;
		}
		// At this point, all ranges are done and the processRanges array is filled with all ranges that didn"t fit any range in the map.

		seedRanges = newSeedRanges.concat(processRanges);
	}

	// Now we have a big array of seed ranges, just need to find the lowest range.s
	return Math.min(...seedRanges.map(v => v.s));
}

function main() {
	console.log(`Part 1: ${part1()}`);
	// TODO: Part 2 is buggy, I"ve seen negative range, which are "fine", then the range.s is just the "end" of the range, so the minimum might be a different number!
	console.log(`Part 2: ${part2()}`);
}

main();
