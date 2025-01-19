import {
  Container,
  Heading,
  Button,
  Icon,
  Box,
  useDisclosure
} from "@chakra-ui/react"
import { FaPlus } from "react-icons/fa"

import { useQueryClient } from "@tanstack/react-query"
import { createFileRoute } from "@tanstack/react-router"

import type { UserPublic } from "../../client"
import Appearance from "../../components/UserSettings/Appearance"
import ChangePassword from "../../components/UserSettings/ChangePassword"
import DeleteAccount from "../../components/UserSettings/DeleteAccount"
import UserInformation from "../../components/UserSettings/UserInformation"
import SocialMediaList from "../../components/You/SocialMediaList"
import AddSocialMedia from "../../components/You/AddSocialMedia"

const tabsConfig = [
  { title: "My profile", component: UserInformation },
  { title: "Password", component: ChangePassword },
  { title: "Appearance", component: Appearance },
  { title: "Danger zone", component: DeleteAccount },
]

export const Route = createFileRoute("/_layout/you")({
  component: You,
})

const hardcoded_social_options = {
  "whatsapp": "whats_username",
  "discord": "discord_username",
  "instagram": "instagram_username",
};

function You() {
  const addModal = useDisclosure()
  const queryClient = useQueryClient()
  const currentUser = queryClient.getQueryData<UserPublic>(["currentUser"])
  const finalTabs = currentUser?.is_superuser
    ? tabsConfig.slice(0, 3)
    : tabsConfig

  return (
    <Container maxW="full">
      <Heading size="lg" textAlign={{ base: "center", md: "left" }} py={12}>
        User Settings
      </Heading>
      <SocialMediaList data={hardcoded_social_options}>
      </SocialMediaList>
      
      <Box p={"1rem"}>
        <Button onClick={addModal.onOpen}>
          <Icon as={FaPlus}/> Add Social Media
        </Button>
        <AddSocialMedia isOpen={addModal.isOpen} onClose={addModal.onClose} />
      </Box>
    </Container>
  )
}
