import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import heroImg from './assets/hero.png'
import './App.css'
import characterData from "./assets/characters.json"
import Row from './Row'

function App() {
  return (
    <>
      <Row character={characterData["A_Knight"]}/>
    </>
  )
}

export default App
