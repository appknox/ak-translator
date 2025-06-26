import { useState } from 'react'
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

interface TranslationFormProps {
  onTranslationComplete: (result: TranslationResponse) => void
}

const TranslationForm = ({ onTranslationComplete }: TranslationFormProps) => {
  const [text, setText] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    setError('')
    setIsLoading(true)

    try {
      const requestConfig = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: text }),
      }

      const response = await fetch('http://localhost:8000/translate', requestConfig)

      if (!response.ok) {
        throw new Error('Translation failed')
      }

      const data = await response.json()
      onTranslationComplete(data)
    } catch {
      setError('Failed to translate text. Please try again.')
    } finally {
      setIsLoading(false)
    }
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
                Japanese, Spanish (LATAM), Vietnamese, and Indonesian.
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
          disabled={!text.trim() || isLoading}
          sx={{ minWidth: 200, gap: 1, boxShadow: 'none' }}
        >
          {isLoading && <CircularProgress size={20} sx={{ color: 'var(--neutral-grey-500)' }} />}
          {isLoading ? 'Translating...' : 'Translate to All Languages'}
        </Button>

        {text.trim() && (
          <IconButton onClick={() => setText('')} sx={{ background: 'var(--neutral-grey-100)' }}>
            <Tooltip title="Clear text">
              <DeleteIcon />
            </Tooltip>
          </IconButton>
        )}
      </Stack>
    </Box>
  )
}

export default TranslationForm
