import * as fs from "node:fs";
import * as path from "node:path";

async function main() {
	fs.access(dir, (err) => {
		if (err) {
			fs.mkdir(dir);
		}
	});

	const templateContent = await fs.promises.readFile("./template.js", {"encoding": "utf-8"});

	fs.writeFile(path.join(dir, "solution.js"), templateContent, {"encoding": "utf-8"});
}

function getDayFromArgs() {
	const day = process.argv[0];
	
	return day.length === 1 ? "0" + day : day;
}

const day = getDayFromArgs();
const dir = path.join(__dirname, `day${day}`);

main().then(
	console.log(`Created day ${day}`)
).catch(
	(error) => {
		console.error(`Failed creating day ${day}: ${error}`);
	}
);
