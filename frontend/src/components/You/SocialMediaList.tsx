import React from "react";
import { Box, List, ListItem, ListIcon, Text } from "@chakra-ui/react";
import { IconType } from "react-icons";
import { FaWhatsapp, FaDiscord, FaInstagram } from "react-icons/fa";

// Define the type for the data prop
interface SocialMediaData {
  [key: string]: string;
}

interface SocialMediaListProps {
  data: SocialMediaData;
}

const SocialMediaList: React.FC<SocialMediaListProps> = ({ data }) => {
  // Map platform names to corresponding icons
  const icons: Record<string, IconType> = {
    whatsapp: FaWhatsapp,
    discord: FaDiscord,
    instagram: FaInstagram,
  };
  
  return (
    <Box borderWidth="1px" borderRadius="md" p={4} shadow="sm">
      <Text fontSize="lg" fontWeight="bold" mb={4}>
        Social Media Accounts
      </Text>
      <List spacing={3}>
        {Object.entries(data).map(([platform, username]) => (
          <ListItem key={platform} display="flex" alignItems="center">
            <Text>
              {platform.charAt(0).toUpperCase() + platform.slice(1)}:{" - "}
              {username}
            </Text>
          </ListItem>
        ))}
      </List>
    </Box>
  );
};

export default SocialMediaList;
