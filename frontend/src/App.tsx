import { Container, ThemeProvider, CssBaseline, Divider } from '@mui/material'
import React, { useState } from 'react'

import Header from '@/components/Header'
import TranslationForm from '@/components/TranslationForm'
import TranslationResult from '@/components/TranslationResult'
import theme from '@/theme'

export interface TranslationResponse {
  translations: {
    [language: string]: {
      text: string | Record<string, string>
      accuracy: number
    }
  }
}

const App = () => {
  const [translationResult, setTranslationResult] = useState<TranslationResponse | null>(null)

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
        <TranslationForm onTranslationComplete={setTranslationResult} />

        {translationResult && (
          <React.Fragment>
            <Divider sx={{ my: 4, width: '100%', borderColor: 'var(--neutral-grey-200)' }} />
            <TranslationResult result={translationResult} />
          </React.Fragment>
        )}
      </Container>
    </ThemeProvider>
  )
}

export default App
