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

interface AddProfileProps {
  isOpen: boolean;
  onClose: () => void;
}

const AddProfile = ({ isOpen, onClose }: AddProfileProps) => {
  const [title, setTitle] = useState<string>("");
  const [contacts, setContacts] = useState<(string)[]>([]);
  const navigate = useNavigate();

  const options = [
    { label: "LinkedIn", value: "option1" },
    { label: "GitHub", value: "option2" },
    { label: "WhatsApp", value: "option3" },
  ];

  async function onSubmit() {
    let socials: any = {}
    contacts.map((contact) => {
      const { label, value } = JSON.parse(contact)
      socials[label] = value
    })

    const payload = {
      user_id: 1,
      username: "Bhatiawaris",
      type: title,
      contacts: socials,
      text: "",
      color: "yellow",
    }

    console.log(payload)

    let res = await fetch("http://localhost:8000/api/v1/profiles/createProfile", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    })

    navigate({ to: "/" })
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
        <ModalHeader>New Profile Card</ModalHeader>
        <ModalCloseButton />
        <ModalBody pb={6}>
          {/* Title */}
          <FormControl>
            <FormLabel htmlFor="title">Title</FormLabel>
            <Input
              id="title"
              placeholder="Title"
              type="text"
              onChange={(e) => setTitle(e.target.value)}
              value={title}
            />
          </FormControl>

          {/* Contacts */}
          <FormControl mt={4}>
            <FormLabel htmlFor="contacts">Contacts</FormLabel>
            <Menu closeOnSelect={false}>
              <MenuButton as={Button} rightIcon={<ChevronDownIcon />}>
                {contacts.length > 0 ? `${contacts.length} selected` : "Select options"}
              </MenuButton>
              <MenuList>
                <CheckboxGroup value={contacts} onChange={(values: string[]) => {
                    setContacts(values)
                    console.log(contacts)
                  }}
                >
                  {options.map((option) => (
                    <MenuItem key={option.label}>
                      <Checkbox value={JSON.stringify(option)}>{option.label}</Checkbox>
                    </MenuItem>
                  ))}
                </CheckboxGroup>
              </MenuList>
            </Menu>
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

export default AddProfile;
