import type Character from "./types/Character"

interface RowProps {
    character: Character
}

export default function Row({character}: RowProps) {
    return (
        <div>
            <img src={character.image}></img>
        </div>
    )
}