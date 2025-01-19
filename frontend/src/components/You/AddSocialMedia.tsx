import {
    Button,
    Checkbox,
    CheckboxGroup,
    FormControl,
    FormErrorMessage,
    FormLabel,
    Input,
    Menu,
    MenuButton,
    MenuItem,
    MenuList,
    Modal,
    ModalBody,
    ModalCloseButton,
    ModalContent,
    ModalFooter,
    ModalHeader,
    ModalOverlay,
  } from "@chakra-ui/react";
  
  import { useState } from "react";
  import { ChevronDownIcon } from "@chakra-ui/icons";
  import { useNavigate } from "@tanstack/react-router";
  
  interface AddSocialMediaProps {
    isOpen: boolean;
    onClose: () => void;
  }
  
  const AddSocialMedia = ({ isOpen, onClose }: AddSocialMediaProps) => {
    const [platform, setPlatform] = useState<string>("");
    const [username, setUsername] = useState<string>("");
    const navigate = useNavigate();
  
    async function onSubmit() {
        const payload = {
            user_id: 1,
            social_media_platform: platform,
            social_media_username: username
          }
        
        navigate({ to: "/you" })
    }

    
  
    return (
      <Modal
        isOpen={isOpen}
        onClose={onClose}
        size={{ base: "sm", md: "md" }}
        isCentered
      >
        <ModalOverlay />
        <ModalContent as="form">
          <ModalHeader>Add Social Media Contact</ModalHeader>
          <ModalCloseButton />
          <ModalBody pb={6}>
            <FormControl>
                <FormLabel htmlFor="Social Media Platform">Social Media Platform</FormLabel>
                <Input
                id="Social Media Platform"
                placeholder="Social Media Platform"
                type="text"
                onChange={(e) => setPlatform(e.target.value)}
                value={platform}
                />
            </FormControl>

          <FormControl>
                <FormLabel htmlFor="Social Media Username">Social Media Username</FormLabel>
                <Input
                id="Social Media Username"
                placeholder="Social Media Username"
                type="text"
                onChange={(e) => setUsername(e.target.value)}
                value={username}
                />
            </FormControl>
          </ModalBody>

          <ModalFooter gap={3}>
            <Button variant="primary" onClick={() => {onSubmit(); onClose()}}>
              Save
            </Button>
            <Button onClick={onClose}>Cancel</Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    );
  };
  
  export default AddSocialMedia;
  