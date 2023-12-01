
const data = {
	verbose: false,
	test: true,
	input: "",
	part: 1,
}

function loadDataFromInput() {
	if (process.argv.length < 2)
		throw new Error("Invalid input, usage node ./solution.js <part> <input-file> [-v]");

	data.part = Number.parseInt(process.argv[0]);
	data.input = process.argv[1];
	data.test = data.input.contains("test");
	data.verbose = process.argv.includes("-v");
}


async function main() {
	loadDataFromInput();
}

function

main().then(
	console.log("Done")
).catch(
	err => console.error(err)
);
