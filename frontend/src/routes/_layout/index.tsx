import { Box,
  Container,
  Text,
  Button,
  Flex,
  HStack,
  Icon,
  useDisclosure,
} from "@chakra-ui/react"

declare global {
  interface Window {
    activeProfile: number;
  }
}
import { Block, createFileRoute } from "@tanstack/react-router"
import {QRProfile} from "../../components/QR/QRProfile"

import styled from "styled-components"

import useAuth from "../../hooks/useAuth"
import { FaPlus } from "react-icons/fa"
import AddProfile from "../../components/Profiles/AddProfile"
import { useEffect, useState } from "react"

export const Route = createFileRoute("/_layout/")({
  component: Dashboard,
})

function Dashboard() {
  const addModal = useDisclosure()
  const { user: currentUser } = useAuth()
  const [cards,setCards] = useState([
    { title: "networking", color: "blue", val: JSON.stringify({contacts: {"LinkedIn": "https://www.google.com"}, profileId: 1000, username: "Bhatiawaris"})},
    { title: "dating", color: "pink",  val: JSON.stringify({contacts: {"ChatGPT": "https://chatgpt.com/"}, profileId: 1001, username: "Bhatiawaris"})},
    { title: "friends", color: "green", val: JSON.stringify({contacts: {"GitHub": "https://github.com/Bhatiawaris/MaiCard"}, profileId: 1002, username: "Bhatiawaris" })},
  ])

  const getProfiles = async () => {
    let res = await fetch(`http://localhost:8000/api/v1/profiles/getProfiles/${"1"}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    })
    console.log(res)
    return res
  }

  const setActiveProfile = (profileId: number) => {
    window.activeProfile = profileId;
  }

  useEffect(() => {
    const fetchData = async () => {
      const response = await getProfiles()
      const data: any[] = await response.json()
      console.log(data)
      let loadedCards: any[] = []
      data.map((profile) => {
        loadedCards = [...loadedCards, { title: profile.type, color: profile.color ? profile.color : "grey", val: JSON.stringify({contacts: profile.contacts, profileId: profile.profile_id, username: profile.username })}]  
        if (!window.activeProfile) {
          window.activeProfile = profile.profile_id
        }
      })
      setCards([...cards, ...loadedCards])
    }
    fetchData()
    
    console.log(cards)
  }, [])

  return (
    <>
      <Container maxW="full" maxH={"100vh"}>
        <Box m={"1rem"} mt={"2rem"}>
          <Text fontSize="2xl">
            Welcome back, {currentUser?.full_name}
          </Text>
          <Text>How will you connect today?</Text>
        </Box>

        <Box 
          height={"80%"} 
          display={{ base: "flex", md: "none" }}
        >
          <MobileWallet>
            {cards.map((card) => (
              <Card key={card.title} style={{ backgroundColor: card.color }}>
                {card.title}
                <Box backgroundColor="white" m={"3rem"} style={{ borderRadius: "1rem" }}>
                  <QRProfile title={card.title} value={card.val}/>
                </Box>
                <Button onClick={() => setActiveProfile(JSON.parse(card.val).profileId)}>Set as Active</Button>
              </Card>
            ))}
          </MobileWallet>
        </Box>

        <Box 
          height={"50%"}
          display={{ base: "none", md: "flex" }}
          justifyContent="center"
        >
          <DesktopCarousel>
            {cards.map((card) => (
              <Slide key={card.title} style={{ backgroundColor: card.color }}>
                <HStack spacing={"5%"}>
                  <Box backgroundColor="white" m={"0.5%"} alignItems="center" justifyContent="center">
                    <QRProfile title={card.title} value={card.val}/>
                  </Box>
                  <Text textAlign="center" alignSelf="flex-start">
                    {card.title}
                  </Text>
                </HStack>
                <Button onClick={() => setActiveProfile(JSON.parse(card.val).profileId)}>Set as Active</Button>
              </Slide>
            ))}
          </DesktopCarousel>
        </Box>
        
        <Box p={"1rem"}>
          <Button onClick={addModal.onOpen}>
            <Icon as={FaPlus}/> New Profile
          </Button>
          <AddProfile isOpen={addModal.isOpen} onClose={addModal.onClose} />
        </Box>

      </Container>
    </>
  )
}

const MobileWallet = styled.div`
  display: flex;
  overflow-x: scroll;
  scroll-snap-type: x mandatory;
  scroll-behavior: smooth;
  height: 100%;
  width: 100%;
  gap: 1rem;
  padding: 1rem;
  &::-webkit-scrollbar {
    display: none;
  }
`;

const DesktopCarousel = styled(MobileWallet)`
  display: block;
  overflow-y: scroll;
  scroll-snap-type: y mandatory;
  gap: 0;
  width: 100%;
  &::-webkit-scrollbar {
    display: flex;
  }
`

const Card = styled.div`
  scroll-snap-align: center;
  flex: 0 0 90%;
  height: 100%;
  border-radius: 1rem;
  box-shadow: 0 0.25rem 0.5rem rgba(0, 0, 0, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  color: white;
  text-align: center;
  display: block;
`;

const Slide = styled(Card)`
  font-size: 2rem;
  border-radius: 0;
  box-shadow: none;
`;