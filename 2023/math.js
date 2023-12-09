/**
 * Sum all the elements in an array of numbers.
 * 
 * @param {number[]} arr Array of numbers to sum.
 * @returns {number} The sum of all elements of the array.
 */
export function sum(arr) {
	return arr.reduce((a, b) => a+b, 0);
}

/**
 * Multiply all the elements in an array of numbers.
 * 
 * @param {number[]} arr Array of numbers to multiply.
 * @returns {number} The product of all elements of the array. If the array is empty, returns 1.
 */
export function mult(arr) {
	return arr.reduce((a, b) => a*b, 1);
}

/**
 * Get the minimum number if an array of numbers.
 * 
 * @param {number[]} arr Array of numbers.
 * @returns {number} The minimum value of the array.
 */
export function min(arr) {
	return sort([...arr])[0];
}

/**
 * Get the maximum number if an array of numbers.
 * 
 * @param {number[]} arr Array of numbers.
 * @returns {number} The maximum value of the array.
 */
export function max(arr) {
	return sort([...arr])[arr.length - 1];
}

/**
 * Sort a array of numbers.
 * 
 * This function sorts the array in place, and returns a reference to that same array.
 * 
 * @param {number[]} arr Number array to sort.
 * @returns {number[]} Sorted array.
 */
export function sort(arr) {
	arr.sort((a, b) => a - b);
	return arr;
}

/**
 * Greatest common denominator.
 * 
 * This function calculates the greatest common denominator of two numbers.
 * 
 * @param {number} a First number
 * @param {number} b Second number
 * @returns {number} Greatest common denominator of the two numbers
 */
export function gcd(a, b) {
	return !b ? a : gcd(b, a % b);
}

/**
 * Least common multiple.
 * 
 * This function calculates the least common multiple of two numbers.
 * 
 * @param {number} a First number
 * @param {number} b Second number
 * @returns {number} Least common multiple of the two numbers
 */
export function lcm(a, b) {
	return (a * b) / gcd(a, b);
}
