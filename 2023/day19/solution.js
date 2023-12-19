import { readFileSync } from "node:fs";
import { dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { sum } from "../math.js";

const __dirname = dirname(fileURLToPath(import.meta.url));

const isTest = false;
const testNumber = "";

const fname = (isTest ? `test${testNumber}_` : "") + "input.dat";

const lines = readFileSync(__dirname + "/" + fname).toString().split("\n");
lines.pop();

const workFlow = {}
const parts = [];

const rejected = [];
const accepted = [];

let processingWorkFlow = true;

// function getAdvancedRules(rules) {
// 	steps = [];
// 	for advancedRules
// }

function addRule(line) {
	const workFlowName = line.split("{")[0];
	const rules = line.split("{")[1].split("}")[0].split(",");

	let functionBody = "";
	rules.forEach((rule, idx) => {
		if (idx === rules.length - 1) {
			functionBody+=`return "${rule}";\n`
		}
		else {
			const [condition, target] = rule.split(":");
			functionBody+=`if (xmas.${condition}) return "${target}";\n`
		}
	});

	workFlow[workFlowName] = {
		name: workFlowName,
		rules: rules,
		advancedRules: getAdvancedRules(rules),
		process: new Function("xmas", functionBody)
	}

}

function addPart(line) {
	// parts.push(JSON.parse(line.replace(/=/g, ":")));
	const part = {};

	line.slice(1, -1).split(",").forEach((p) => {
		const [a, b] = p.split("=");
		part[a] = Number.parseInt(b);
	});
	part["route"] = [];
	parts.push(part);
}

lines.forEach((line) => {
	if (!line.length) {
		processingWorkFlow = false;
		return;
	}

	if (processingWorkFlow)
		addRule(line);
	else
		addPart(line);
});

parts.forEach((part) => {
	let nextFunction = "in";
	part.route.push(nextFunction);
	while (nextFunction !== "A" && nextFunction !== "R") {
		nextFunction = workFlow[nextFunction].process(part);
		part.route.push(nextFunction);
	}

	if (nextFunction === "A")
		accepted.push(part);
	else
		rejected.push(part);
});

/* Algo:
- Find the flows from in to A
- List the conditions to pass
*/

const routes = [];


const possibleRoutes = [[{name: "in", condition: ""}]];

while (options.length) {
	const currentRoute = possibleRoutes.pop()


}

function part1() {
	return sum(accepted.map(p => p.x + p.m + p.a + p.s));
}

function part2() {
	return "";
}

function main() {
	const answerPart1 = part1();
	const testPart1 = 19114
	console.log(`Part 1: ${answerPart1} (test${!isTest ? "" : testPart1 === answerPart1 ? " OK" : " NOK"}: ${testPart1})`);

	const answerPart2 = part2();
	const testPart2 = 167409079868000;
	console.log(`Part 1: ${answerPart2} (test${!isTest ? "" : testPart2 === answerPart2 ? " OK" : " NOK"}: ${testPart2})`);
}

main();
