import { useState } from "react"
import { characters } from "./utils"
import type Character from "./types/Character"

type onSelectFunction = (c: Character) => any

export default function Dropdown({ onSelect }: { onSelect: onSelectFunction }) {
	const [dropdownVisible, setDropdownVisible] = useState(false)
	const [query, setQuery] = useState("")

	let startsWith: Array<Character> = characters.filter((data) => {
		return data.Name.toLowerCase().startsWith(query.toLowerCase())
	})

	let contains: Array<Character> = characters.filter((data) => {
		return data.Name.toLowerCase().includes(query.toLowerCase())
	})

	const subset = [... new Set(startsWith.concat(contains))]

	return (
		<div style={{ display: "flex", justifyContent: "center", marginTop: "20px"}}>
			<div style={{display: "flex", flexDirection: "column", minWidth: "200px", flexGrow: 1, maxWidth: "600px"}}>
				<input
					className="text-input"
					type='text'
					value={query}
					placeholder="Enter a character's name"
					onChange={(e) => setQuery(e.target.value)}
					onFocus={(_) => setDropdownVisible(true) }
					onBlur={(_) => setDropdownVisible(false)}
				/>
				{dropdownVisible
					?
					<div style={{ position: "relative", minWidth: "200px", flexGrow: 1, maxWidth: "600px", zIndex: "2"}}>
						<div className="dropdown-container">
							{subset.map((character) =>
								<div 
									key={character.ID}
									className="dropdown-item"
									onMouseDown={(_) => {
										onSelect(character)
										setQuery("")
									}}>
									<img src={character.Icon_Small} style={{ height: "72px" }}></img>
									{character.Name}
								</div>
							)}
						</div>
					</div>
					:
					<></>
				}
			</div>
		</div>
	)
}