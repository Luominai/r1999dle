import type Character from "./types/Character"

	export function compare(char1: Character, char2: Character) {
		const output = {
			image: char1.image === char2.image,
			name: char1.name === char2.name,
			rarity: char1.rarity === char2.rarity,
			afflatus: char1.afflatus === char2.afflatus,
			damage: char1.damage === char2.damage,
			tags: -1,
			release: 0
		}

		// return 1 if the 2 characters have the same tags
		if (char1.tags.length === char2.tags.length && char1.tags.every((tag) => char2.tags.includes(tag))) {
			output.tags = 1
		}
		// return 0 if the tags are not identical, but character 1 shares some tags with character 2
		else if (char1.tags.some((tag) => char2.tags.includes(tag))) {
			output.tags = 0
		}

		if (toDate(char1.release[0]) > toDate(char2.release[0])) {
			output.release = 1
		}
		else if (toDate(char1.release[0]) < toDate(char2.release[0])) {
			output.release = -1
		}

		return output
	}

	export function toDate(dateString: string) {
		const monthToNumber: Record<string, number> = {
			"January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6,
			"July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12
		}
		let [month, day, year] = dateString.split(" ")
		const monthNumber = monthToNumber[month]
		const dayNumber = Number(day.substring(0, day.length - 2))
		const yearNumber = Number(year)
		return new Date(yearNumber, monthNumber, dayNumber)
	}