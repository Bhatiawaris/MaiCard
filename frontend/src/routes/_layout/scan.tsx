import { Container, Flex } from '@chakra-ui/react';
import { createFileRoute } from '@tanstack/react-router'
import QRScanner from '../../components/QR/QRScanner';

export const Route = createFileRoute('/_layout/scan')({
  component: Scan
})

function Scan () {
    
    return (
        <Container maxW="full">
            <Flex>
                <QRScanner/>
            </Flex>
        </Container>
    )
}