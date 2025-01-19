import { QrCode } from '@ark-ui/react/qr-code'
import { Box, Button } from '@chakra-ui/react'

export const QRProfile = ({ title, value } : { title: string, value: string}) => {
  return (
    <Box>
      <QrCode.Root defaultValue={value} encoding={{ ecc: 'M' }}>
        <QrCode.Frame>
          <QrCode.Pattern />
        </QrCode.Frame>
        <QrCode.DownloadTrigger fileName={title + `_Profile.png`} mimeType="image/png">
            Save & Share
        </QrCode.DownloadTrigger>
      </QrCode.Root>
    </Box>
  )
}
