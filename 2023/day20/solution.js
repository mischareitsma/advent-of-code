import { readFileSync } from "node:fs";
import { dirname } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));

const isTest = false;
const testNumber = 2;

const fname = (isTest ? `test${testNumber}_` : "") + "input.dat";

const lines = readFileSync(__dirname + "/" + fname).toString().split("\n");
lines.pop();

/*
%: Flip-flop: On or Off, start Off, only flips with low pulses If turns on, sends high pulse, if
   turned off, sends low pulse. High pulses are ignored
&: Conjunction modules: remembers all pulses from all connected modules. When pulse comes, t will
   update memory and send low pulse if all memory is high pulse.
broadcaster: sends incoming pulse to all its connected modules
button module: Starts the process, sends low pulse directly to the broadcaster

pulses are processed in order (fifo)
*/

// Could do thi all over as well:
// const low = false
// const high = true;

class FlipFlop {
	constructor(name, targets) {
		this.name = name;
		this. targets = targets
		this.on = false;
	}

	process(pulse) {
		if (pulse) return;

		this.on = !this.on;

		return {state: this.on, source: this.name, targets: this.targets};
	}

	getState() {
		return this.on;
	}
}

class Conjunction {
	constructor(name, targets) {
		this.name = name;
		this. targets = targets;
		this.sources = []
		this.sourceStates = {};
		this.totalHigh = 0;
	}

	/*
	&: Conjunction modules: remembers all pulses from all connected modules. When pulse comes, t will
	update memory and send low pulse if all memory is high pulse.
	*/

	addSource(sourceName) {
		this.sources.push(sourceName);
		this.sourceStates[sourceName] = false;
	}

	process(pulse, source) {
		if (this.sourceStates[source] !== pulse) {
			this.totalHigh += pulse ? 1 : -1;
			this.sourceStates[source] = pulse
		}

		return {
			state: this.totalHigh !== this.sources.length,
			source: this.name,
			targets: this.targets
		};
	}
}

class Circuit {

	modules = {}
	pulses = [];
	previousPulses = [];
	pulsesOnTarget = [];
	flipFlops = [];
	conjunctions = [];
	endModules = [];
	allModules = [];
	highPulses = 0;
	lowPulses = 0;
	totalPresses = 0;

	pressesRequired = 0;

	addModule(moduleName, targets) {
		if (moduleName === "broadcaster") {
			this.modules[moduleName] = {
				name: moduleName,
				targets: targets
			};
			this.allModules.push(moduleName);
		}
		else if (moduleName[0] === "%") {
			const name = moduleName.slice(1)
			this.modules[name] = new FlipFlop(name, targets);
			this.flipFlops.push(name);
			this.allModules.push(name);
		}
		else if (moduleName[0] === "&") {
			const name = moduleName.slice(1)
			this.modules[name] = new Conjunction(name, targets);
			this.conjunctions.push(name);
			this.allModules.push(name);
		}
		else {
			throw new Error("Invalid module name " + moduleName);
		}
	}

	initializeCircuit() {
		for (const name of this.allModules) {
			for (const targetModule of this.modules[name].targets) {
				if (this.conjunctions.includes(targetModule)) {
					this.modules[targetModule].addSource(name);
				}
				if (!this.allModules.includes(targetModule)) {
					this.endModules.push(targetModule)
				}
			}
		}
	}

	initializeEndModules() {
		for (const name of this.allModules) {
			for (const targetModule of this.modules[name].targets) {
				if (this.conjunctions.includes(targetModule)) {
					this.modules[targetModule].addSource(name);
				}
			}
		}
	}

	pressButton() {
		this.totalPresses++;
		this.increment(false);
		this.pulsesOnTarget = [];
		// this.previousPulses.push({state: false, source: "button", targets: ["broadcaster"]})
		this.pulses.push({
			state: false,
			source: "broadcaster",
			targets: this.modules.broadcaster.targets
		});

		while (this.pulses.length) this.processPulse();

		// if (this.pulsesOnTarget.length)
		// 	console.log("There were pulses");

		console.log(`${this.totalPresses}\t${this.pulsesOnTarget.filter(p => p.state).length}\t${this.pulsesOnTarget.filter(p => !p.state).length}`)

		if (this.pulsesOnTarget.length === 1 && !(this.pulsesOnTarget[0].state))
			this.pressesRequired = this.totalPresses;
	}

	processPulse() {
		const pulse = this.pulses.shift();
		// Could increment number? do that for now, no need to keep track of all pulses
		// this.previousPulses.push(pulse);
		// TODO: increment can be +=pulse.targets.length, saves a few if/elses

		for (const name of pulse.targets) {
			this.increment(pulse.state);

			if (name === "rx")
				this.pulsesOnTarget.push(pulse);

			if (this.endModules.includes(name))
				continue;

			const newPulse = this.modules[name].process(pulse.state, pulse.source);
			if (newPulse)
				this.pulses.push(newPulse);
		}
	}

	increment(pulseState) {
		if (pulseState)
			this.highPulses++;
		else
			this.lowPulses++;
	}

	reset() {
		this.highPulses = 0;
		this.lowPulses = 0;
		this.totalPresses = 0;
		this.pressesRequired = 0;
	}
}

const circuit = new Circuit();
lines.forEach(line => {
	const [name, targets] = line.split(" -> ");
	circuit.addModule(name, targets.split(", "));
});

circuit.initializeCircuit();

function part1() {
	while(circuit.totalPresses < 1000) {
		circuit.pressButton();
	}
	return circuit.highPulses * circuit.lowPulses;
}

function part2() {
	return 0;
	circuit.reset();
	while (circuit.pressesRequired === 0) {
		if (circuit.totalPresses % 100000 === 0)
			console.log("Total presses: " + circuit.totalPresses)
		circuit.pressButton()
	}

	return circuit.pressesRequired;
}

function main() {
	const answerPart1 = part1();
	let testPart1 = 0
	if (testNumber === 1) testPart1 = 32000000;
	if (testNumber === 2) testPart1 = 11687500;
	console.log(`Part 1: ${answerPart1} (test${testNumber}${!isTest ? "" : testPart1 === answerPart1 ? " OK" : " NOK"}: ${testPart1})`);

	const answerPart2 = part2();
	let testPart2 = 0;
	if (testNumber === 1) testPart2 = 0;
	if (testNumber === 2) testPart2 = 0;
	console.log(`Part 1: ${answerPart2} (test${testNumber}${!isTest ? "" : testPart2 === answerPart2 ? " OK" : " NOK"}: ${testPart2})`);
}

main();
