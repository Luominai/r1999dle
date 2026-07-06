import type Character from "./types/Character"
import { answer } from "./utils"
import versionOrder from "./assets/versions.json"
import locationGroups from "./assets/location_groups.json"

interface RowProps {
  character?: Character,
  fields: Array<string>
  // correctness?: {
  //   image: boolean,
  //   name: boolean,
  //   rarity: boolean,
  //   release: number,
  //   afflatus: boolean,
  //   damage: boolean,
  //   tags: number
  // }
}

const green = "#5adc6341"
const red = "#e9575741"
const yellow = "#f8f25741"

export default function Row({ character, fields }: RowProps) {
  if (character === undefined) {
    return <EmptyRow/>
  }

  function compare(char1: Character, char2: Character) {
    return fields.map((field) => {
      return comparisonHandlers[field](char1, char2)
    })
  }

  const correctness = compare(character, answer)
  const cells = fields.map((field, idx) => {
    const handler = hotColdHandlers[field] ?? hotColdHandlers["Default"]
    return handler(character[field], correctness[idx])
  })
  
  return (
    <tr className="row">
      <th scope="row" style={{ backgroundColor: correctness.every((val) => val == true) ? green : red }}>
        <div>
          <img src={character.Icon_Small} className="cell"></img>
        </div>
      </th>

      {cells}
    </tr>
  )
}

function EmptyRow(){
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

const comparisonHandlers: Record<string, CallableFunction> = {
  "Version": (c1: Character, c2: Character) => {
    return Math.sign(versionOrder.indexOf(c2.Version) - versionOrder.indexOf(c1.Version))
  },
  "Afflatus": (c1: Character, c2: Character) => {
    if (c1.Afflatus === c2.Afflatus) { return 1 }
    return -1
  },
  "Era": (c1: Character, c2: Character) => {
    if (c1.Era === c2.Era) { return 1 }
    const [s1, e1] = eraToTimeWindow(c1.Era)
    const [s2, e2] = eraToTimeWindow(c2.Era)
    // console.log(s1, e1, s2, e2)
    if (hasOverlap(s1,e1,s2,e2)) { return 0 }
    if (s2 > s1) { return 2 }
    return -1
  },
  "Location": (c1: Character, c2: Character) => {
    if (c1.Location === c2.Location) { return 1 }
    if (locationGroups.find((val) => val.includes(c2.Location))?.includes(c1.Location)) { return 0 }
    return -1
  },
  "Archetypes": (c1: Character, c2: Character) => {
    if (c1.Archetypes.every((type) => c2.Archetypes.includes(type))) { return 1 }
    if (c1.Archetypes.some((type) => c2.Archetypes.includes(type))) { return 0 }
    return -1
  }
}

const hotColdHandlers: Record<string, CallableFunction> = {
  "Default": (val: unknown, correctness: number) => {
    const style = { backgroundColor: correctness == 1 ? green : correctness == 0 ? yellow : red }
    if (Array.isArray(val)) {
      return <td className="cell" style={style}>{val.map((e) => <>{e} <br/></>)}</td>
    }
    // @ts-ignore
    return <td className="cell" style={style}>{val}</td> 
  },
  "Version": (val: string, correctness: number) => {
    const style = { backgroundColor: correctness == 0 ? green :  yellow }
    const indicator = correctness == 0 ? "" : correctness == 1 ? "↑" : "↓"
    return <td className="cell" style={style}>{val} {indicator}</td>
  },
  "Era": (val: string, correctness: number) => {
    const style = { backgroundColor: correctness == 1 ? green : correctness == 0 ? yellow : red}
    const indicator = correctness == 2 ? "↑" : correctness == -1 ? "↓" : ""
    return <td className="cell" style={style}>{val} {indicator}</td>
  },
}

function eraToTimeWindow(era: string){
  if (era.endsWith("s")) {
    const decade = parseInt(era.substring(0, era.length - 1))
    return [decade, decade + 10]
  }
  const parts = era.split(" ")
  if (parts[parts.length - 1] === "BCE") {
    return [-1 * parseInt(parts[0]), -1 * parseInt(parts[0]) + 1]
  }
  if (parts[parts.length - 1] === "century") {
    const century = parseInt(parts[parts.length - 2].substring(0, 2))
    if (parts.length === 2) {
      return [parseInt((century - 1).toString() + "01"), parseInt(century.toString() + "01")]
    }
    if (parts[0] === "early") {
      return [parseInt((century - 1).toString() + "01"), parseInt((century - 1).toString() + "34")]
    }
    if (parts[0] === "mid") {
      return [parseInt((century - 1).toString() + "34"), parseInt((century - 1).toString() + "67")]
    }
    if (parts[0] === "late") {
      return [parseInt((century - 1).toString() + "67"), parseInt(century.toString() + "01")]
    }
  }
  return [parseInt(era), parseInt(era) + 1]
}

function hasOverlap(s1: number, e1: number, s2: number, e2: number) {
  return Math.max(s1, s2) < Math.min(e1, e2)
}