import * as fs from "node:fs";
import { dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));

const isTest = true;

const fname = (isTest ? `test_` : '') + 'input.dat'

const lines = fs.readFileSync(__dirname + "/" + fname).toString().split('\n');
lines.pop()

/**
 * Get the type of cards. Types available:
 * 
 * - (7) Five of a kind (all cards the same)
 * - (6) Four of a kind (four cards the same)
 * - (5) Full house (three the same and remaining two the same)
 * - (4) Three of a kind (three the same, other two not the same)
 * - (3) Two pair (Two times two cards the same, remaining not the same)
 * - (2) One pair (Two cards the same, rest different)
 * - (1) High cards (No same cards, all different)
 * 
 * @param {string} cards String of five cards
 * @returns Integer value for the type. Higher number is stronger type.
 */
function getTypeFromCards(cards) {
	const counts = getCountsFromCard()

	if (counts[0] === 5) return 7;
	if (counts[0] === 4) return 6;
	if (counts[0] === 3) {
		if (counts[1] === 2) return 5
		else return 4
	}
	if (counts[0] === 2) {
		if (counts[1] === 2) return 3;
		else return 2;
	}
	return 1
}

function getCountsFromCard(cards) {
	// const counts = {
	// 	'A': 0, 'K': 0, 'Q': 0, 'J': 0, 'T': 0, '9': 0, '8': 0,
	// 	'7': 0, '6': 0, '5': 0, '4': 0, '3': 0, '2': 0
	// }
	const countsPerCard = {}
	for (const card of cards) {
		if (card in countsPerCard)
			countsPerCard[card]++;
		else
			countsPerCard[card] = 1;
	}
	const counts = []
	for (const card in countsPerCard) {
		counts.push(countsPerCard[card]);
	}
	return counts.sort().reverse()
}

lines.forEach((line) => {
	const [cards, bid] = line.split(" ")
	const hand = {
		cards: cards,
		bid: Number.parseInt(bid),
		type: getTypeFromCards(cards)
	}
});

function handSorter(hand1, hand2) {

	if (hand1.type === hand2.type) {
		for (let i = 0; i < 5; i++) {
			if (hand1.cards[i] === hand2.cards[i]) continue
			return hand1.cards[i] > 
		}
	}

	return hand1.type > hand2.type ? 1 : -1
}

async function part1() {
	return "";
}

async function part2() {
	return "";
}

async function main() {
	console.log(`Part 1: ${await part1()}`);
	console.log(`Part 2: ${await part2()}`);
}

main().then().catch(
	err => console.error(err)
);
