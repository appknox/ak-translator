import { useEffect, useState } from 'react'
import DeleteIcon from '@mui/icons-material/Delete'

import {
  Box,
  Button,
  TextField,
  CircularProgress,
  Typography,
  Divider,
  Stack,
  IconButton,
  Tooltip,
} from '@mui/material'

import type { TranslationResponse } from '@/App'
import wsClient, { TranslationResult } from '@/services/websocket'

interface TranslationFormProps {
  onTranslationComplete: (result: TranslationResponse) => void
  clearTranslationResult: () => void
  isLoadingTranslations: boolean
  setIsLoadingTranslations: (isLoading: boolean) => void
}

const TranslationForm = ({
  onTranslationComplete,
  clearTranslationResult,
  isLoadingTranslations,
  setIsLoadingTranslations,
}: TranslationFormProps) => {
  const [text, setText] = useState('')
  const [error, setError] = useState('')

  // Connect to WebSocket and set up event listeners
  useEffect(() => {
    wsClient.onConnect = () => console.log('WebSocket connected')
    wsClient.onDisconnect = () => console.log('WebSocket disconnected')

    // Update the translation result when a language is completed
    wsClient.onLanguageCompleted = (result: TranslationResult) => {
      if (result.target_language && result.final_translation) {
        onTranslationComplete({
          [result.target_language]: result,
        })
      }
    }

    // Update the translation result when a language is in progress
    wsClient.onProgress = () => setIsLoadingTranslations(true)

    wsClient.onTranslationError = (error: string) => {
      setError(error)
      setIsLoadingTranslations(false)
    }

    wsClient.onAllCompleted = () => setIsLoadingTranslations(false)
    wsClient.connect()

    return () => wsClient.disconnect()
  }, [onTranslationComplete, setIsLoadingTranslations])

  // Reset translations and translate the text when the form is submitted
  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()

    setError('')
    clearTranslationResult()

    wsClient.translateMultiple(text)
  }

  return (
    <Box maxWidth={800} component="form" onSubmit={handleSubmit} sx={{ width: '100%' }}>
      <TextField
        autoFocus={false}
        label="Enter text or JSON to translate"
        multiline
        rows={7}
        fullWidth
        onChange={e => setText(e.target.value)}
        value={text}
        error={!!error}
        helperText={
          error || (
            <Typography variant="caption">
              Supported languages:{' '}
              <Typography variant="caption" color="var(--text-primary)" fontWeight={600}>
                Arabic, French, Japanese, Portuguese, and Spanish
              </Typography>
            </Typography>
          )
        }
        sx={{
          '& .MuiInputBase-root': {
            '& .MuiInputBase-input': {
              '&::placeholder': {
                color: 'var(--text-secondary)',
              },
            },
          },
          '& .MuiOutlinedInput-root': {
            '&:hover .MuiOutlinedInput-notchedOutline': {
              borderWidth: 1,
              borderColor: 'var(--text-secondary)',
            },
            '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
              borderWidth: 1,
              borderColor: 'var(--text-secondary)',
            },
          },
          '& .MuiInputLabel-root': {
            '&.Mui-focused': {
              borderWidth: 1,
              color: 'var(--text-secondary)',
            },
          },
        }}
      />

      <Divider sx={{ my: 4 }} />

      <Stack direction="row" alignItems="center" spacing={1}>
        <Button
          type="submit"
          variant="contained"
          disabled={!text.trim() || isLoadingTranslations}
          sx={{ minWidth: 200, gap: 1, boxShadow: 'none' }}
        >
          {isLoadingTranslations && <CircularProgress size={20} sx={{ color: 'var(--neutral-grey-500)' }} />}
          {isLoadingTranslations ? 'Translating...' : 'Translate to All Languages'}
        </Button>

        {text.trim() && (
          <IconButton
            disabled={isLoadingTranslations}
            onClick={() => {
              setText('')
              setError('')
              clearTranslationResult()
            }}
          >
            <Tooltip title="Clear Translations">
              <DeleteIcon
                sx={{
                  '&:hover': {
                    fill: 'var(--primary-main)',
                  },
                }}
              />
            </Tooltip>
          </IconButton>
        )}
      </Stack>
    </Box>
  )
}

export default TranslationForm
