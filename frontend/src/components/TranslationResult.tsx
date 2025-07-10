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
  Chip,
  Divider,
} from '@mui/material'

import React, { useState } from 'react'
import { CopyBlock, atomOneDark } from 'react-code-blocks'
import CopyAllIcon from '@mui/icons-material/CopyAll'

import type { TranslationResponse } from '@/App'

interface TranslationResultProps {
  result: TranslationResponse
}

const TranslationResult = ({ result }: TranslationResultProps) => {
  const [, setCopied] = useState(false)

  const handleCopy = (e: React.MouseEvent<HTMLButtonElement>, text: string) => {
    e.stopPropagation()
    navigator.clipboard.writeText(text).then(() => setCopied(true))
  }

  return (
    <React.Fragment>
      <Stack direction="column" alignItems="flex-start" justifyContent="space-between" mb={2}>
        <Typography variant="h6" sx={{ fontWeight: 600 }}>
          Translation Results
        </Typography>

        <Typography variant="body2" color="var(--text-secondary)" sx={{ maxWidth: '800px' }}>
          Please review the translations before using them. The stars indicate the quality rating of the translation,
          and you can view the review reasoning for each language.
        </Typography>
      </Stack>

      {Object.entries(result).map(([language, translation]) => (
        <Accordion key={language} sx={{ width: '100%', mb: 1 }}>
          <AccordionSummary
            sx={{
              width: '100%',
              position: 'sticky',
              top: 64,
              zIndex: 1000,
              backgroundColor: 'var(--neutral-grey-50)',
              '&:hover': {
                backgroundColor: 'var(--background-light)',
              },
            }}
          >
            <Stack width="100%" direction="row" alignItems="center" justifyContent="space-between" spacing={1}>
              <Stack direction="row" alignItems="center" spacing={1}>
                <Typography sx={{ textTransform: 'capitalize' }}>{language}</Typography>

                {translation.iterations > 0 && (
                  <Chip
                    label={`${translation.iterations} iterations`}
                    size="small"
                    color="primary"
                    variant="outlined"
                  />
                )}
              </Stack>

              <Stack direction="row" alignItems="center" spacing={1}>
                <Tooltip arrow title={translation.review_reasoning} placement="top">
                  <Rating
                    value={translation.translation_rating}
                    readOnly
                    size="small"
                    sx={{
                      '& .MuiRating-icon': {
                        color: 'var(--primary-main)',
                      },
                    }}
                  />
                </Tooltip>

                <IconButton onClick={e => handleCopy(e, JSON.stringify(translation.final_translation, null, 2))}>
                  <CopyAllIcon />
                </IconButton>
              </Stack>
            </Stack>
          </AccordionSummary>

          <AccordionDetails sx={{ backgroundColor: 'var(--neutral-grey-100)', borderRadius: 1 }}>
            <Stack spacing={2}>
              {translation.is_json ? (
                <CopyBlock
                  text={JSON.stringify(translation.final_translation, null, 2)}
                  language="json"
                  showLineNumbers={true}
                  wrapLongLines
                  theme={atomOneDark}
                />
              ) : (
                <Stack>
                  <Divider sx={{ my: 2 }} />

                  <Typography p={2} whiteSpace="pre-line" variant="body2" color="var(--text-primary)">
                    {translation.final_translation as string}
                  </Typography>

                  <Divider sx={{ my: 2 }} />
                </Stack>
              )}

              <Box sx={{ mt: 2, p: 2, backgroundColor: 'var(--neutral-grey-200)', borderRadius: 1 }}>
                <Typography variant="subtitle2" color="var(--text-primary)" sx={{ mb: 1 }}>
                  Review Feedback:
                </Typography>

                <Typography variant="body2" color="var(--text-secondary)">
                  {translation.review_reasoning}
                </Typography>
              </Box>
            </Stack>
          </AccordionDetails>
        </Accordion>
      ))}
    </React.Fragment>
  )
}

export default TranslationResult
