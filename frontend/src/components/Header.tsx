import { AppBar, Toolbar, Typography } from '@mui/material'
import TranslateIcon from '@mui/icons-material/Translate'

const Header = () => {
  return (
    <AppBar position="fixed" sx={{ mb: 4 }}>
      <Toolbar>
        <TranslateIcon sx={{ mr: 2 }} />

        <Typography variant="h6" component="div">
          Ak Translator
        </Typography>
      </Toolbar>
    </AppBar>
  )
}

export default Header
