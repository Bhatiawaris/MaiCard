import { Html5QrcodeScanner } from "html5-qrcode";
import { useEffect, useRef } from "react";
import { Box } from "@chakra-ui/react";

function onScanSuccess(decodedText: string, decodedResult: any) {
    // handle the scanned code as you like, for example:
    console.log(`Code matched = ${decodedText}`, decodedResult);
  }
  
function onScanFailure(error: any) {
    // handle scan failure, usually better to ignore and keep scanning.
    // for example:
    console.warn(`Code scan error = ${error}`);
}

function QRScanner () {
    const scannerRef = useRef(null);
    
    useEffect(() => {
        const profileScanner = new Html5QrcodeScanner(
            "reader",
            { fps: 10, qrbox: {width: 250, height: 250}, supportedScanTypes: [0,1] },
            false
        );
        profileScanner.render(onScanSuccess, onScanFailure);
    })

    return (
        <Box id="reader"  ref={scannerRef}/>
    )
}

export default QRScanner