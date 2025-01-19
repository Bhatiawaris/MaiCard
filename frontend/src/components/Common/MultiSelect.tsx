import {
    Box,
    Checkbox,
    CheckboxGroup,
    Button,
    Menu,
    MenuButton,
    MenuList,
    MenuItem,
    Text,
    Input,
  } from "@chakra-ui/react";
  import { useState } from "react";
  import { ChevronDownIcon } from "@chakra-ui/icons";
  
const MultiSelect = ({ options, id, onChange }: { options: any, id: any, onChange?: any }) => {
    const [selectedValues, setSelectedValues] = useState([]);
  
    const handleChange = (values: any) => {
      setSelectedValues(values);
      console.log(values);
      if (onChange) {
        onChange(values);
      }
    };
  
    return (
        <>
            <Menu closeOnSelect={false}>
                <MenuButton as={Button} rightIcon={<ChevronDownIcon />}>
                {selectedValues.length > 0
                    ? `${selectedValues.length} selected`
                    : "Select options"}
                </MenuButton>
                <MenuList>
                <CheckboxGroup
                    value={selectedValues}
                    onChange={handleChange}
                >
                    {options.map((option: any) => (
                    <MenuItem key={option.value}>
                        <Checkbox value={option.value}>{option.label}</Checkbox>
                    </MenuItem>
                    ))}
                </CheckboxGroup>
                </MenuList>
            </Menu>
            <Input
                type="hidden"
                id={id}
                value={JSON.stringify(selectedValues)}
                readOnly
            />
        </>
    );
};

export default MultiSelect;