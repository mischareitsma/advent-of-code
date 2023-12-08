import * as fs from "node:fs";
import { dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));

const isTest = false;
const testNumber = 3;


const fname = (isTest ? `test${testNumber}_` : '') + 'input.dat'

const lines = fs.readFileSync(__dirname + "/" + fname).toString().split('\n');
lines.pop()

const instructions = lines[0];
const N = instructions.length;
console.log(N)

lines.shift()
lines.shift()

const nodes = {}
const startNodes = [];
const allNodes = [];

lines.forEach((line) => {
	const node = line.substring(0, 3)
	allNodes.push(node);
	nodes[node] = {
		left: line.substring(7, 10),
		right: line.substring(12, 15)
	}
	if (node.endsWith("A")) startNodes.push(node);
});

function nextNode(node, instruction) {
	return instruction === "L" ? nodes[node].left : nodes[node].right
}

function part1() {
	let steps = 0;
	let currentNode = 'AAA';

	while (currentNode != 'ZZZ') {
		currentNode = (
			instructions[steps%N] === "L" ?
			nodes[currentNode].left :
			nodes[currentNode].right
		);
		steps++;
	}

	return steps;
}

function part2_old() {
	let steps = 0;
	let currentNodes = [...startNodes];

	console.log(startNodes);
	console.log(JSON.stringify(nodes));

	const atEnd = (nodes) => nodes.filter(n => !n.endsWith("Z")).length === 0

	// TODO: for each start node see if there is a cycle, then go for greatest common denom.

	while(!atEnd(currentNodes)) {
		const newCurrentNodes = [];
		const left = instructions[steps%N] === "L"
		currentNodes.forEach(currentNode => {
			newCurrentNodes.push(
				left ?
				nodes[currentNode].left :
				nodes[currentNode].right
			);
		});
		steps++;
		currentNodes = newCurrentNodes;
	}

	return steps;
}

function findCycle(node) {
	const visitedNodes = {}
	allNodes.forEach(n => {
		visitedNodes[n] = [];
	});

	let idx = 0;
	let steps = 0;
	
	const foundCycle = (n, i) => visitedNodes[n].includes(i);

	let currentNode = startNodes[0];

	while(!foundCycle(currentNode, idx)) {
		currentNode = nextNode(currentNode, instructions[idx]);
		visitedNodes[currentNode].push(idx);
		idx = (idx + 1) % N;
		steps++;
	}

	console.log("Cycle found for first node after " + steps + " steps")
	return steps;
}

function oneNode() {
	// Noticed: cycle = 11836 for all nodes. So after 11836 we are really back to the start
	// and in the same position in the string.
	const steps = startNodes.map(n => findCycle(N));
	console.log("All steps: ")
	console.log(steps);

	let currentNode = startNodes[3];
	console.log("Start: " + currentNode);
	let i = 0;
	while (!currentNode.endsWith("Z")) {
		const instruction = instructions[i%N];
		currentNode = nextNode(currentNode, instruction);
		i++;
		// console.log(`After ${i} steps: ${currentNode}`);
	}
	const firstTime = i;
	currentNode = nextNode(currentNode, instructions[i++%N])
	while (!currentNode.endsWith("Z")) {
		const instruction = instructions[i%N];
		currentNode = nextNode(currentNode, instruction);
		i++;
		// console.log(`After ${i} steps: ${currentNode}`);
	}
	console.log("Next node would be: " + nextNode(currentNode, instructions[i%N]))
	console.log("First: " + firstTime + ", 2nd: " + i + " delta: " + (i-firstTime))
	return "";
}

async function main() {
	console.log(`Part 1: ${part1()}`);
	console.log(`Part 2: ${part2()} (11836 too low)`);
}

main().then().catch(
	err => console.error(err)
);
