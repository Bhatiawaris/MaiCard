import { Html5QrcodeScanner } from "html5-qrcode";
import { useEffect, useRef, useState } from "react";
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


function QRScanner () {
    const scannerRef = useRef(null);
    const addModal = useDisclosure();
    const [scanned,setScanned] = useState<any|null>(null)

    let profileScanner: Html5QrcodeScanner|null = null;
    function onScanSuccess(decodedText: string, decodedResult: any) {
        // handle the scanned code as you like, for example:
        console.log(`Code matched = ${decodedText}`);
        addModal.onOpen()
        profileScanner?.clear()
        const scannedProfile: any = JSON.parse(decodedText)
        console.log(scannedProfile)
        setScanned(scannedProfile)
    }
      
    function onScanFailure(error: any) {
        // handle scan failure, ignore and keep scanning.
    }

    async function onSave() {
        const payload = {
          profile_id1: window.activeProfile,
          profile_id2: scanned,
        }
    
        console.log(payload)
    
        let res = await fetch("http://localhost:8000/api/v1/profiles/saveProfile", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(payload),
        })
    
        console.log(res)
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

                    <ModalFooter gap={3}>
                        <Button variant="primary" onClick={() => {
                            onSave()
                            addModal.onClose()
                        }}>
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