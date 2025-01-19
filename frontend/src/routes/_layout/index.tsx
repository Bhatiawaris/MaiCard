import { Box,
  Container,
  Text,
  Button,
  Flex,
  HStack,
  Icon,
  useDisclosure,
} from "@chakra-ui/react"
import { Block, createFileRoute } from "@tanstack/react-router"
import {QRProfile} from "../../components/QR/QRProfile"

import styled from "styled-components"

import useAuth from "../../hooks/useAuth"
import { FaPlus } from "react-icons/fa"
import AddProfile from "../../components/Profiles/AddProfile"

export const Route = createFileRoute("/_layout/")({
  component: Dashboard,
})

function Dashboard() {
  const addModal = useDisclosure()
  
  const { user: currentUser } = useAuth()
  const cards = [
    { title: "work", color: "blue", description: "null", val: "https://www.google.com" },
    { title: "dating", color: "pink", description: "null", val: "https://chatgpt.com/" },
    { title: "friends", color: "green", description: "null", val: "https://github.com/Bhatiawaris/MaiCard" },
  ]

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