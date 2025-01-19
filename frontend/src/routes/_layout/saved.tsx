import {
  Box,
  Text,
  Container,
  SimpleGrid,
  Card,
  Heading,
  color,
} from "@chakra-ui/react"
import { createFileRoute } from "@tanstack/react-router"
import { useEffect, useState } from "react"


export const Route = createFileRoute("/_layout/saved")({
  component: Saved,
})

function Saved() {
  const [cards,setCards] = useState<any[]>([])
  
  const getSaves = async () => {
    let res = await fetch(`http://localhost:8000/api/v1/profiles/getSaves/${encodeURIComponent(window.activeProfile)}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    })
    console.log(res)
    return res
  }

  useEffect(() => {
    const fetchData = async () => {
      const response = await getSaves()
      const data: any[] = await response.json()
      console.log(data)
      let loadedCards: any[] = []
      data.map((profile) => {
        loadedCards = [...loadedCards, { username: profile.username, contacts: profile.contacts, dateSaved: profile.date_saved, compatability: profile.compatability_score }]
      })
      setCards([...cards, ...loadedCards])
    }
    fetchData()
    
    console.log(cards)
  }, [window.activeProfile])

  return (
    <>
      <Container maxW="full" maxH={"100vh"}>
        <Box m={"1rem"} mt={"2rem"}>
          <Text fontSize="2xl">
            Your Saved Profile Cards
          </Text>
          <Text>Your new connections!</Text>
        </Box>

        <SimpleGrid columns={[1, 2, 3]} spacing='1rem'>
          {cards.length > 0 ? 
            cards.map((card) => (
              <Card key={card.username} height="33fv" width="100%" p={"1rem"}>
                <Heading size="md">{card.username}</Heading>
                {Object.keys(card.contacts).map((social) => (
                  <a key={social} href={card.contacts[social]} style={{color: "blue"}}>{social}</a>
                ))}
                <Text>Compatability score: {card.compatability}</Text>
                <Text>Meeting date: {card.dateSaved}</Text>
              </Card>
            ))
          :
            <Text>No saved profiles yet or no active profile set.</Text>  
          }
        </SimpleGrid>

        </Container>
      </>
  )
}