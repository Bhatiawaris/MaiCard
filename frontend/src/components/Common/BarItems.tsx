import { Box, Flex, Icon, IconButton, Text, useColorModeValue } from "@chakra-ui/react"
import { useQueryClient } from "@tanstack/react-query"
import { Link } from "@tanstack/react-router"
import { HiMiniWallet } from "react-icons/hi2"
import { MdQrCodeScanner } from "react-icons/md";
import { AiFillProfile } from "react-icons/ai";
import { FaUserEdit } from "react-icons/fa";

import type { UserPublic } from "../../client"

const items = [
  { icon: HiMiniWallet, title: "Wallet", path: "/" },
  { icon: MdQrCodeScanner, title: "Scan", path: "/scan" },
  { icon: AiFillProfile, title: "Saved", path: "/saved" },
  { icon: FaUserEdit, title: "You", path: "/you" },
]

interface BarItemsProps {
  onClose?: () => void
  mobile?: boolean
}

const BarItems = ({ onClose, mobile }: BarItemsProps) => {
  // const queryClient = useQueryClient()
  const textColor = useColorModeValue("ui.main", "ui.light")
  const bgActive = useColorModeValue("#E2E8F0", "#4A5568")
  // const currentUser = queryClient.getQueryData<UserPublic>(["currentUser"])

  // const finalItems = currentUser?.is_superuser
  //   ? [...items, { icon: FiUsers, title: "Admin", path: "/admin" }]
  //   : items
  
  const finalItems = items

  const listItems = finalItems.map(({ icon, title, path }) => 
    <Flex
      as={Link}
      to={path}
      w="100%"
      p={2}
      direction={mobile ? "column" : "row"}
      key={title}
      activeProps={{
        style: {
          background: bgActive,
          borderRadius: "12px",
        },
      }}
      color={textColor}
      onClick={onClose}
      align="center"
    >
      <Icon as={icon} alignSelf="center" />
      <Text>{title}</Text>
    </Flex>
  )

  return (
    <>
      <Flex 
        direction={mobile ? "row" : "column"}
        align={mobile ? "center" : "start"}
        width="80%"
      >
        {listItems}
      </Flex>
    </>
  )
}

export default BarItems
