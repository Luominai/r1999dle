import type Character from "./types/Character"
import { toDate } from "./utils"

interface RowProps {
  character?: Character
  correctness?: {
    image: boolean,
    name: boolean,
    rarity: boolean,
    release: number,
    afflatus: boolean,
    damage: boolean,
    tags: number
  }
}

const green = "#5adc6341"
const red = "#e9575741"
const yellow = "#f8f25741"

export default function Row({ character, correctness }: RowProps) {
  if (character === undefined) {
    return (
      <tr className="row">
        <th scope="row"></th>
        <td className="cell"></td>
        <td className="cell"></td>
        <td className="cell"></td>
        <td className="cell"></td>
        <td className="cell"></td>
      </tr>
    )
  }

  if (correctness === undefined) {
    return (
      <tr className="row">
        <th scope="row">
          <div>
            <img src={character.image} className="cell"></img>
          </div>
        </th>
        <td className="cell">{character.name}</td>
        <td className="cell">{character.release}</td>
        <td className="cell">{character.afflatus}</td>
        <td className="cell">{character.damage === "Real" ? "Reality" : character.damage}</td>
        <td className="cell">
          {character.tags.map((tag) =>
            <div key={tag} style={{
              display: "flex",
              alignItems: "center",
              justifyContent: "center"
            }}>
              {tag}
            </div>
          )}
        </td>
      </tr>
    )
  }

  return (
    <tr className="row">
      <th scope="row" style={{ backgroundColor: correctness.image ? green : red }}>
        <div>
          <img src={character.image} className="cell"></img>
        </div>
      </th>
      <td className="cell" style={{ backgroundColor: correctness.name ? green : red }}>{character.name}</td>
      <td className="cell" style={{
        backgroundColor: correctness.release === 0 ? green
          : red
      }}>{character.release.map((str) => {
        const date = toDate(str)
        return (
          <div>
            {date.toDateString().split(" ").slice(1).join(" ")}
          </div>
        )
      })}</td>
      <td className="cell" style={{
        backgroundColor: correctness.afflatus ? green : red
      }}>{character.afflatus}</td>
      <td className="cell" style={{ backgroundColor: correctness.damage ? green : red }}>{character.damage === "Real" ? "Reality" : character.damage}</td>
      <td className="cell" style={{
        backgroundColor: correctness.tags === 1 ? green
          : correctness.tags === 0 ? yellow
            : red
      }}>
        {character.tags.map((tag) =>
          <div style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center"
          }}>
            {tag}
          </div>
        )}
      </td>
    </tr>
  )
}