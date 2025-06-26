import { createTheme } from '@mui/material/styles'

const theme = createTheme({
  palette: {
    primary: {
      main: '#ff4d3f',
      dark: '#e23123',
      light: 'rgba(254, 77, 63, 0.2)',
      contrastText: '#ffffff',
    },
    background: {
      default: '#ffffff',
      paper: '#fafafa',
    },
    text: {
      primary: '#171717',
      secondary: '#7b7b7b',
      disabled: '#c4c4c4',
    },
  },
  typography: {
    fontFamily: 'Open Sans, sans-serif',
    h1: {
      fontFamily: 'Open Sans, sans-serif',
    },
    h2: {
      fontFamily: 'Open Sans, sans-serif',
    },
    h3: {
      fontFamily: 'Open Sans, sans-serif',
    },
    h4: {
      fontFamily: 'Open Sans, sans-serif',
    },
    h5: {
      fontFamily: 'Open Sans, sans-serif',
    },
    h6: {
      fontFamily: 'Open Sans, sans-serif',
    },
    subtitle1: {
      fontFamily: 'Open Sans, sans-serif',
    },
    subtitle2: {
      fontFamily: 'Open Sans, sans-serif',
    },
    body1: {
      fontFamily: 'Open Sans, sans-serif',
    },
    body2: {
      fontFamily: 'Open Sans, sans-serif',
    },
    button: {
      fontFamily: 'Open Sans, sans-serif',
      textTransform: 'none',
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 2,
          '&:hover': {
            backgroundColor: '#e23123',
          },
        },
      },
    },
    MuiAppBar: {
      styleOverrides: {
        root: {
          backgroundColor: '#ff4d3f',
          boxShadow: '4px 4px 8px 0px rgba(0, 0, 0, 0.1)',
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          borderRadius: 2,
        },
      },
    },
  },
})

export default theme
