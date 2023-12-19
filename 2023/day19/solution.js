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

function getAdvancedRules(rules) {
	const steps = [];
	rules.forEach((rule) => {
		if (rule.indexOf(":") !== -1) {
			steps.push({
				condition: {
					varName: rule[0],
					operator: rule[1],
					value: Number.parseInt(rule.slice(2, rule.indexOf(":"))),
				},
				next: rule.split(":")[1]
			});
		}
		else {
			steps.push({
				next: rule
			});
		}
	});
	return steps;
}

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

const routes = [];
const possibleRoutes = [];

possibleRoutes.push({
	workFlow: "in",
	steps: [],
	ranges: {
		x: { min: 1, max: 4000 },
		m: { min: 1, max: 4000 },
		a: { min: 1, max: 4000 },
		s: { min: 1, max: 4000 }
	}
});

const copyRoute = (route) => {
	return {
		workFlow: route.workFlow,
		steps: [...route.steps],
		ranges: {
			x: { ...route.ranges.x },
			m: { ...route.ranges.m },
			a: { ...route.ranges.a },
			s: { ...route.ranges.s }
		}
	}
}

function updateRange(range, condition, negate) {
	const minMax = condition.operator === "<" ?
		(negate ? "min" : "max") :
		(negate ? "max" : "min");
	const delta = negate ? 0 : (minMax === "max" ? -1 : 1);
	range[minMax] = condition.value + delta;
}

function updateRanges(route, prev, curr) {
	prev.forEach(cond => {
		updateRange(route.ranges[cond.varName], cond, true);
	});

	if (curr)
		updateRange(route.ranges[curr.varName], curr, false);
}

function hasValidRanges(ranges) {
	for (const varName in ranges) {
		if (ranges[varName].min > ranges[varName].max)
			return false;
	}

	return true;
}

while (possibleRoutes.length) {
	const currentRoute = possibleRoutes.pop();

	if (currentRoute.workFlow === "A") {
		routes.push(currentRoute);
		continue;
	}

	if (currentRoute.workFlow === "R")
		continue;

	currentRoute.steps.push(currentRoute.workFlow);

	const previousConditions = [];

	workFlow[currentRoute.workFlow].advancedRules.forEach(rule => {

		// Got some looping going on.
		if (currentRoute.steps.includes(rule.next))
			return;

		const newRoute = copyRoute(currentRoute);
		newRoute.workFlow = rule.next;

		updateRanges(newRoute, previousConditions, rule.condition);

		if (rule.condition)
			previousConditions.push(rule.condition);

		if (!hasValidRanges(newRoute.ranges))
			return;

		possibleRoutes.push(newRoute);
	});
}

function part1() {
	return sum(accepted.map(p => p.x + p.m + p.a + p.s));
}

function part2() {
	return sum(routes.map(route => {
		let combos = 1;
		for (const varName in route.ranges) {
			combos *= (route.ranges[varName].max - route.ranges[varName].min + 1);
		}
		return combos;
	}));
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
