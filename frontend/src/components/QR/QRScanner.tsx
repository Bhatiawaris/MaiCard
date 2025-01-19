import { Html5QrcodeScanner } from "html5-qrcode";
import { useEffect, useRef } from "react";
import {
    Modal,
    ModalBody,
    ModalCloseButton,
    ModalContent,
    ModalFooter,
    ModalHeader,
    ModalOverlay,
    Box,
    Button,
    useDisclosure,
} from '@chakra-ui/react'
import { Link } from "@tanstack/react-router"
import { profile } from "console";

function QRScanner () {
    const scannerRef = useRef(null);
    const addModal = useDisclosure();
    let profileScanner: Html5QrcodeScanner|null = null;
    function onScanSuccess(decodedText: string, decodedResult: any) {
        // handle the scanned code as you like, for example:
        console.log(`Code matched = ${decodedText}`, decodedResult);
        addModal.onOpen()
        profileScanner?.clear()
    }
      
    function onScanFailure(error: any) {
        // handle scan failure, usually better to ignore and keep scanning.
        // for example:
        console.warn(`Code scan error = ${error}`);
    }
    
    useEffect(() => {
        profileScanner = new Html5QrcodeScanner(
            "reader",
            { fps: 10, qrbox: {width: 250, height: 250}, supportedScanTypes: [0,1] },
            false
        );
        profileScanner?.render(onScanSuccess, onScanFailure);
    })

    return (
        
        <>
            <Modal
                isOpen={addModal.isOpen}
                onClose={() => {
                    addModal.onClose()
                }}
                size={{ base: "xs", md: "md" }}
                isCentered
            >
                <ModalOverlay />
                <ModalContent as="form">
                    <ModalHeader>New Connection</ModalHeader>
                        <ModalCloseButton />
                    <ModalBody pb={6}>
                        PERSONS INFO
                    </ModalBody>

                    <ModalFooter gap={3}>
                        <Button variant="primary" type="submit">
                            Save Profile Card
                        </Button>
                    </ModalFooter>
                </ModalContent>
            </Modal>
            <Box id="reader" ref={scannerRef}/>
        </>
    )
}

export default QRScanner