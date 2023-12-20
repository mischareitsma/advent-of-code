import { readFileSync } from "node:fs";
import { dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { lcm } from "../math.js";

const __dirname = dirname(fileURLToPath(import.meta.url));

const isTest = false;
const testNumber = 2;

const fname = (isTest ? `test${testNumber}_` : "") + "input.dat";

const lines = readFileSync(__dirname + "/" + fname).toString().split("\n");
lines.pop();

class FlipFlop {
	constructor(name, targets) {
		this.name = name;
		this. targets = targets
		this.on = false;
	}

	process(pulse) {
		if (pulse) return;

		this.on = !this.on;

		return {
			state: this.getState(),
			source: this.name,
			targets: this.targets
		};
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
			state: this.getState(),
			source: this.name,
			targets: this.targets
		};
	}

	getState() {
		return this.totalHigh !== this.sources.length
	}
}

class Circuit {

	modules = {}
	pulses = [];
	flipFlops = [];
	conjunctions = [];
	endModules = [];
	allModules = [];
	highPulses = 0;
	lowPulses = 0;
	totalPresses = 0;

	watchState = {}

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
					this.modules[targetModule].addSource(
						name
					);
				}
				if (!this.allModules.includes(targetModule)) {
					this.endModules.push(targetModule)
				}
			}
		}
		this.allModules.sort();
	}

	addStateWatcher(moduleName, state) {
		this.watchState[moduleName] = {
			state: state,
			numberOfPresses: 0,
			foundState: false
		}
	}

	pressButton() {
		this.totalPresses++;
		this.pulsesDuringPress = 0;

		this.increment(false);

		this.pulses.push({
			state: false,
			source: "broadcaster",
			targets: this.modules.broadcaster.targets
		});

		while (this.pulses.length) this.processPulse();
	}

	processPulse() {
		const pulse = this.pulses.shift();
		// this.previousPulses.push(pulse);
		for (const name in this.states) {
			this.states[name].push(this.modules[name].getState());
		}

		for (const name of pulse.targets) {
			this.increment(pulse.state);

			if (this.endModules.includes(name))
				continue;

			const newPulse = this.modules[name].process(
				pulse.state,
				pulse.source
			);

			if (newPulse && newPulse.source in this.watchState) {
				const ws = this.watchState[newPulse.source];
				if (!ws.foundState && ws.state === this.modules[newPulse.source].getState()) {
					ws.foundState = true;
					ws.numberOfPresses = this.totalPresses;
				}
			}

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

	foundAllCycles() {
		for (const name in this.watchState) {
			if (!this.watchState[name].foundState)
				return false;
		}
		return true;
	}
}

function getCleanCircuit() {
	const circuit = new Circuit();
	lines.forEach(line => {
		const [name, targets] = line.split(" -> ");
		circuit.addModule(name, targets.split(", "));
	});
	
	circuit.initializeCircuit();
	return circuit;
}

function part1() {

	const circuit = getCleanCircuit();

	while(circuit.totalPresses < 1000) {
		circuit.pressButton();
	}
	return circuit.highPulses * circuit.lowPulses;
}

function part2() {
	if (isTest) return 0;

	/* Looking at the input, the structure is as follows:
	
	- Broadcast is linked to four flip flops that are part of a flip
	  flop chain that each are linked to a conjunction. These are four
	  isolated modules.
	- The conjunctions of those are connected to a conjunction that acts as
	  an inverter.
	- Those inverters are connected to a final conjunction that is then
	  connected to RX.

	We want low to RX, which means all inverters need to send high, which
	means that each module's conjunction needs to send low. These modules
	have some cycle length. The LCM of those cycle lengths is what we want,
	*/

	const circuit = getCleanCircuit();

	const finalConjunction = circuit.conjunctions.filter(
		c => circuit.modules[c].targets[0] === "rx"
	)[0];

	circuit.modules[finalConjunction].sources.forEach(s => {
		circuit.addStateWatcher(circuit.modules[s].sources[0], false)
	});

	
	while(!circuit.foundAllCycles())
		circuit.pressButton();

	const cycles = [];

	for (const name in circuit.watchState) {
		cycles.push(circuit.watchState[name].numberOfPresses);
	}

	return lcm(...cycles);
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
