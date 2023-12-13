import * as fs from "node:fs";
import { dirname } from "path";
import { fileURLToPath } from "url";
import { stringToNumberArray } from "../utils.js";

const __dirname = dirname(fileURLToPath(import.meta.url));

const isTest = false;
const testNumber = "";

const fname = (isTest ? `test${testNumber}_` : "") + "input.dat";

const lines = fs.readFileSync(__dirname + "/" + fname).toString().split("\n");
lines.pop();

const SPRING = {
	operational: ".",
	broken: "#",
	unknown: "?"
}

let totalPermutations1 = 0;
let totalPermutations2 = 0;

function unfold(s, d) {
	const a = [];
	for (let i = 0; i < 5; i++)
		a.push(s);

	return a.join(d);
}

lines.forEach(line => {
	const springs = line.split(" ")[0];
	const springGroups = line.split(" ")[1];

	totalPermutations1 += getPermutations(
		Array.from(springs),
		stringToNumberArray(springGroups, ",")
	);

	totalPermutations2 += getPermutations(
		Array.from(unfold(springs, "?")),
		stringToNumberArray(unfold(springGroups, ","), ",")
	);
});

/**
 * Get the number of permutations for a given list of springs and a list of groups of
 * consecutive damaged springs.
 * 
 * @param {string[]} springs Array of springs
 * @param {number[]} springGroups The groups of damaged strings
 * @returns {number} Number of permutations that fit the springGroups.
 */
function getPermutations(springs, springGroups) {
	/* Algorithm:
	We go through the list of strings one by one, replacing the ? with either . or # if
	possible. We keep track of the number of permutations we get at a specific index with
	the number of groups we already found and the number of broken springs in the current
	group.
	*/
	let permutations = [[0, 0, 1]];

	const getNewPermutationCounts = () => {
		
		let permCounts = {}

		permutations.forEach(p => {
			// TODO: (Mischa Reitsma) Nicer way? In Python would use a dict with tuple as key, int as value
			const key = `${p[0]},${p[1]}`;
			if (key in permCounts)
				permCounts[key][2] += p[2];
			else
				permCounts[key] = [...p];
		});

		return permCounts;
	}

	let totalPermutationCounts = getNewPermutationCounts()

	const updatedPermutations = (currentSpring, currentIndex) => {
		const newPermutations = [];

		for (const key in totalPermutationCounts) {
			let [g, c, p] = totalPermutationCounts[key];

			if (currentSpring === SPRING.broken) {
				c++; // Found one more new broken one, add to the count
				if (c <= springGroups[g]) {
					// Counter didn't breach the number we were looking for yet,
					// still a valid permutation
					newPermutations.push([g,c,p]);
				}
			}
			else { // We only get here with a . or #, so no need to do else if / else.
				if (c === springGroups[g]) {
					// This . ended a valid group, increment.
					g++;
					c=0;
					// If we finished finding all groups but there are more 
					// broken springs, we have an invalid config.
					if (
						springGroups.length === g &&
						springs.indexOf(SPRING.broken, currentIndex) !== -1
					)
						continue;
				}

				// Now c should be 0. if not, then we ended a group with invalid
				// length
				if (!c)
					newPermutations.push([g, c, p]);
			}
		}

		// TODO: Could trim more I think. Like if we already made too many groups, or we
		// could check if we can still make it like:
		// sum(springGroups) > currentBroken + remainingBroken + remainingUnknown)

		return newPermutations;
	}

	springs.forEach((spring, i) => {
		if (spring === SPRING.unknown) {
			const newPermsBroken = updatedPermutations(SPRING.broken, i);
			const newPermsOperational = updatedPermutations(SPRING.operational, i);
			permutations = newPermsBroken.concat(newPermsOperational);
		}
		else {
			permutations = updatedPermutations(spring, i);
		}

		// Recreate the permutations map
		totalPermutationCounts = getNewPermutationCounts();

	});

	// Reached end, see if groups are correct
	// Does this work? Gut feeling says yes, but only works because there is an `if broken else`
	// if it would be `if operational else` it would not work
	permutations = updatedPermutations("", springs.length);
	totalPermutationCounts = getNewPermutationCounts();

	let totalPermutations = 0;

	for (const key in totalPermutationCounts) {
		const [g, , p] = totalPermutationCounts[key];
		if (g !== springGroups.length)
			continue;

		totalPermutations += p;
	}

	return totalPermutations;
}

function part1() {
	return totalPermutations1;
}

function part2() {
	return totalPermutations2;
}

function main() {
	console.log(`Part 1: ${part1()}`);
	console.log(`Part 2: ${part2()}`);
}

main();
