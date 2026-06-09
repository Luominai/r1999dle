import './App.css'
import characterData from "./assets/merged.json"
import Row from './Row'

function App() {
  return (
    <>
      <Row character={characterData["A_Knight"]}/>
    </>
  )
}

export default App
