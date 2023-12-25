import { readFileSync } from "node:fs";
import { dirname } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));

const isTest = false;
const testNumber = "";

const fname = (isTest ? `test${testNumber}_` : "") + "input.dat";

const lines = readFileSync(__dirname + "/" + fname).toString().split("\n");
lines.pop();

const modules = {}
const moduleNames = new Set();

lines.forEach(line => {
	const module = line.split(":")[0];
	const connectedModules = line.split(": ")[1].split(" ");
	moduleNames.add(module);
	if (!(module in modules)) {
		modules[module] = new Set();
	}
	connectedModules.forEach(m => {
		moduleNames.add(m);
		modules[module].add(m)
		if (!(m in modules)) {
			modules[m] = new Set();
		}
		modules[m].add(module);
	});
});

const currentCluster = new Set();
const potentialMembers = new Set();

// Super random, didn't work for 0-6, but oh well, worked for 7
const startModule = Array.from(moduleNames)[7];

currentCluster.add(startModule);
modules[startModule].forEach(m => potentialMembers.add(m));

let pcs = 0;
let pps = 0;
let ccs = currentCluster.size;
let cps = potentialMembers.size;

while (potentialMembers.size !== 3) {
	if (pcs === ccs && pps === cps) throw new Error("Cluster didn't grew this round");
	console.log(`Current cluster size: ${currentCluster.size}, potentialMembers: ${potentialMembers.size}`);
	// Make sure that not by accident currentCluster stuff is considered

	const newPotentialMembers = new Set();
	const newClusterMembers = new Set();

	// potentialMembers.forEach(m => {
	moduleNames.forEach(m => {
		if (currentCluster.has(m)) return;
		const connections = modules[m];
		let n = 0;
		connections.forEach(c => {
			if (currentCluster.has(c) || potentialMembers.has(c))
				n += 1;
		});

		if (n > 1) {
			connections.forEach(c => {
				newPotentialMembers.add(c)
			});
			// potentialMembers.delete(m);
			newClusterMembers.add(m);
		}
	});

	newClusterMembers.forEach(m => currentCluster.add(m));
	newPotentialMembers.forEach(m => potentialMembers.add(m));
	currentCluster.forEach(m => potentialMembers.delete(m));

	pcs = ccs;
	pps = cps;
	ccs = currentCluster.size;
	cps = potentialMembers.size;
}

potentialMembers.forEach(m => {
	let n = 0;
	modules[m].forEach(c => {
		if (currentCluster.has(c))
			n++;
	});
	if (n > 1) currentCluster.add(m);
});

function part1() {
	return currentCluster.size * (moduleNames.size - currentCluster.size);
}

function part2() {
	return "";
}

function main() {
	const answerPart1 = part1();
	const testPart1 = 54
	console.log(`Part 1: ${answerPart1} (test${!isTest ? "" : testPart1 === answerPart1 ? " OK" : " NOK"}: ${testPart1})`);

	const answerPart2 = part2();
	const testPart2 = 0;
	console.log(`Part 2: ${answerPart2} (test${!isTest ? "" : testPart2 === answerPart2 ? " OK" : " NOK"}: ${testPart2})`);
}

main();
