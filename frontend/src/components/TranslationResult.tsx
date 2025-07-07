import {
  Box,
  Typography,
  AccordionSummary,
  AccordionDetails,
  Accordion,
  Stack,
  IconButton,
  Rating,
  Tooltip,
} from '@mui/material'

import { useState } from 'react'
import { CopyBlock, atomOneDark } from 'react-code-blocks'
import CopyAllIcon from '@mui/icons-material/CopyAll'
import type { TranslationResponse } from '@/App'

interface TranslationResultProps {
  result: TranslationResponse
}

const TranslationResult = ({ result }: TranslationResultProps) => {
  const [, setCopied] = useState(false)

  const handleCopy = (text: string) => navigator.clipboard.writeText(text).then(() => setCopied(true))

  const isJsonText = (text: string | Record<string, string>): text is Record<string, string> => {
    try {
      JSON.parse(String(text))
      return true
    } catch {
      return false
    }
  }

  return (
    <Box
      sx={{
        width: '100%',
        maxWidth: '800px',
        display: 'flex',
        flexDirection: 'column',
      }}
    >
      <Stack direction="column" alignItems="flex-start" justifyContent="space-between" mb={2}>
        <Typography variant="h6" sx={{ fontWeight: 600 }}>
          Translation Results
        </Typography>

        <Typography variant="body2" color="var(--text-secondary)" sx={{ maxWidth: '800px' }}>
          Please review the translations before using them as they may contain errors. You can copy the translations to
          your clipboard by clicking the copy icon. The stars indicate the estimated accuracy of the translation.
        </Typography>
      </Stack>

      {Object.entries(result.translations).map(([language, translation]) => (
        <Accordion key={language} sx={{ width: '100%' }}>
          <AccordionSummary>
            <Stack
              sx={{ width: '100%' }}
              direction="row"
              alignItems="center"
              justifyContent="space-between"
              spacing={1}
            >
              <Typography sx={{ textTransform: 'capitalize' }}>{language}</Typography>

              <Stack direction="row" alignItems="center" spacing={1}>
                <Tooltip
                  arrow
                  title={`Estimated accuracy: ${(translation.accuracy * 100).toFixed(1)}%`}
                  placement="top"
                >
                  <Rating
                    value={translation.accuracy * 5}
                    precision={0.5}
                    readOnly
                    size="small"
                    sx={{
                      '& .MuiRating-icon': {
                        color: 'var(--primary-main)',
                      },
                    }}
                  />
                </Tooltip>

                <IconButton onClick={() => handleCopy(JSON.stringify(translation.text))}>
                  <CopyAllIcon />
                </IconButton>
              </Stack>
            </Stack>
          </AccordionSummary>

          <AccordionDetails sx={{ backgroundColor: 'var(--neutral-grey-100)', borderRadius: 1 }}>
            {isJsonText(translation.text) ? (
              <CopyBlock
                text={JSON.stringify(JSON.parse(String(translation.text)), null, 4)}
                language="json"
                showLineNumbers={true}
                wrapLongLines
                theme={atomOneDark}
              />
            ) : (
              <Typography>{translation.text}</Typography>
            )}
          </AccordionDetails>
        </Accordion>
      ))}
    </Box>
  )
}

export default TranslationResult
