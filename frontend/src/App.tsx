import { useState } from 'react'
import './App.css'
import Row from './Row'
import Dropdown from './Dropdown'
import type Character from './types/Character'
import bg from "./assets/Hongshan_Forest_Zoo_Collab_Special_Art_01.webp"

function App() {
	const [guesses, setGuesses] = useState<Array<Character>>([])
	return (
		<div style={{
			backgroundImage: `url(${bg})`,
			backgroundSize: "cover"
		}}>
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
					if (!guesses.includes(selected)) {
						setGuesses((g) => g.concat(selected))
					}
				}} />

				<table>
					<thead>
						<tr className='row'>
							<th scope='col'>Image</th>
							<th scope='col'>Name</th>
							<th scope='col'>Rarity</th>
							<th scope='col'>Afflatus</th>
							<th scope='col'>Damage</th>
							<th scope='col'>Tags</th>
						</tr>
					</thead>
					<tbody>
						{guesses.map((guess) => <Row character={guess} />)}
					</tbody>
				</table>
			</div>
		</div>
	)
}

export default App
