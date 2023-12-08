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

function oneNodeSteps(node) {
	let i = 0;
	while (!node.endsWith("Z")) {
		const instruction = instructions[i++%N];
		node = nextNode(node, instruction);
	}
	return i
}

function greatestCommonDenominator(a, b) {
	return !b ? a : greatestCommonDenominator(b, a % b);
}

function leastCommonMultiple(a, b) {
	return (a * b) / greatestCommonDenominator(a, b);
}

function leastCommonMultipleOfList(l) {
	let multiple = l[0];
	l.forEach(n => {
		multiple = leastCommonMultiple(multiple, n);
	});
	return multiple
}

function part2() {
	return leastCommonMultipleOfList(startNodes.map(n => oneNodeSteps(n)));
}

async function main() {
	console.log(`Part 1: ${part1()}`);
	console.log(`Part 2: ${part2()}`);
}

main().then().catch(
	err => console.error(err)
);
