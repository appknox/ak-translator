import { Container, ThemeProvider, CssBaseline, Divider, Box } from '@mui/material'
import React, { useCallback, useMemo, useState } from 'react'

import Header from '@/components/Header'
import TranslationForm from '@/components/TranslationForm'
import TranslationResult from '@/components/TranslationResult'
import theme from '@/theme'
import TranslationLoading from '@/components/TranslationLoading'

export interface TranslationResponse {
  [language: string]: {
    is_json: boolean
    is_string: boolean
    original_input: string
    target_language: string
    final_translation: string | object
    translation_rating: number
    review_decision: string
    review_reasoning: string
    iterations: number
  }
}

const App = () => {
  const [translationResult, setTranslationResult] = useState<TranslationResponse>({})
  const [isLoadingTranslations, setIsLoadingTranslations] = useState(false)

  const clearTranslationResult = () => setTranslationResult({})
  const translationsLength = useMemo(() => Object.keys(translationResult).length, [translationResult])

  // Update the translation result when a language is completed
  const updateTranslationResult = useCallback((result: TranslationResponse) => {
    setTranslationResult(prev => ({
      ...prev,
      ...result,
    }))
  }, [])

  // Update the loading state when translations are in progress
  const updateLoadingTranslations = useCallback((isLoading: boolean) => {
    setIsLoadingTranslations(isLoading)
  }, [])

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />

      <Header />

      <Container
        style={{
          padding: '100px',
          width: '100vw',
          maxWidth: '100%',
          height: '100%',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'flex-start',
        }}
      >
        <TranslationForm
          onTranslationComplete={updateTranslationResult}
          clearTranslationResult={clearTranslationResult}
          isLoadingTranslations={isLoadingTranslations}
          setIsLoadingTranslations={updateLoadingTranslations}
        />

        <React.Fragment>
          <Divider sx={{ my: 4, width: '100%', borderColor: 'var(--neutral-grey-200)', maxWidth: '800px' }} />

          <Box
            sx={{
              width: '100%',
              maxWidth: '800px',
              display: 'flex',
              flexDirection: 'column',
            }}
          >
            {translationsLength > 0 && <TranslationResult result={translationResult} />}
            {isLoadingTranslations && <TranslationLoading translationsLength={translationsLength} />}
          </Box>
        </React.Fragment>
      </Container>
    </ThemeProvider>
  )
}

export default App
