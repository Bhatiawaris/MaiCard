import {
  Box,
  Flex,
  Text,
  useColorModeValue,
} from "@chakra-ui/react"
import { useQueryClient } from "@tanstack/react-query"

import type { UserPublic } from "../../client"
import BarItems from "./BarItems"

const NavMenu = () => {
  const queryClient = useQueryClient()
  const bgColor = useColorModeValue("ui.light", "ui.dark")
  const textColor = useColorModeValue("ui.dark", "ui.light")
  const secBgColor = useColorModeValue("ui.secondary", "ui.darkSlate")
  const currentUser = queryClient.getQueryData<UserPublic>(["currentUser"])

  return (
    <>
      {/* Mobile */}
      <Box
        position="fixed"
        bottom="0"
        left="0"
        width="100%"
        bg="white"
        boxShadow="0 -2px 5px rgba(0, 0, 0, 0.1)"
        display={{ base: "flex", md: "none" }}
        zIndex="1000"
      >
        <Flex justify="space-around" align="center" py="3%" width="100%">
          <BarItems mobile/>
        </Flex>
      </Box>

      {/* Desktop */}
      <Box
        bg={bgColor}
        p={3}
        h="100vh"
        position="sticky"
        top="0"
        display={{ base: "none", md: "flex" }}
      >
        <Flex
          flexDir="column"
          justify="space-between"
          bg={secBgColor}
          p={4}
          borderRadius={12}
        >
          <Box>
            <BarItems />
          </Box>
          {currentUser?.email && (
            <Text
              color={textColor}
              noOfLines={2}
              fontSize="sm"
              p={2}
              maxW="180px"
            >
              Logged in as: {currentUser.email}
            </Text>
          )}
        </Flex>
      </Box>
    </>
  )
}

export default NavMenu
