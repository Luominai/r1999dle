import { useState } from 'react'
import './App.css'
import Row from './Row'
import Dropdown from './Dropdown'
import type Character from './types/Character'
import bg from "./assets/Hongshan_Forest_Zoo_Collab_Special_Art_01.webp"
import Rand from 'rand-seed';
import characterData from "./assets/complete.json"
import Results from './Results'
import { compare } from './utils'

const today = new Date().toDateString()
const rand = new Rand(today)
const characters = Object.values(characterData)
const dailyCharacter = characters[Math.floor(rand.next() * characters.length)]

function App() {
	const [guesses, setGuesses] = useState<Array<Character | undefined>>([undefined, undefined, undefined, undefined, undefined])
	const [completed, setCompleted] = useState<boolean>(localStorage.getItem("completed") !== null)
	const [correct, setCorrect] = useState<boolean>(localStorage.getItem("correct") === "true")
	const [resultsPageOpen, setResultsPageOpen] = useState<boolean>(false)

	return (
		<div style={{
			backgroundImage: `url(${bg})`,
			backgroundSize: "cover",
			position: "relative"
		}}>
			{
				completed && resultsPageOpen
				? 
					<Results character={dailyCharacter} correct={correct} onClose={() => setResultsPageOpen(false)}/>
				:
					<></>
			}

			<div style={{
				width: "875px",
				maxWidth: "100%",
				margin: "0 auto",
				textAlign: "center",
				minHeight: "100svh",
				display: "flex",
				flexDirection: "column",
				boxSizing: "border-box"
			}}>
				<Dropdown onSelect={(selected) => {
					if (guesses.includes(selected)) {
						return
					}

					if (completed) {
						return
					}

					const indexOfUndefined = guesses.findIndex((val) => val === undefined)
					if (indexOfUndefined !== -1) {
						const copy = guesses.slice()
						copy[indexOfUndefined] = selected
						setGuesses(copy)
					}

					if (indexOfUndefined === guesses.length - 1) {
						setCompleted(true)
					}

					// if every value is truthy, we have the correct answer
					if (Object.values(compare(selected, dailyCharacter)).every((val) => val == true)) {
						setCompleted(true)
						setCorrect(true)
					}
				}} />

				<table>
					<thead>
						<tr className='row'>
							<th scope='col'>Image</th>
							<th scope='col'>Name</th>
							<th scope='col'>Release</th>
							<th scope='col'>Afflatus</th>
							<th scope='col'>Damage</th>
							<th scope='col'>Tags</th>
						</tr>
					</thead>
					<tbody>
						{guesses.map((guess) => {
							if (guess !== undefined) {
								return (
									<Row character={guess} correctness={compare(guess, dailyCharacter)}/>
								)
							}
							return (
								<Row/>
							)
						})}
					</tbody>
				</table>

				{
					completed 
					?
						<div style={{display: "flex", justifyContent: "end"}}>
							<div className="button" onClick={(_) => setResultsPageOpen(true)}>
								See Results
							</div>
						</div>
					:
						<></>
				}
			</div>
		</div>
	)
}

export default App
