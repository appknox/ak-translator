import { Stack, Skeleton } from '@mui/material'

const TOTAL_TRANSLATIONS_LENGTH = 5

const TranslationLoading = ({ translationsLength }: { translationsLength: number }) => {
  return (
    <Stack direction="column" alignItems="flex-start" justifyContent="center">
      {translationsLength === 0 && (
        <Stack mb={2} direction="column" alignItems="flex-start" justifyContent="center" width="100%">
          <Skeleton variant="text" width={100} height={32} />
          <Skeleton variant="text" width="80%" height={20} />
          <Skeleton variant="text" width="60%" height={20} />
        </Stack>
      )}

      <Stack direction="column" alignItems="flex-start" justifyContent="center" spacing={0.5} width="100%">
        {[...Array(Math.max(0, TOTAL_TRANSLATIONS_LENGTH - translationsLength))].map((_, index) => (
          <Stack
            key={index}
            width="100%"
            direction="row"
            alignItems="center"
            justifyContent="space-between"
            spacing={1}
            height={64}
            sx={{
              borderRadius: 2,
              backgroundColor: 'var(--neutral-grey-100)',
              paddingLeft: 2,
              paddingRight: 2,
            }}
          >
            <Stack direction="row" alignItems="center" spacing={1}>
              <Skeleton variant="rounded" width={50} height={24} />
              <Skeleton variant="rounded" width={84} height={18} />
            </Stack>

            <Stack direction="row" alignItems="center" spacing={1}>
              <Skeleton variant="rounded" width={90} height={18} />
              <Skeleton variant="rounded" width={30} height={30} />
            </Stack>
          </Stack>
        ))}
      </Stack>
    </Stack>
  )
}

export default TranslationLoading
