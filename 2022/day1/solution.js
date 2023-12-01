fs = require("fs");

const calories = fs.readFileSync(__dirname + "/input.dat").toString().split('\n');

const summedCalories = [];
let current = 0;

calories.forEach(cal => {
	if (cal === '') {
		summedCalories.push(current);
		current = 0;
	}
	else {
		current += Number.parseInt(cal);
	}
});

summedCalories.push(current);

summedCalories.sort().reverse();

console.log('Max: ' + summedCalories[0]);
console.log('Max 3: ' + (summedCalories[0] + summedCalories[1] + summedCalories[2]));
