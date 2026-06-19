import { useState } from 'react'
import './App.css'
import characterData from "./assets/merged.json"
import Card from './Card'
import Row from './Row'
import Dropdown from './Dropdown'
import type Character from './types/Character'

function App() {
  const [guesses, setGuesses] = useState<Array<Character>>([])
  const [query, setQuery] = useState("")
  const [dropdownVisible, setDropdownVisible] = useState(false)


  return (
    <div>
      <div>
        <input 
          type='text' 
          onChange={(e) => setQuery(e.target.value)} 
          onFocus={() => setDropdownVisible(true)} 
          onBlur={() => setDropdownVisible(false)}
        />
        {dropdownVisible 
          ? 
            <Dropdown 
              query={query} 
              onSelect={(selected) => {
                if (!guesses.includes(selected)) {
                  setGuesses((g) => g.concat(selected))
                }
              }}
            /> 
          : 
            <></>
        }
      </div>

      <table>
        <thead>
          <tr className='row'>
            <th scope='col'>Image</th>
            <th scope='col'>Name</th>
            {/* <th scope='col'>Rarity</th> */}
            <th scope='col'>Afflatus</th>
            <th scope='col'>Damage</th>
            <th scope='col'>Tags</th>
          </tr>
        </thead>
        <tbody>
          {guesses.map((guess) => <Row character={guess}/>)}
        </tbody>
      </table>
    </div>
  )


  return (
    <div style={{
      height: "100vh",
      padding: "10px"
    }}>
      <div style={{
        border: "1px solid #B55829",
        backgroundColor: "#00000080",
        height: "100%",
        width: "100%",
        display:"flex",
        flexDirection:"column",
        gap: "4px"
      }}>
        <table>
          <thead>
            <tr className='row'>
              <th scope='col'>Image</th>
              <th scope='col'>Name</th>
              <th scope='col'>Rarity</th>
              <th scope='col'>Afflatus</th>
              <th scope='col'>Damage Type</th>
              <th scope='col'>Tags</th>
            </tr>
          </thead>
          <tbody>
            <Row character={characterData["APPLe"]}/>
            <Row character={characterData["A_Knight"]}/>
            <Row character={characterData["Alexios"]}/>
            <Row character={characterData["An-an_Lee"]}/>
            <Row character={characterData["Anjo_Nala"]}/>
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default App
