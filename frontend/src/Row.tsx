import type Character from "./types/Character"
import star from "./assets/star.png"

interface RowProps {
    character: Character
}

export default function Row({character}: RowProps) {
    return (
        <tr className="row">
            <th scope="row">
                <div>
                    <img src={character.image} className="cell image-cell"></img>
                </div>
            </th>
            <td className="cell name-cell">{character.name}</td>
            <td className="cell rarity-cell" style={{padding: "5px"}}>
                {Array.from({length: character.rarity}).map((_) => {
                    return (
                        <img 
                            style={{
                                margin: "-5px"
                            }}
                            src={star}
                        />
                    )
                })}
            </td>
            <td className="cell afflatus-cell">{character.afflatus}</td>
            <td className="cell damage-cell">{character.damage === "Real" ? "Reality" : character.damage}</td>
            <td className="cell tags-cell">{character.tags.map((tag) => 
                <div style={{
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center"
                }}>
                    {tag}
                </div>
            )}</td>
        </tr>
    )
}